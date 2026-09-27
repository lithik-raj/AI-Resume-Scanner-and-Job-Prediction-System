import re

ALLOWED_KEYWORDS = [

    # Jobs
    "job",
    "jobs",
    "opening",
    "openings",
    "vacancy",
    "vacancies",
    "position",
    "positions",
    "role",
    "roles",

    # Internship
    "intern",
    "interns",
    "internship",
    "internships",

    # Companies
    "company",
    "companies",
    "employer",
    "employers",

    # Career
    "career",
    "career path",
    "career option",
    "career options",

    # Hiring
    "hiring",
    "hire",
    "hired",
    "recruiting",
    "recruitment",

    # Application
    "apply",
    "application",
    "applications",
    "applying",

    # Salary
    "salary",
    "stipend",
    "pay",
    "package",
    "ctc",
    "compensation",

    # Resume
    "resume",
    "cv",
    "ats",
    "profile",
    "experience",
    "qualification",
    "qualifications",
    "requirement",
    "requirements",
    "match",
    "matching",
    "fit",
    "suitable",
    "suit",

    # Skills
    "skill",
    "skills",
    "technology",
    "technologies",
    "technical",

    # Location / work mode
    "location",
    "where",
    "remote",
    "wfh",
    "work from home",
    "hybrid",
    "onsite",
    "on-site",

    # Projects / technical career
    "project",
    "projects",
    "python",
    "java",
    "javascript",
    "typescript",
    "sql",
    "machine learning",
    "ml",
    "deep learning",
    "ai",
    "artificial intelligence",
    "data science",
    "data scientist",
    "data analytics",
    "genai",
    "generative ai",
    "tensorflow",
    "pytorch",
    "nlp",
    "computer vision",
    "flask",
    "fastapi",
    "django",
    "react",
    "node",
    "mongodb",
    "mysql",
    "git",
    "github",
    "docker",
    "aws",
    "azure",
    "power bi",
    "tableau",
    "portfolio"

]


# =========================================================
# TEXT HELPERS
# =========================================================

def normalize_text(text):

    if not text:
        return ""

    text = str(text).lower().strip()

    text = re.sub(
        r"\s+",
        " ",
        text
    )

    return text


def contains_any(message, words):

    message = normalize_text(message)

    return any(
        word in message
        for word in words
    )


# =========================================================
# TOPIC VALIDATION
# =========================================================

def is_allowed_question(message):

    message = normalize_text(message)

    if not message:
        return False

    return any(
        keyword in message
        for keyword in ALLOWED_KEYWORDS
    )


# =========================================================
# SAFE RESUME HELPERS
# =========================================================

def get_role(prediction_result):

    if not isinstance(
        prediction_result,
        dict
    ):
        return "Not available"

    return (
        prediction_result.get("role")
        or prediction_result.get("prediction")
        or "Not available"
    )


def get_skills(skills):

    if not isinstance(
        skills,
        list
    ):
        return []

    result = []

    for skill in skills:

        value = str(
            skill
        ).strip()

        if value:

            result.append(
                value
            )

    return result


def get_score(ats_score):

    try:

        if ats_score is None:

            return "Not available"

        return f"{float(ats_score):.0f}%"

    except (
        ValueError,
        TypeError
    ):

        return "Not available"


# =========================================================
# JOB FIELD HELPERS
# =========================================================

def job_value(
    job,
    *keys,
    default="Not specified"
):

    if not isinstance(
        job,
        dict
    ):

        return default

    for key in keys:

        value = job.get(
            key
        )

        if (
            value is not None
            and str(value).strip()
        ):

            return str(
                value
            ).strip()

    return default


def job_title(job):

    return job_value(
        job,
        "title",
        "job_title",
        "position",
        "name",
        default="Job opportunity"
    )


def job_company(job):

    return job_value(
        job,
        "company",
        "company_name",
        "employer",
        default="Company not specified"
    )


def job_location(job):

    return job_value(
        job,
        "location",
        "locations",
        "place",
        "city",
        default="Location not specified"
    )


def job_salary(job):

    return job_value(
        job,
        "salary",
        "salary_min",
        "stipend",
        "pay",
        "salary_range",
        default="Not disclosed"
    )


def job_type(job):

    return job_value(
        job,
        "job_type",
        "type",
        "employment_type",
        default="Not specified"
    )


def job_description(job):

    return job_value(
        job,
        "description",
        "summary",
        "job_description",
        "details",
        default=""
    )


def job_apply_url(job):

    return job_value(
        job,
        "apply_url",
        "apply_link",
        "url",
        "link",
        default=""
    )


# =========================================================
# JOB SKILLS
# =========================================================

def job_skills(job):

    if not isinstance(
        job,
        dict
    ):

        return []

    fields = [

        "required_skills",
        "skills",
        "skill_requirements",
        "technologies",
        "requirements",
        "technical_skills"

    ]

    result = []

    for field in fields:

        value = job.get(
            field
        )

        if isinstance(
            value,
            list
        ):

            for item in value:

                item = str(
                    item
                ).strip()

                if item:

                    result.append(
                        item
                    )

        elif isinstance(
            value,
            str
        ):

            parts = re.split(
                r",|;|\||\n",
                value
            )

            for item in parts:

                item = item.strip()

                if item:

                    result.append(
                        item
                    )

    # Remove duplicates
    final = []

    seen = set()

    for item in result:

        key = item.lower()

        if key not in seen:

            seen.add(
                key
            )

            final.append(
                item
            )

    return final


# =========================================================
# KNOWN TECHNICAL SKILLS
# =========================================================

COMMON_SKILLS = [

    "python",
    "java",
    "javascript",
    "typescript",
    "sql",
    "machine learning",
    "deep learning",
    "artificial intelligence",
    "data science",
    "data analytics",
    "tensorflow",
    "pytorch",
    "flask",
    "fastapi",
    "django",
    "react",
    "node",
    "node.js",
    "mongodb",
    "mysql",
    "postgresql",
    "git",
    "github",
    "docker",
    "aws",
    "azure",
    "power bi",
    "tableau",
    "generative ai",
    "genai",
    "nlp",
    "computer vision",
    "llm",
    "langchain",
    "pandas",
    "numpy",
    "scikit-learn",
    "sklearn",
    "opencv",
    "html",
    "css",
    "rest api",
    "api"

]


# =========================================================
# SKILL MATCHING
# =========================================================

def skill_matches(
    resume_skill,
    required_skill
):

    resume_skill = normalize_text(
        resume_skill
    )

    required_skill = normalize_text(
        required_skill
    )

    if not resume_skill or not required_skill:

        return False

    # Exact match
    if resume_skill == required_skill:

        return True

    # Safe substring matching
    if (
        required_skill in resume_skill
        and len(required_skill) >= 3
    ):

        return True

    if (
        resume_skill in required_skill
        and len(resume_skill) >= 3
    ):

        return True

    # Common aliases
    aliases = {

        "ml": [
            "machine learning"
        ],

        "machine learning": [
            "ml"
        ],

        "ai": [
            "artificial intelligence"
        ],

        "artificial intelligence": [
            "ai"
        ],

        "genai": [
            "generative ai",
            "gen ai"
        ],

        "generative ai": [
            "genai",
            "gen ai"
        ],

        "sklearn": [
            "scikit-learn",
            "scikit learn"
        ],

        "scikit-learn": [
            "sklearn",
            "scikit learn"
        ],

        "node": [
            "node.js"
        ],

        "node.js": [
            "node"
        ]

    }

    if required_skill in aliases:

        for alias in aliases[
            required_skill
        ]:

            if alias in resume_skill:

                return True

    if resume_skill in aliases:

        for alias in aliases[
            resume_skill
        ]:

            if alias in required_skill:

                return True

    return False


# =========================================================
# JOB MATCH CALCULATION
# =========================================================

def calculate_job_match(
    job,
    skills
):

    resume_skills = get_skills(
        skills
    )

    description = normalize_text(
        job_description(job)
    )

    required = job_skills(
        job
    )

    matched = []
    missing = []

    # -----------------------------------------------------
    # Explicit API requirements
    # -----------------------------------------------------

    if required:

        for required_skill in required:

            found = False

            for resume_skill in resume_skills:

                if skill_matches(
                    resume_skill,
                    required_skill
                ):

                    found = True

                    break

            if found:

                matched.append(
                    required_skill
                )

            else:

                missing.append(
                    required_skill
                )

        score = (
            len(matched)
            / len(required)
        ) * 100

        return {

            "score": round(
                score
            ),

            "matched": matched,

            "missing": missing

        }

    # -----------------------------------------------------
    # API has no explicit skill field
    #
    # Compare resume skills with job description.
    # -----------------------------------------------------

    for resume_skill in resume_skills:

        resume_skill_lower = normalize_text(
            resume_skill
        )

        if len(
            resume_skill_lower
        ) < 2:

            continue

        if (
            resume_skill_lower
            in description
        ):

            matched.append(
                resume_skill
            )

    # Remove duplicate matches
    unique_matched = []

    seen = set()

    for item in matched:

        key = item.lower()

        if key not in seen:

            seen.add(
                key
            )

            unique_matched.append(
                item
            )

    matched = unique_matched

    if matched:

        score = min(
            len(matched) * 20,
            100
        )

    else:

        score = 0

    return {

        "score": round(
            score
        ),

        "matched": matched,

        "missing": []

    }


# =========================================================
# GET ALL JOB MATCHES
# =========================================================

def get_job_matches(
    recommendations,
    skills
):

    if not isinstance(
        recommendations,
        list
    ):

        return []

    results = []

    for job in recommendations:

        if not isinstance(
            job,
            dict
        ):

            continue

        match = calculate_job_match(
            job,
            skills
        )

        results.append({

            "job": job,

            "score": match[
                "score"
            ],

            "matched": match[
                "matched"
            ],

            "missing": match[
                "missing"
            ]

        })

    results.sort(
        key=lambda item: item[
            "score"
        ],
        reverse=True
    )

    return results


# =========================================================
# FORMAT JOB
# =========================================================

def format_job(
    job,
    match=None
):

    title = job_title(
        job
    )

    company = job_company(
        job
    )

    location = job_location(
        job
    )

    salary = job_salary(
        job
    )

    jobtype = job_type(
        job
    )

    response = (

        f"**{title}**\n"
        f"Company: {company}\n"
        f"Location: {location}\n"
        f"Salary/Stipend: {salary}\n"
        f"Job Type: {jobtype}"

    )

    if match is not None:

        response += (
            f"\nResume Match: "
            f"{match['score']}%"
        )

        if match[
            "matched"
        ]:

            response += (

                "\nMatching skills: "
                + ", ".join(
                    match[
                        "matched"
                    ][:10]
                )

            )

        if match[
            "missing"
        ]:

            response += (

                "\nPotential missing skills: "
                + ", ".join(
                    match[
                        "missing"
                    ][:8]
                )

            )

    return response


# =========================================================
# FIND INTERNSHIPS
# =========================================================

def get_internships(
    recommendations
):

    internships = []

    for job in recommendations:

        title = normalize_text(
            job_title(job)
        )

        jobtype = normalize_text(
            job_type(job)
        )

        description = normalize_text(
            job_description(job)
        )

        if (

            "intern" in title
            or "intern" in jobtype
            or "internship" in description

        ):

            internships.append(
                job
            )

    return internships


# =========================================================
# QUESTION INTENT DETECTION
# =========================================================

def is_suitability_question(
    message
):

    return contains_any(
        message,
        [

            "which job suits me",
            "which job suit me",
            "which job is suitable",
            "what job suits me",
            "what job should i choose",
            "which job should i choose",
            "which one should i choose",
            "what should i choose",
            "which job is best for me",
            "what job is best for me",
            "best job for me",
            "best job for my resume",
            "job for my resume",
            "job matches my resume",
            "job match my resume",
            "which job matches me",
            "which job fits me",
            "what job fits me",
            "which opportunity suits me",
            "which opportunity fits me",
            "which opportunity is suitable",
            "which role suits me",
            "which role fits me",
            "what role suits me",
            "career option for me",
            "career options for me",
            "which career should i choose",
            "what should i apply for",
            "what should i apply",
            "which should i apply",
            "where should i apply"

        ]
    )


def is_missing_skill_question(
    message
):

    return contains_any(
        message,
        [

            "missing skill",
            "missing skills",
            "skills missing",
            "what skill am i missing",
            "what skills am i missing",
            "what should i learn",
            "what should i learn for this job",
            "what skills should i learn",
            "what skills do i need",
            "skills do i need",
            "which skills should i improve",
            "what should i improve"

        ]
    )


def is_resume_question(
    message
):

    return contains_any(
        message,
        [

            "my resume",
            "my cv",
            "resume score",
            "cv score",
            "resume match",
            "resume matching",
            "ats",
            "ats score",
            "resume skills",
            "resume analysis"

        ]
    )


def is_skill_question(
    message
):

    return contains_any(
        message,
        [

            "my skills",
            "what skills do i have",
            "what skills i have",
            "skills on my resume",
            "skills in my resume",
            "what are my skills",
            "show my skills",
            "list my skills"

        ]
    )


def is_role_question(
    message
):

    return contains_any(
        message,
        [

            "predicted role",
            "what role am i",
            "which role am i",
            "my role",
            "what is my role",
            "which role fits",
            "role prediction"

        ]
    )


# =========================================================
# MILO RESPONSE ENGINE
# =========================================================

def generate_milo_response(
    message,
    recommendations=None,
    prediction_result=None,
    ats_score=None,
    skills=None
):

    message = normalize_text(
        message
    )

    recommendations = (
        recommendations
        if isinstance(
            recommendations,
            list
        )
        else []
    )

    prediction_result = (
        prediction_result
        if isinstance(
            prediction_result,
            dict
        )
        else {}
    )

    skills = get_skills(
        skills
    )

    predicted_role = get_role(
        prediction_result
    )

    ats_text = get_score(
        ats_score
    )

    # =====================================================
    # EMPTY QUESTION
    # =====================================================

    if not message:

        return (

            "Please ask me about jobs, internships, "
            "companies, skills, your resume, ATS score, "
            "salary, hiring, or applications."

        )

    # =====================================================
    # TOPIC FILTER
    # =====================================================

    if not is_allowed_question(
        message
    ):

        return (

            "I'm Milo, your job and internship "
            "assistant. I can answer only questions "
            "about jobs, internships, companies, "
            "skills, resumes, applications, salaries, "
            "hiring, and career opportunities."

        )

    # =====================================================
    # CURRENT LIVE MATCHES
    # =====================================================

    matches = get_job_matches(
        recommendations,
        skills
    )

    # =====================================================
    # WHICH JOB SHOULD I CHOOSE?
    # =====================================================

    if is_suitability_question(
        message
    ):

        if not matches:

            return (

                f"Your predicted role is "
                f"{predicted_role} and your ATS score "
                f"is {ats_text}.\n\n"

                "I don't currently have live job "
                "results to compare with your resume. "
                "Please run the resume analysis again "
                "or check whether the job API returned "
                "results."

            )

        best = matches[0]

        job = best[
            "job"
        ]

        response = (

            "Based on your current resume skills "
            "and the live job results, this listing "
            "has the highest calculated skill match "
            "among the returned jobs.\n\n"

        )

        response += format_job(
            job,
            best
        )

        response += (

            "\n\nWhy this match:\n"
            f"Predicted role: {predicted_role}\n"
            f"ATS score: {ats_text}\n"

        )

        if best[
            "matched"
        ]:

            response += (

                "Matching skills: "
                + ", ".join(
                    best[
                        "matched"
                    ][:10]
                )
                + "\n"

            )

        if best[
            "missing"
        ]:

            response += (

                "Skills to check: "
                + ", ".join(
                    best[
                        "missing"
                    ][:8]
                )

            )

        return response

    # =====================================================
    # INTERNSHIP QUESTIONS
    # =====================================================

    if contains_any(
        message,
        [

            "internship",
            "internships",
            "intern",
            "student internship"

        ]
    ):

        internships = get_internships(
            recommendations
        )

        internship_matches = get_job_matches(
            internships,
            skills
        )

        if not internship_matches:

            return (

                "I couldn't find a matching internship "
                "in the current live job results."

            )

        response = (

            "Current internship opportunities "
            "from the live results:\n\n"

        )

        for item in internship_matches[:5]:

            response += (

                format_job(
                    item[
                        "job"
                    ],
                    item
                )

                + "\n\n"

            )

        return response.strip()

    # =====================================================
    # MISSING SKILLS
    # =====================================================

    if is_missing_skill_question(
        message
    ):

        if not matches:

            return (

                "I need current live job results "
                "to compare your resume with job "
                "requirements and identify missing skills."

            )

        # Use the highest matching job
        best = matches[0]

        if best[
            "missing"
        ]:

            return (

                "Based on the strongest current "
                "job match, these required skills "
                "were not found in your resume:\n\n"

                + ", ".join(
                    best[
                        "missing"
                    ][:15]
                )

                + "\n\n"

                "These are areas you can consider "
                "learning or strengthening."

            )

        return (

            "The strongest current job match does "
            "not show additional missing skills from "
            "the available job requirements."

        )

    # =====================================================
    # RESUME / ATS
    # =====================================================

    if is_resume_question(
        message
    ):

        return (

            f"Predicted Role: {predicted_role}\n\n"

            f"ATS Score: {ats_text}\n\n"

            "Detected Skills:\n"

            + (

                ", ".join(
                    skills[:30]
                )

                if skills

                else "No skills detected"

            )

        )

    # =====================================================
    # SKILLS
    # =====================================================

    if is_skill_question(
        message
    ):

        if not skills:

            return (

                "No technical skills were detected "
                "from your current resume."

            )

        return (

            "Skills detected from your resume:\n\n"

            + ", ".join(
                skills[:30]
            )

        )

    # =====================================================
    # ROLE
    # =====================================================

    if is_role_question(
        message
    ):

        return (

            "Based on the current resume analysis, "
            f"your predicted role is **{predicted_role}**."

        )

    # =====================================================
    # COMPANY QUESTIONS
    # =====================================================

    if contains_any(
        message,
        [

            "company",
            "companies",
            "employer",
            "employers",
            "who is hiring"

        ]
    ):

        if not recommendations:

            return (

                "There are no current company results "
                "available from the live job search."

            )

        companies = []

        for job in recommendations:

            company = job_company(
                job
            )

            if (

                company
                not in companies
                and company != "Company not specified"

            ):

                companies.append(
                    company
                )

        if not companies:

            return (

                "Company information is not available "
                "in the current live listings."

            )

        return (

            "Companies appearing in the current "
            "live job results:\n\n"

            + "\n".join(
                companies[:10]
            )

        )

    # =====================================================
    # SALARY / STIPEND
    # =====================================================

    if contains_any(
        message,
        [

            "salary",
            "stipend",
            "pay",
            "package",
            "ctc",
            "compensation"

        ]
    ):

        if not matches:

            return (

                "Salary or stipend information is not "
                "available because there are no current "
                "job results."

            )

        lines = []

        for item in matches[:6]:

            lines.append(

                f"{job_title(item['job'])} — "
                f"{job_company(item['job'])} — "
                f"{job_salary(item['job'])}"

            )

        return (

            "Salary/stipend information from the "
            "current live listings:\n\n"

            + "\n".join(
                lines
            )

        )

    # =====================================================
    # LOCATION / WORK MODE
    # =====================================================

    if contains_any(
        message,
        [

            "location",
            "where",
            "remote",
            "wfh",
            "work from home",
            "hybrid",
            "onsite",
            "on-site"

        ]
    ):

        if not matches:

            return (

                "No current job listings are available "
                "to provide location or work-mode details."

            )

        lines = []

        for item in matches[:6]:

            job = item[
                "job"
            ]

            lines.append(

                f"{job_title(job)} — "
                f"{job_location(job)} — "
                f"{job_type(job)}"

            )

        return (

            "Location and work information from "
            "the current live listings:\n\n"

            + "\n".join(
                lines
            )

        )

    # =====================================================
    # APPLICATION QUESTIONS
    # =====================================================

    if contains_any(
        message,
        [

            "apply",
            "application",
            "application link",
            "apply link",
            "how to apply",
            "where to apply"

        ]
    ):

        if not matches:

            return (

                "There are currently no job listings "
                "with application information available."

            )

        lines = []

        for item in matches[:6]:

            job = item[
                "job"
            ]

            url = job_apply_url(
                job
            )

            if url and url != "#":

                lines.append(

                    f"{job_title(job)} — "
                    f"{job_company(job)}\n"
                    f"Apply: {url}"

                )

        if lines:

            return (

                "Application links from the "
                "current live job results:\n\n"

                + "\n\n".join(
                    lines
                )

            )

        return (

            "The current job results do not contain "
            "a direct application link."

        )

    # =====================================================
    # GENERAL JOB QUESTIONS
    # =====================================================

    if contains_any(
        message,
        [

            "job",
            "jobs",
            "opening",
            "openings",
            "vacancy",
            "vacancies",
            "hiring"

        ]
    ):

        if not matches:

            return (

                f"No current live jobs were returned "
                f"for comparison with your predicted "
                f"role ({predicted_role})."

            )

        response = (

            "Current live jobs matching your "
            "resume skills:\n\n"

        )

        for item in matches[:6]:

            response += (

                format_job(
                    item[
                        "job"
                    ],
                    item
                )

                + "\n\n"

            )

        return response.strip()

    # =====================================================
    # GENERAL CAREER RESPONSE
    # =====================================================

    return (

        f"Your current predicted role is "
        f"{predicted_role} and your ATS score is "
        f"{ats_text}.\n\n"

        f"I currently have "
        f"{len(recommendations)} live job result(s) "
        "available for comparison.\n\n"

        "You can ask me:\n"
        "• Which job suits my resume?\n"
        "• Which internship matches my skills?\n"
        "• What skills am I missing?\n"
        "• What salary or stipend is offered?\n"
        "• Which companies are hiring?\n"
        "• Where are the jobs located?\n"
        "• Is the job remote or hybrid?\n"
        "• How can I apply?"

    )
