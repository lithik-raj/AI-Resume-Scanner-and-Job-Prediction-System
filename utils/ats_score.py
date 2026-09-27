import re


SECTION_KEYWORDS = {
    "summary": [
        "summary",
        "professional summary",
        "profile",
        "objective",
    ],

    "education": [
        "education",
        "academic",
        "qualification",
        "degree",
    ],

    "experience": [
        "experience",
        "work experience",
        "internship",
        "employment",
        "professional experience",
    ],

    "projects": [
        "projects",
        "academic projects",
        "personal projects",
        "technical projects",
    ],

    "skills": [
        "skills",
        "technical skills",
        "technologies",
        "technical expertise",
    ],

    "certifications": [
        "certifications",
        "certificates",
        "courses",
    ],

    "achievements": [
        "achievements",
        "awards",
        "accomplishments",
    ],
}


IMPORTANT_KEYWORDS = [
    "python",
    "machine learning",
    "deep learning",
    "artificial intelligence",
    "data science",
    "data analysis",
    "scikit-learn",
    "tensorflow",
    "pytorch",
    "pandas",
    "numpy",
    "sql",
    "nlp",
    "computer vision",
    "generative ai",
    "llm",
    "flask",
    "fastapi",
    "rest api",
    "git",
    "github",
    "feature engineering",
    "model evaluation",
    "model training",
    "classification",
    "regression",
    "clustering",
    "neural network",
]


def normalize_text(text):
    if not text:
        return ""

    text = text.lower()

    text = re.sub(
        r"[\u2010-\u2015]",
        "-",
        text
    )

    text = re.sub(
        r"\s+",
        " ",
        text
    )

    return text.strip()


def keyword_exists(text, keyword):
    normalized_text = normalize_text(text)
    normalized_keyword = normalize_text(keyword)

    return normalized_keyword in normalized_text


def detect_sections(text):
    normalized_text = normalize_text(text)

    detected = {}

    for section, keywords in SECTION_KEYWORDS.items():

        found = False

        for keyword in keywords:

            if keyword in normalized_text:
                found = True
                break

        detected[section] = found

    return detected


def analyze_keywords(text):
    normalized_text = normalize_text(text)

    matched = []
    missing = []

    for keyword in IMPORTANT_KEYWORDS:

        if keyword in normalized_text:
            matched.append(keyword)
        else:
            missing.append(keyword)

    return {
        "matched": matched,
        "missing": missing,
        "total": len(IMPORTANT_KEYWORDS),
    }


def analyze_projects(text):
    normalized_text = normalize_text(text)

    project_score = 0
    evidence = []

    project_keywords = [
        "project",
        "developed",
        "built",
        "implemented",
        "created",
        "designed",
        "deployed",
        "model",
        "prediction",
        "classification",
        "dashboard",
        "application",
        "pipeline",
        "api",
    ]

    project_section_found = False

    for keyword in SECTION_KEYWORDS["projects"]:

        if keyword in normalized_text:
            project_section_found = True
            break

    if project_section_found:
        project_score += 40
        evidence.append("Projects section found.")

    matched_project_terms = []

    for keyword in project_keywords:

        if keyword in normalized_text:
            matched_project_terms.append(keyword)

    if matched_project_terms:

        project_score += min(
            len(matched_project_terms) * 5,
            40
        )

        evidence.append(
            f"{len(matched_project_terms)} project-related terms found."
        )

    if any(
        keyword in normalized_text
        for keyword in [
            "github",
            "portfolio",
            "deployed",
            "deployment",
            "live demo",
        ]
    ):

        project_score += 20

        evidence.append(
            "Project/deployment evidence found."
        )

    return {
        "score": min(project_score, 100),
        "evidence": evidence,
    }


def analyze_experience(text):
    normalized_text = normalize_text(text)

    score = 0
    evidence = []

    experience_found = False

    for keyword in SECTION_KEYWORDS["experience"]:

        if keyword in normalized_text:
            experience_found = True
            break

    if experience_found:

        score += 50

        evidence.append(
            "Experience or internship section found."
        )

    experience_terms = [
        "intern",
        "internship",
        "worked",
        "developed",
        "implemented",
        "collaborated",
        "responsible",
        "experience",
    ]

    matched = [
        term
        for term in experience_terms
        if term in normalized_text
    ]

    score += min(
        len(matched) * 6,
        50
    )

    if matched:

        evidence.append(
            f"{len(matched)} experience-related terms found."
        )

    return {
        "score": min(score, 100),
        "evidence": evidence,
    }


def analyze_education(text):
    normalized_text = normalize_text(text)

    score = 0
    evidence = []

    education_found = False

    for keyword in SECTION_KEYWORDS["education"]:

        if keyword in normalized_text:
            education_found = True
            break

    if education_found:

        score += 60

        evidence.append(
            "Education section found."
        )

    degree_keywords = [
        "b.tech",
        "btech",
        "b.e",
        "bachelor",
        "degree",
        "engineering",
        "computer science",
        "artificial intelligence",
        "data science",
    ]

    matched = [
        keyword
        for keyword in degree_keywords
        if keyword in normalized_text
    ]

    score += min(
        len(matched) * 8,
        40
    )

    if matched:

        evidence.append(
            "Degree/academic information detected."
        )

    return {
        "score": min(score, 100),
        "evidence": evidence,
    }


def analyze_skills(skills):
    if not skills:
        return {
            "score": 0,
            "count": 0,
        }

    unique_skills = set()

    for skill in skills:

        if skill:

            normalized = normalize_text(
                str(skill)
            )

            unique_skills.add(normalized)

    count = len(unique_skills)

    # Score increases with actual skill count.
    score = min(
        100,
        count * 5
    )

    return {
        "score": score,
        "count": count,
    }


def calculate_ats(skills, text=""):
    details = get_ats_details(
        skills,
        text
    )

    return details["score"]


def get_ats_details(skills, text=""):

    normalized_text = normalize_text(text)

    # -----------------------------
    # 1. TECHNICAL SKILLS — 35%
    # -----------------------------

    skill_analysis = analyze_skills(
        skills
    )

    technical_score = skill_analysis["score"]

    # -----------------------------
    # 2. IMPORTANT KEYWORDS — 20%
    # -----------------------------

    keyword_analysis = analyze_keywords(
        normalized_text
    )

    keyword_total = keyword_analysis["total"]

    if keyword_total > 0:

        keyword_score = (
            len(keyword_analysis["matched"])
            / keyword_total
        ) * 100

    else:
        keyword_score = 0

    # -----------------------------
    # 3. PROJECTS — 20%
    # -----------------------------

    project_analysis = analyze_projects(
        normalized_text
    )

    project_score = project_analysis["score"]

    # -----------------------------
    # 4. EDUCATION — 10%
    # -----------------------------

    education_analysis = analyze_education(
        normalized_text
    )

    education_score = education_analysis["score"]

    # -----------------------------
    # 5. EXPERIENCE — 15%
    # -----------------------------

    experience_analysis = analyze_experience(
        normalized_text
    )

    experience_score = experience_analysis["score"]

    # -----------------------------
    # FINAL WEIGHTED SCORE
    # -----------------------------

    final_score = (
        technical_score * 0.35
        + keyword_score * 0.20
        + project_score * 0.20
        + education_score * 0.10
        + experience_score * 0.15
    )

    final_score = round(
        max(
            0,
            min(
                final_score,
                100
            )
        )
    )

    sections = detect_sections(
        normalized_text
    )

    return {
        "score": final_score,

        "breakdown": {
            "technical_skills": round(
                technical_score
            ),

            "important_keywords": round(
                keyword_score
            ),

            "projects": round(
                project_score
            ),

            "education": round(
                education_score
            ),

            "experience": round(
                experience_score
            ),
        },

        "skills_count": skill_analysis["count"],

        "matched_keywords":
            keyword_analysis["matched"],

        "missing_keywords":
            keyword_analysis["missing"],

        "sections":
            sections,

        "project_evidence":
            project_analysis["evidence"],

        "education_evidence":
            education_analysis["evidence"],

        "experience_evidence":
            experience_analysis["evidence"],
    }