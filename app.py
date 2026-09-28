import warnings

warnings.filterwarnings("ignore")

import os
import json
import tempfile
import joblib

from flask import Flask, render_template, request

from utils.resume_parser import extract_text
from utils.skill_extractor import extract_skills
from utils.ats_score import get_ats_details
from utils.recommendation import recommend_jobs
from utils.prediction_engine import predict_role
from utils.url_extractor import extract_urls
from utils.github_analyzer import analyze_github
from utils.portfolio_analyzer import analyze_portfolio

from chatbot import generate_milo_response


app = Flask(__name__)


# =========================================================
# VERCEL-SAFE UPLOAD CONFIGURATION
# =========================================================

# Vercel's deployed filesystem is read-only.
# /tmp is the writable temporary directory.
UPLOAD_FOLDER = tempfile.gettempdir()

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER


# =========================================================
# LOAD ML MODEL
# =========================================================

BASE_DIR = os.path.dirname(
    os.path.abspath(__file__)
)

model = joblib.load(
    os.path.join(
        BASE_DIR,
        "models",
        "resume_classifier.pkl"
    )
)

vectorizer = joblib.load(
    os.path.join(
        BASE_DIR,
        "models",
        "vectorizer.pkl"
    )
)


# =========================================================
# HOME PAGE
# =========================================================

@app.route("/")
def home():

    return render_template(
        "index.html"
    )


# =========================================================
# UPLOAD PAGE
# =========================================================

@app.route("/upload")
def upload():

    return render_template(
        "upload.html"
    )


# =========================================================
# RESUME ANALYSIS
# =========================================================

@app.route(
    "/predict",
    methods=["POST"]
)
def predict():

    if "resume" not in request.files:

        return "No file uploaded."

    file = request.files["resume"]

    if file.filename == "":

        return "No file selected."

    opportunity_type = request.form.get(
        "opportunity_type",
        "job"
    ).strip().lower()

    if opportunity_type not in [
        "job",
        "internship"
    ]:

        opportunity_type = "job"


    # =====================================================
    # SAVE RESUME TO TEMPORARY VERCEL STORAGE
    # =====================================================

    safe_filename = os.path.basename(
        file.filename
    )

    filepath = os.path.join(
        app.config["UPLOAD_FOLDER"],
        safe_filename
    )

    try:

        file.save(
            filepath
        )

    except Exception as error:

        print(
            "Resume save error:",
            error
        )

        return (
            "Unable to temporarily save the uploaded "
            "resume. Please try again."
        )


    # =====================================================
    # EXTRACT RESUME TEXT
    # =====================================================

    try:

        text = extract_text(
            filepath
        )

    except Exception as error:

        print(
            "Resume parser error:",
            error
        )

        text = ""


    if not text or not text.strip():

        try:
            if os.path.exists(filepath):
                os.remove(filepath)
        except Exception:
            pass

        return (
            "Unable to extract readable text "
            "from this resume."
        )


    # =====================================================
    # EXTRACT SKILLS
    # =====================================================

    skills = extract_skills(
        text
    )


    # =====================================================
    # ATS ANALYSIS
    # =====================================================

    ats_details = get_ats_details(
        skills,
        text
    )

    ats_score = ats_details.get(
        "score",
        0
    )


    # =====================================================
    # ML ROLE PREDICTION
    # =====================================================

    text_vector = vectorizer.transform(
        [text]
    )

    ml_prediction = model.predict(
        text_vector
    )[0]


    # =====================================================
    # URL EXTRACTION
    # =====================================================

    detected_urls = extract_urls(
        text
    )

    github_urls = [
        item["url"]
        for item in detected_urls
        if item.get("type") == "github"
    ]

    portfolio_urls = [
        item["url"]
        for item in detected_urls
        if item.get("type") == "portfolio"
    ]


    # =====================================================
    # GITHUB ANALYSIS
    # =====================================================

    github_evidence = None

    if github_urls:

        try:

            github_evidence = analyze_github(
                github_urls[0]
            )

        except Exception as error:

            print(
                "GitHub analysis error:",
                error
            )

            github_evidence = None


    # =====================================================
    # PORTFOLIO ANALYSIS
    # =====================================================

    portfolio_evidence = []

    for portfolio_url in portfolio_urls[:2]:

        try:

            portfolio_result = analyze_portfolio(
                portfolio_url
            )

            portfolio_evidence.append(
                portfolio_result
            )

        except Exception as error:

            print(
                "Portfolio analysis error:",
                error
            )


    # =====================================================
    # EXTERNAL EVIDENCE
    # =====================================================

    external_evidence = {

        "github": github_evidence,

        "portfolio": portfolio_evidence

    }


    # =====================================================
    # FINAL ROLE PREDICTION
    # =====================================================

    prediction_result = predict_role(

        text=text,

        ml_prediction=ml_prediction,

        github_evidence=github_evidence,

        portfolio_evidence=portfolio_evidence

    )

    if not isinstance(
        prediction_result,
        dict
    ):

        prediction_result = {

            "role": str(
                prediction_result
            )

        }

    prediction_result[
        "portfolio_evidence"
    ] = portfolio_evidence

    prediction_result[
        "external_evidence"
    ] = external_evidence

    prediction = prediction_result.get(
        "role",
        ml_prediction
    )


    # =====================================================
    # LIVE OPPORTUNITY SEARCH
    # =====================================================

    print(
        "\n========================================"
    )

    print(
        "LIVE OPPORTUNITY SEARCH"
    )

    print(
        "Selected type:",
        opportunity_type
    )

    print(
        "Predicted role:",
        prediction
    )

    print(
        "ATS score:",
        ats_score
    )

    print(
        "========================================\n"
    )


    try:

        recommendations = recommend_jobs(

            prediction,

            opportunity_type=opportunity_type,

            resume_text=text,

            skills=skills

        )

    except TypeError:

        recommendations = recommend_jobs(

            prediction,

            opportunity_type=opportunity_type,

            resume_text=text

        )

    except Exception as error:

        print(
            "Recommendation API error:",
            error
        )

        recommendations = []


    if not isinstance(
        recommendations,
        list
    ):

        recommendations = []


    # =====================================================
    # VALIDATE RECOMMENDATIONS
    # =====================================================

    valid_recommendations = []

    for job in recommendations:

        if not isinstance(
            job,
            dict
        ):

            continue

        title = str(
            job.get(
                "title",
                ""
            )
        ).strip()

        company = str(
            job.get(
                "company",
                ""
            )
        ).strip()

        if not title:

            continue

        if not company:

            company = "Company not specified"

        job["company"] = company

        valid_recommendations.append(
            job
        )


    # =====================================================
    # REMOVE DUPLICATES
    # =====================================================

    unique_recommendations = []

    seen_jobs = set()

    for job in valid_recommendations:

        title = str(
            job.get(
                "title",
                ""
            )
        ).strip().lower()

        company = str(
            job.get(
                "company",
                ""
            )
        ).strip().lower()

        location = str(
            job.get(
                "location",
                ""
            )
        ).strip().lower()

        unique_key = (
            title,
            company,
            location
        )

        if unique_key in seen_jobs:

            continue

        seen_jobs.add(
            unique_key
        )

        unique_recommendations.append(
            job
        )


    # =====================================================
    # SORT BY RESUME MATCH
    # =====================================================

    def get_match_score(job):

        value = job.get(
            "resume_match",
            0
        )

        try:

            return float(
                value or 0
            )

        except (
            ValueError,
            TypeError
        ):

            return 0


    unique_recommendations.sort(
        key=get_match_score,
        reverse=True
    )


    recommendations = (
        unique_recommendations[:30]
    )


    # =====================================================
    # SEPARATE JOBS / INTERNSHIPS
    # =====================================================

    if opportunity_type == "internship":

        internships = recommendations

        job_recommendations = []

    else:

        job_recommendations = recommendations

        internships = []


    # =====================================================
    # DEBUG INFORMATION
    # =====================================================

    print(
        "Live results returned:",
        len(recommendations)
    )

    if recommendations:

        print(
            "Top result:",
            recommendations[0].get(
                "title",
                "Unknown"
            )
        )

        print(
            "Top resume match:",
            recommendations[0].get(
                "resume_match",
                0
            ),
            "%"
        )

    else:

        print(
            "No live opportunities returned."
        )

    print(
        "========================================\n"
    )


    # =====================================================
    # CLEAN TEMPORARY RESUME
    # =====================================================

    try:

        if os.path.exists(filepath):

            os.remove(
                filepath
            )

    except Exception as error:

        print(
            "Temporary file cleanup error:",
            error
        )


    # =====================================================
    # RESULT PAGE
    # =====================================================

    return render_template(

        "result.html",

        ats_score=ats_score,

        ats_details=ats_details,

        skills=skills,

        prediction=prediction,

        prediction_result=prediction_result,

        opportunity_type=opportunity_type,

        selected_opportunity=opportunity_type,

        recommendations=recommendations,

        job_recommendations=job_recommendations,

        internships=internships,

        live_jobs=job_recommendations,

        live_internships=internships,

        detected_urls=detected_urls,

        github_urls=github_urls,

        github_evidence=github_evidence,

        portfolio_urls=portfolio_urls,

        portfolio_evidence=portfolio_evidence,

        external_evidence=external_evidence

    )


# =========================================================
# MILO API
# =========================================================

@app.route(
    "/milo",
    methods=["POST"]
)
def milo():

    message = request.form.get(
        "message",
        ""
    ).strip()

    if not message:

        return {

            "success": False,

            "response": (
                "Please ask me about jobs, "
                "internships, companies, skills, "
                "your resume, salary, hiring, "
                "or applications."
            )

        }


    recommendations_data = request.form.get(
        "recommendations_data",
        ""
    )

    prediction_data = request.form.get(
        "prediction_data",
        ""
    )

    ats_score_data = request.form.get(
        "ats_score",
        ""
    )

    skills_data = request.form.get(
        "skills_data",
        ""
    )

    opportunity_type = request.form.get(
        "opportunity_type",
        "job"
    )


    try:

        recommendations = (
            json.loads(
                recommendations_data
            )
            if recommendations_data
            else []
        )

    except (
        json.JSONDecodeError,
        TypeError
    ):

        recommendations = []


    try:

        prediction_result = (
            json.loads(
                prediction_data
            )
            if prediction_data
            else {}
        )

    except (
        json.JSONDecodeError,
        TypeError
    ):

        prediction_result = {}


    try:

        skills = (
            json.loads(
                skills_data
            )
            if skills_data
            else []
        )

    except (
        json.JSONDecodeError,
        TypeError
    ):

        skills = []


    try:

        ats_score = (
            float(
                ats_score_data
            )
            if ats_score_data
            else None
        )

    except (
        ValueError,
        TypeError
    ):

        ats_score = None


    if opportunity_type not in [
        "job",
        "internship"
    ]:

        opportunity_type = "job"


    try:

        response = generate_milo_response(

            message=message,

            recommendations=recommendations,

            prediction_result=prediction_result,

            ats_score=ats_score,

            skills=skills

        )

    except Exception as error:

        print(
            "Milo error:",
            error
        )

        response = (
            "I couldn't process that question "
            "right now. Please ask me about jobs, "
            "internships, companies, skills, "
            "resume matching, salary, or applications."
        )


    return {

        "success": True,

        "response": response,

        "opportunity_type": opportunity_type

    }


# =========================================================
# START APPLICATION
# =========================================================

if __name__ == "__main__":

    app.run(
        debug=True
    )
