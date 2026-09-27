import os
import re
import requests
from urllib.parse import quote

from dotenv import load_dotenv


# =========================================================
# LOAD ENVIRONMENT VARIABLES
# =========================================================

load_dotenv()

APP_ID = os.getenv("ADZUNA_APP_ID")
APP_KEY = os.getenv("ADZUNA_APP_KEY")


# =========================================================
# ADZUNA CONFIGURATION
# =========================================================

ADZUNA_URL = (
    "https://api.adzuna.com/"
    "v1/api/jobs/in/search"
)

DEFAULT_LOCATION = "Bangalore"


# =========================================================
# COMPANY LOGO
# =========================================================

def get_company_logo(company):
    """
    Generate a company logo URL from the company name.
    Uses Google's favicon service.
    """

    company = str(company or "").strip()

    if not company:
        return ""

    # Remove common company suffixes
    clean_name = re.sub(
        r"\b(private limited|pvt ltd|pvt\. ltd\.|"
        r"limited|ltd|llp|inc|incorporated|corp|"
        r"corporation|technologies|technology|"
        r"solutions|services|group)\b",
        "",
        company,
        flags=re.IGNORECASE
    )

    clean_name = re.sub(
        r"[^a-zA-Z0-9\s]",
        " ",
        clean_name
    )

    clean_name = re.sub(
        r"\s+",
        " ",
        clean_name
    ).strip()

    if not clean_name:
        clean_name = company

    words = clean_name.lower().split()

    if not words:
        return ""

    # Try the most common company-domain patterns
    domain_candidates = []

    joined = "".join(words)
    dotted = ".".join(words)

    domain_candidates.append(
        f"{joined}.com"
    )

    domain_candidates.append(
        f"{joined}.in"
    )

    domain_candidates.append(
        f"{dotted}.com"
    )

    domain_candidates.append(
        f"{joined}.co.in"
    )

    # Special handling for known common companies
    known_domains = {
        "accenture": "accenture.com",
        "amazon": "amazon.com",
        "microsoft": "microsoft.com",
        "google": "google.com",
        "ibm": "ibm.com",
        "oracle": "oracle.com",
        "infosys": "infosys.com",
        "wipro": "wipro.com",
        "tcs": "tcs.com",
        "tata consultancy services": "tcs.com",
        "cognizant": "cognizant.com",
        "capgemini": "capgemini.com",
        "deloitte": "deloitte.com",
        "ey": "ey.com",
        "pwc": "pwc.com",
        "kpmg": "kpmg.com",
        "hcl": "hcltech.com",
        "hcl technologies": "hcltech.com",
        "tech mahindra": "techmahindra.com",
        "mistral ai": "mistral.ai",
        "openai": "openai.com",
        "nvidia": "nvidia.com",
        "intel": "intel.com",
        "meta": "meta.com",
        "apple": "apple.com",
        "netflix": "netflix.com",
        "uber": "uber.com",
        "ola": "olacabs.com",
        "flipkart": "flipkart.com",
        "swiggy": "swiggy.com",
        "zomato": "zomato.com",
        "phonepe": "phonepe.com",
        "paytm": "paytm.com",
        "razorpay": "razorpay.com",
        "walmart": "walmart.com",
        "salesforce": "salesforce.com",
        "adobe": "adobe.com",
        "sap": "sap.com",
        "siemens": "siemens.com",
        "bosch": "bosch.com",
        "volvo": "volvocars.com",
        "toyota": "toyota.com",
        "hp": "hp.com",
        "dell": "dell.com",
        "qualcomm": "qualcomm.com",
        "samsung": "samsung.com",
        "linkedin": "linkedin.com",
        "github": "github.com",
        "gitlab": "gitlab.com",
        "accenture plc": "accenture.com",
    }

    normalized_company = re.sub(
        r"\s+",
        " ",
        company.lower()
    ).strip()

    domain = known_domains.get(
        normalized_company
    )

    if not domain:
        domain = domain_candidates[0]

    return (
        "https://www.google.com/"
        "s2/favicons"
        f"?domain={quote(domain)}"
        "&sz=128"
    )


# =========================================================
# ROLE → SEARCH KEYWORD
# =========================================================

def get_search_keyword(role, opportunity_type="job"):

    role = str(role or "").strip()

    role_keywords = {

        "Data Scientist": "data scientist",
        "Web Developer": "web developer",
        "Java Developer": "java developer",
        "Machine Learning Engineer": "machine learning engineer",
        "AI Engineer": "AI engineer",
        "Data Analyst": "data analyst",
        "Frontend Developer": "frontend developer",
        "Backend Developer": "backend developer",
        "React Developer": "react developer",
        "Spring Boot Developer": "spring boot developer",
        "Software Developer": "software developer",
        "Software Engineer": "software engineer",
        "Python Developer": "python developer",
        "Data Engineer": "data engineer",
        "ML Engineer": "machine learning engineer",
        "AI/ML Engineer": "AI machine learning engineer"

    }

    keyword = role_keywords.get(role, role)

    if not keyword:
        keyword = "technology"

    opportunity_type = str(
        opportunity_type or "job"
    ).lower().strip()

    if opportunity_type in (
        "intern",
        "internship",
        "internships"
    ):

        if "intern" not in keyword.lower():

            keyword = keyword + " internship"

    return keyword


# =========================================================
# CLEAN DESCRIPTION
# =========================================================

def clean_description(description, max_length=1200):

    if not description:
        return "No job description available."

    description = re.sub(
        r"\s+",
        " ",
        str(description)
    ).strip()

    if len(description) > max_length:

        description = (
            description[:max_length]
            .rsplit(" ", 1)[0]
            + "..."
        )

    return description


# =========================================================
# SALARY / STIPEND
# =========================================================

def format_salary(job):

    salary_min = job.get("salary_min")
    salary_max = job.get("salary_max")

    predicted = job.get(
        "salary_is_predicted",
        0
    )

    try:
        salary_min = (
            float(salary_min)
            if salary_min is not None
            else None
        )
    except (ValueError, TypeError):
        salary_min = None

    try:
        salary_max = (
            float(salary_max)
            if salary_max is not None
            else None
        )
    except (ValueError, TypeError):
        salary_max = None

    if salary_min is not None and salary_max is not None:

        salary = (
            f"₹{salary_min:,.0f} – "
            f"₹{salary_max:,.0f}"
        )

    elif salary_min is not None:

        salary = f"From ₹{salary_min:,.0f}"

    elif salary_max is not None:

        salary = f"Up to ₹{salary_max:,.0f}"

    else:

        salary = "Salary/Stipend not disclosed"

    if str(predicted).lower() in (
        "1",
        "true",
        "yes"
    ):

        salary += " (estimated)"

    return salary


# =========================================================
# JOB TYPE
# =========================================================

def format_job_type(job):

    contract_time = job.get("contract_time")
    contract_type = job.get("contract_type")

    values = []

    if contract_time:

        values.append(
            str(contract_time)
            .replace("_", " ")
            .title()
        )

    if contract_type:

        values.append(
            str(contract_type)
            .replace("_", " ")
            .title()
        )

    if values:

        return " • ".join(values)

    return "Not specified"


# =========================================================
# NORMALIZE SKILL
# =========================================================

def normalize_skill(skill):

    skill = str(
        skill or ""
    ).lower().strip()

    skill = re.sub(
        r"[^a-z0-9+#.\- ]",
        " ",
        skill
    )

    skill = re.sub(
        r"\s+",
        " ",
        skill
    )

    return skill.strip()


# =========================================================
# KNOWN TECHNICAL SKILLS
# =========================================================

KNOWN_SKILLS = [

    "python",
    "java",
    "javascript",
    "typescript",
    "c++",
    "c#",

    "sql",
    "mysql",
    "postgresql",
    "mongodb",

    "machine learning",
    "deep learning",
    "artificial intelligence",

    "data science",
    "data analytics",
    "data analysis",

    "pandas",
    "numpy",
    "scikit-learn",
    "sklearn",

    "tensorflow",
    "pytorch",
    "keras",

    "flask",
    "fastapi",
    "django",

    "html",
    "css",
    "react",
    "react.js",
    "node",
    "node.js",

    "spring boot",

    "git",
    "github",
    "docker",

    "aws",
    "azure",
    "gcp",

    "power bi",
    "tableau",
    "excel",

    "nlp",
    "natural language processing",

    "computer vision",

    "generative ai",
    "genai",
    "llm",
    "large language model",

    "langchain",
    "hugging face",

    "rest api",
    "api",

    "linux",

    "matplotlib",
    "seaborn",

    "spark",
    "hadoop"

]


# =========================================================
# SKILL ALIASES
# =========================================================

SKILL_ALIASES = {

    "sklearn": "scikit-learn",
    "scikit learn": "scikit-learn",
    "react.js": "react",
    "node.js": "node",
    "genai": "generative ai",
    "natural language processing": "nlp"

}


# =========================================================
# REMOVE DUPLICATES
# =========================================================

def remove_duplicate_skills(skills):

    result = []

    for skill in skills:

        normalized = normalize_skill(skill)

        if (
            normalized
            and normalized not in result
        ):

            result.append(normalized)

    return result


# =========================================================
# EXTRACT RESUME SKILLS
# =========================================================

def extract_resume_keywords(resume_text=""):

    if not resume_text:
        return []

    text = normalize_skill(resume_text)

    found = []

    for skill in KNOWN_SKILLS:

        normalized = normalize_skill(skill)

        if not normalized:
            continue

        pattern = (
            r"(?<![a-z0-9])"
            + re.escape(normalized)
            + r"(?![a-z0-9])"
        )

        if re.search(pattern, text):

            alias = SKILL_ALIASES.get(
                normalized,
                normalized
            )

            found.append(alias)

    return remove_duplicate_skills(found)


# =========================================================
# NORMALIZE PROVIDED SKILLS
# =========================================================

def normalize_resume_skills(skills):

    if not isinstance(skills, list):
        return []

    result = []

    for skill in skills:

        normalized = normalize_skill(skill)

        if not normalized:
            continue

        alias = SKILL_ALIASES.get(
            normalized
        )

        if alias:
            normalized = alias

        if normalized not in result:
            result.append(normalized)

    return result


# =========================================================
# EXTRACT JOB SKILLS
# =========================================================

def extract_job_skills(description=""):

    if not description:
        return []

    text = normalize_skill(description)

    found = []

    for skill in KNOWN_SKILLS:

        normalized = normalize_skill(skill)

        if not normalized:
            continue

        pattern = (
            r"(?<![a-z0-9])"
            + re.escape(normalized)
            + r"(?![a-z0-9])"
        )

        if re.search(pattern, text):

            alias = SKILL_ALIASES.get(
                normalized,
                normalized
            )

            found.append(alias)

    return remove_duplicate_skills(found)


# =========================================================
# RESUME ↔ JOB MATCH
# =========================================================

# =========================================================
# RESUME ↔ JOB MATCH
# =========================================================

def calculate_resume_match(
    resume_keywords,
    job_description,
    job_title=""
):

    resume_keywords = normalize_resume_skills(
        resume_keywords
    )

    job_title = str(
        job_title or ""
    ).strip()

    job_description = str(
        job_description or ""
    ).strip()

    combined_text = normalize_skill(
        job_title
        + " "
        + job_description
    )

    if not combined_text:
        return {
            "score": 0,
            "matched_skills": [],
            "missing_skills": []
        }

    job_skills = extract_job_skills(
        combined_text
    )

    matched = []
    missing = []

    # -----------------------------------------------------
    # SKILL MATCHING
    # -----------------------------------------------------

    for job_skill in job_skills:

        found = False

        for resume_skill in resume_keywords:

            if (
                job_skill == resume_skill
                or job_skill in resume_skill
                or resume_skill in job_skill
            ):
                found = True
                break

        if found:
            matched.append(job_skill)
        else:
            missing.append(job_skill)

    # -----------------------------------------------------
    # SKILL COVERAGE
    # -----------------------------------------------------

    if job_skills:

        skill_coverage = (
            len(matched)
            / len(job_skills)
        ) * 100

    else:

        skill_coverage = 0

    # -----------------------------------------------------
    # TITLE RELEVANCE
    # -----------------------------------------------------

    title_text = normalize_skill(
        job_title
    )

    title_matches = 0

    for resume_skill in resume_keywords:

        if (
            resume_skill
            and resume_skill in title_text
        ):
            title_matches += 1

    if resume_keywords:

        title_relevance = (
            title_matches
            / min(len(resume_keywords), 5)
        ) * 100

    else:

        title_relevance = 0

    title_relevance = min(
        title_relevance,
        100
    )

    # -----------------------------------------------------
    # RESUME SKILLS PRESENT IN JOB DESCRIPTION
    # -----------------------------------------------------

    resume_skill_matches = 0

    for resume_skill in resume_keywords:

        if (
            resume_skill
            and resume_skill in combined_text
        ):
            resume_skill_matches += 1

    if resume_keywords:

        resume_relevance = (
            resume_skill_matches
            / len(resume_keywords)
        ) * 100

    else:

        resume_relevance = 0

    resume_relevance = min(
        resume_relevance,
        100
    )

    # -----------------------------------------------------
    # REQUIRED SKILL PENALTY
    # -----------------------------------------------------

    if job_skills:

        missing_ratio = (
            len(missing)
            / len(job_skills)
        )

    else:

        missing_ratio = 0

    missing_penalty = (
        missing_ratio * 20
    )

    # -----------------------------------------------------
    # TITLE MISMATCH PENALTY
    # -----------------------------------------------------

    title_lower = title_text

    role_indicators = [
        "machine learning",
        "data scientist",
        "data analyst",
        "data engineer",
        "ai engineer",
        "software engineer",
        "software developer",
        "python developer",
        "java developer",
        "web developer",
        "frontend developer",
        "backend developer",
        "react developer",
        "ml engineer"
    ]

    detected_role = None

    for role in role_indicators:

        if role in title_lower:
            detected_role = role
            break

    role_penalty = 0

    if detected_role:

        related = False

        for resume_skill in resume_keywords:

            if (
                resume_skill in detected_role
                or detected_role in resume_skill
            ):
                related = True
                break

        if not related:

            role_groups = {

                "machine learning": [
                    "machine learning",
                    "deep learning",
                    "python",
                    "tensorflow",
                    "pytorch",
                    "scikit-learn",
                    "generative ai",
                    "nlp"
                ],

                "data scientist": [
                    "python",
                    "data science",
                    "machine learning",
                    "pandas",
                    "numpy",
                    "scikit-learn"
                ],

                "data analyst": [
                    "python",
                    "sql",
                    "excel",
                    "power bi",
                    "tableau",
                    "data analytics",
                    "data analysis"
                ],

                "data engineer": [
                    "python",
                    "sql",
                    "spark",
                    "hadoop",
                    "aws",
                    "azure",
                    "gcp"
                ],

                "ai engineer": [
                    "python",
                    "machine learning",
                    "deep learning",
                    "generative ai",
                    "llm",
                    "tensorflow",
                    "pytorch"
                ],

                "software engineer": [
                    "python",
                    "java",
                    "javascript",
                    "c++",
                    "c#",
                    "git"
                ],

                "software developer": [
                    "python",
                    "java",
                    "javascript",
                    "c++",
                    "c#",
                    "git"
                ],

                "python developer": [
                    "python",
                    "flask",
                    "fastapi",
                    "django"
                ],

                "java developer": [
                    "java",
                    "spring boot"
                ],

                "web developer": [
                    "html",
                    "css",
                    "javascript",
                    "react",
                    "node"
                ],

                "frontend developer": [
                    "html",
                    "css",
                    "javascript",
                    "react",
                    "typescript"
                ],

                "backend developer": [
                    "python",
                    "java",
                    "node",
                    "flask",
                    "fastapi",
                    "django",
                    "spring boot",
                    "sql"
                ],

                "react developer": [
                    "react",
                    "javascript",
                    "typescript",
                    "html",
                    "css"
                ],

                "ml engineer": [
                    "machine learning",
                    "python",
                    "deep learning",
                    "tensorflow",
                    "pytorch",
                    "scikit-learn"
                ]
            }

            expected_skills = role_groups.get(
                detected_role,
                []
            )

            role_matches = sum(
                1
                for skill in expected_skills
                if skill in resume_keywords
            )

            if expected_skills:

                role_alignment = (
                    role_matches
                    / len(expected_skills)
                ) * 100

                if role_alignment < 20:
                    role_penalty = 15

                elif role_alignment < 40:
                    role_penalty = 8

    # -----------------------------------------------------
    # FINAL REALISTIC SCORE
    # -----------------------------------------------------

    if job_skills:

        score = (
            (skill_coverage * 0.60)
            + (resume_relevance * 0.25)
            + (title_relevance * 0.15)
        )

    else:

        score = (
            (resume_relevance * 0.65)
            + (title_relevance * 0.35)
        )

    score -= missing_penalty
    score -= role_penalty

    # -----------------------------------------------------
    # REALISTIC SCORE LIMITS
    # -----------------------------------------------------

    score = min(
        max(score, 0),
        100
    )

    # Avoid unrealistic 100% matches.
    # A job recommendation should almost never
    # appear as a perfect match.

    if score >= 95:
        score = 94

    elif score >= 90:
        score = min(
            score,
            89
        )

    return {

        "score": round(
            score,
            2
        ),

        "matched_skills": matched,

        "missing_skills": missing

    }


# =========================================================
# INTERNSHIP DETECTION
# =========================================================

def is_internship(job):

    if not isinstance(job, dict):
        return False

    title = str(
        job.get("title", "")
    ).lower()

    description = str(
        job.get("description", "")
    ).lower()

    contract_type = str(
        job.get("contract_type", "")
    ).lower()

    contract_time = str(
        job.get("contract_time", "")
    ).lower()

    combined = (
        title
        + " "
        + description
        + " "
        + contract_type
        + " "
        + contract_time
    )

    internship_words = [
        "intern",
        "internship",
        "trainee",
        "student placement",
        "graduate internship"
    ]

    return any(
        word in combined
        for word in internship_words
    )


# =========================================================
# REGULAR JOB
# =========================================================

def is_regular_job(job):

    return not is_internship(job)


# =========================================================
# SELECTION CHANCE
# =========================================================

def calculate_selection_chance(
    resume_match,
    job
):

    match = float(
        resume_match.get(
            "score",
            0
        ) or 0
    )

    matched_count = len(
        resume_match.get(
            "matched_skills",
            []
        )
    )

    missing_count = len(
        resume_match.get(
            "missing_skills",
            []
        )
    )

    total_skills = (
        matched_count
        + missing_count
    )

    if total_skills > 0:

        skill_factor = (
            matched_count
            / total_skills
        ) * 100

    else:

        skill_factor = match

    chance = (
        (match * 0.70)
        + (skill_factor * 0.30)
    )

    chance = round(
        min(max(chance, 0), 100),
        2
    )

    if chance >= 80:
        label = "High Match"
    elif chance >= 60:
        label = "Good Match"
    elif chance >= 40:
        label = "Moderate Match"
    else:
        label = "Low Match"

    return {
        "score": chance,
        "label": label
    }


# =========================================================
# FORMAT ADZUNA JOB
# =========================================================

def format_job(
    job,
    resume_match,
    opportunity_type
):

    company_data = job.get(
        "company",
        {}
    )

    if isinstance(company_data, dict):

        company = company_data.get(
            "display_name",
            "Company not specified"
        )

    else:

        company = str(company_data)

    company = str(company).strip()

    location_data = job.get(
        "location",
        {}
    )

    if isinstance(location_data, dict):

        location = location_data.get(
            "display_name",
            DEFAULT_LOCATION
        )

    else:

        location = str(location_data)

    title = job.get(
        "title",
        "Opportunity"
    )

    description = clean_description(
        job.get(
            "description",
            ""
        )
    )

    required_skills = extract_job_skills(
        description
    )

    selection = calculate_selection_chance(
        resume_match,
        job
    )

    return {

        "id": job.get(
            "id",
            ""
        ),

        "title": str(title).strip(),

        "company": company,

        "logo": get_company_logo(
            company
        ),

        "location": str(location).strip(),

        "salary": format_salary(job),

        "job_type": format_job_type(job),

        "description": description,

        "created": job.get(
            "created",
            ""
        ),

        "apply_url": job.get(
            "redirect_url",
            "#"
        ),

        "category": (
            job.get(
                "category",
                {}
            ).get(
                "label",
                "Technology"
            )
            if isinstance(
                job.get(
                    "category",
                    {}
                ),
                dict
            )
            else "Technology"
        ),

        "opportunity_type": opportunity_type,

        "resume_match": resume_match["score"],

        "matched_skills": resume_match[
            "matched_skills"
        ],

        "missing_skills": resume_match[
            "missing_skills"
        ],

        "required_skills": required_skills,

        "selection_chance": selection["score"],

        "selection_chance_label": selection["label"]

    }


# =========================================================
# FETCH ADZUNA PAGE
# =========================================================

def fetch_adzuna_page(
    keyword,
    page=1,
    results_per_page=20,
    location=DEFAULT_LOCATION
):

    if not APP_ID or not APP_KEY:

        print(
            "Adzuna API credentials missing."
        )

        return []

    url = (
        ADZUNA_URL
        + f"/{page}"
    )

    params = {

        "app_id": APP_ID,

        "app_key": APP_KEY,

        "results_per_page":
            results_per_page,

        "what": keyword,

        "where": location,

        "sort_by": "date",

        "content-type":
            "application/json"

    }

    try:

        response = requests.get(
            url,
            params=params,
            timeout=20
        )

        if response.status_code != 200:

            print(
                "Adzuna API error:",
                response.status_code
            )

            return []

        data = response.json()

        if not isinstance(data, dict):
            return []

        return data.get(
            "results",
            []
        )

    except (
        requests.RequestException,
        ValueError
    ) as error:

        print(
            "Adzuna connection error:",
            error
        )

        return []


# =========================================================
# MAIN RECOMMENDATION FUNCTION
# =========================================================

def recommend_jobs(
    role,
    opportunity_type="job",
    resume_text="",
    skills=None
):

    opportunity_type = str(
        opportunity_type or "job"
    ).lower().strip()

    if opportunity_type in (
        "intern",
        "internship",
        "internships"
    ):

        opportunity_type = "internship"

    else:

        opportunity_type = "job"

    if not APP_ID or not APP_KEY:

        print(
            "ERROR: ADZUNA_APP_ID or "
            "ADZUNA_APP_KEY is missing."
        )

        return []

    resume_keywords = normalize_resume_skills(
        skills
    )

    text_skills = extract_resume_keywords(
        resume_text
    )

    resume_keywords = remove_duplicate_skills(
        resume_keywords + text_skills
    )

    keyword = get_search_keyword(
        role,
        opportunity_type
    )

    print(
        f"Searching Adzuna: "
        f"{keyword} | "
        f"{opportunity_type} | "
        f"{DEFAULT_LOCATION}"
    )

    raw_jobs = []

    for page in range(1, 3):

        page_results = fetch_adzuna_page(
            keyword=keyword,
            page=page,
            results_per_page=20,
            location=DEFAULT_LOCATION
        )

        raw_jobs.extend(page_results)

        if len(page_results) < 20:
            break

    # -----------------------------------------------------
    # INTERNSHIP FALLBACK
    # -----------------------------------------------------

    if (
        opportunity_type == "internship"
        and not raw_jobs
    ):

        fallback_keyword = (
            str(role or "AI ML")
            + " intern"
        )

        raw_jobs = fetch_adzuna_page(
            keyword=fallback_keyword,
            page=1,
            results_per_page=20,
            location=DEFAULT_LOCATION
        )

    # -----------------------------------------------------
    # REMOVE DUPLICATES
    # -----------------------------------------------------

    unique_jobs = {}

    for job in raw_jobs:

        if not isinstance(job, dict):
            continue

        job_id = str(
            job.get("id", "")
        ).strip()

        redirect_url = str(
            job.get("redirect_url", "")
        ).strip()

        title = str(
            job.get("title", "")
        ).strip().lower()

        company_data = job.get(
            "company",
            {}
        )

        if isinstance(company_data, dict):

            company = str(
                company_data.get(
                    "display_name",
                    ""
                )
            ).strip().lower()

        else:

            company = str(
                company_data
            ).strip().lower()

        unique_key = (
            job_id
            or redirect_url
            or (
                title
                + "|"
                + company
            )
        )

        if unique_key:

            unique_jobs[
                unique_key
            ] = job

    raw_jobs = list(
        unique_jobs.values()
    )

    # -----------------------------------------------------
    # FILTER JOB / INTERNSHIP
    # -----------------------------------------------------

    filtered_jobs = []

    for job in raw_jobs:

        if opportunity_type == "internship":

            if is_internship(job):

                filtered_jobs.append(job)

        else:

            if is_regular_job(job):

                filtered_jobs.append(job)

    # -----------------------------------------------------
    # INTERNSHIP SECOND SEARCH
    # -----------------------------------------------------

    if (
        opportunity_type == "internship"
        and not filtered_jobs
    ):

        fallback_keywords = [

            f"{role} intern",

            f"{role} internship",

            "AI ML intern",

            "machine learning intern",

            "data science intern"

        ]

        for fallback_keyword in fallback_keywords:

            extra_results = fetch_adzuna_page(
                keyword=fallback_keyword,
                page=1,
                results_per_page=20,
                location=DEFAULT_LOCATION
            )

            for job in extra_results:

                if is_internship(job):

                    filtered_jobs.append(job)

            if filtered_jobs:
                break

    # -----------------------------------------------------
    # FORMAT + MATCH
    # -----------------------------------------------------

    opportunities = []

    for job in filtered_jobs:

        title = str(
            job.get(
                "title",
                ""
            )
        )

        description = clean_description(
            job.get(
                "description",
                ""
            ),
            max_length=1200
        )

        match = calculate_resume_match(
            resume_keywords=resume_keywords,
            job_description=description,
            job_title=title
        )

        formatted = format_job(
            job=job,
            resume_match=match,
            opportunity_type=opportunity_type
        )

        opportunities.append(formatted)

    # -----------------------------------------------------
    # SORT BY RESUME MATCH
    # -----------------------------------------------------

    opportunities.sort(
        key=lambda item: (
            float(
                item.get(
                    "resume_match",
                    0
                ) or 0
            ),
            str(
                item.get(
                    "created",
                    ""
                )
            )
        ),
        reverse=True
    )

    print(
        f"Found {len(opportunities)} "
        f"live {opportunity_type} result(s)."
    )

    return opportunities[:20]


# =========================================================
# BACKWARD COMPATIBILITY
# =========================================================

def get_recommendations(
    role,
    opportunity_type="job",
    resume_text="",
    skills=None
):

    return recommend_jobs(
        role=role,
        opportunity_type=opportunity_type,
        resume_text=resume_text,
        skills=skills
    )