import re


ROLE_TECHNOLOGIES = {
    "Machine Learning Engineer": [
        "machine learning",
        "scikit-learn",
        "sklearn",
        "tensorflow",
        "pytorch",
        "pandas",
        "numpy",
        "feature engineering",
        "classification",
        "regression",
        "clustering",
        "model training",
        "model evaluation",
        "cross validation",
        "random forest",
        "gradient boosting",
        "xgboost",
        "supervised learning",
        "unsupervised learning",
    ],

    "AI Engineer": [
        "artificial intelligence",
        "machine learning",
        "deep learning",
        "tensorflow",
        "pytorch",
        "nlp",
        "computer vision",
        "generative ai",
        "llm",
        "embeddings",
        "ai application",
        "model deployment",
    ],

    "Data Scientist": [
        "data science",
        "machine learning",
        "pandas",
        "numpy",
        "scikit-learn",
        "statistics",
        "eda",
        "exploratory data analysis",
        "feature engineering",
        "data visualization",
        "regression",
        "classification",
        "clustering",
        "model evaluation",
        "python",
        "sql",
    ],

    "Data Analyst": [
        "data analysis",
        "data analyst",
        "sql",
        "excel",
        "power bi",
        "tableau",
        "data visualization",
        "statistics",
        "eda",
        "reporting",
        "dashboard",
        "pandas",
    ],

    "Deep Learning Engineer": [
        "deep learning",
        "neural network",
        "cnn",
        "rnn",
        "lstm",
        "transformer",
        "tensorflow",
        "pytorch",
        "computer vision",
        "deep neural network",
    ],

    "NLP Engineer": [
        "nlp",
        "natural language processing",
        "text classification",
        "text preprocessing",
        "tf-idf",
        "embeddings",
        "transformers",
        "bert",
        "language model",
        "sentiment analysis",
        "tokenization",
    ],

    "Computer Vision Engineer": [
        "computer vision",
        "opencv",
        "cnn",
        "image classification",
        "object detection",
        "image processing",
        "yolo",
        "tensorflow",
        "pytorch",
    ],

    "Generative AI Engineer": [
        "generative ai",
        "genai",
        "llm",
        "large language model",
        "prompt engineering",
        "embeddings",
        "rag",
        "retrieval augmented generation",
        "vector database",
        "transformers",
        "openai",
        "gemini",
    ],

    "Python Developer": [
        "python developer",
        "python development",
        "python application",
        "flask",
        "django",
        "fastapi",
        "rest api",
        "backend development",
        "web development",
    ],

    "Web Developer": [
        "web developer",
        "html",
        "css",
        "javascript",
        "frontend",
        "backend",
        "react",
        "node.js",
        "django",
        "flask",
        "web application",
    ],

    "Java Developer": [
        "java developer",
        "java",
        "spring boot",
        "spring",
        "hibernate",
        "maven",
        "jpa",
        "backend development",
    ],
}


# These signals indicate that a resume is genuinely ML-focused.
STRONG_ML_SIGNALS = [
    "machine learning",
    "scikit-learn",
    "sklearn",
    "tensorflow",
    "pytorch",
    "feature engineering",
    "model evaluation",
    "model training",
    "classification",
    "regression",
    "clustering",
    "cross validation",
    "random forest",
    "gradient boosting",
    "xgboost",
    "deep learning",
    "neural network",
    "nlp",
    "computer vision",
    "generative ai",
]


def normalize(text):
    if not text:
        return ""

    text = text.lower()

    text = re.sub(r"[\u2010-\u2015]", "-", text)

    text = re.sub(r"\s+", " ", text)

    return text.strip()


def find_matches(text, keywords):
    normalized = normalize(text)

    matches = []

    for keyword in keywords:
        keyword_normalized = normalize(keyword)

        if keyword_normalized in normalized:
            matches.append(keyword)

    return matches


def calculate_resume_role_scores(text):
    normalized = normalize(text)

    scores = {}

    for role, technologies in ROLE_TECHNOLOGIES.items():

        score = 0
        matches = []

        for technology in technologies:

            tech = normalize(technology)

            if tech in normalized:

                matches.append(technology)

                # Stronger weight for multi-word/domain-specific evidence.
                if len(tech.split()) >= 2:
                    score += 4
                else:
                    score += 2

        scores[role] = {
            "score": score,
            "matches": matches
        }

    return scores


def calculate_github_role_evidence(github_evidence):
    if not github_evidence:
        return {}

    text_parts = []

    technologies = github_evidence.get("technologies", [])

    for technology in technologies:
        text_parts.append(str(technology))

    projects = github_evidence.get("projects", [])

    for project in projects:
        text_parts.append(str(project.get("name", "")))
        text_parts.append(str(project.get("description", "")))
        text_parts.append(str(project.get("languages", "")))
        text_parts.append(str(project.get("topics", "")))

    combined_text = " ".join(text_parts)

    role_scores = calculate_resume_role_scores(combined_text)

    return role_scores


def calculate_portfolio_role_evidence(portfolio_evidence):
    if not portfolio_evidence:
        return {}

    combined_parts = []

    for portfolio in portfolio_evidence:

        if not portfolio:
            continue

        combined_parts.append(str(portfolio.get("title", "")))
        combined_parts.append(str(portfolio.get("text", "")))

        technologies = portfolio.get("technologies", [])

        combined_parts.extend(
            [str(item) for item in technologies]
        )

        projects = portfolio.get("projects", [])

        for project in projects:
            combined_parts.append(str(project))

    combined_text = " ".join(combined_parts)

    return calculate_resume_role_scores(combined_text)


def get_project_proof(github_evidence, portfolio_evidence, role):
    proof = []

    if github_evidence:

        projects = github_evidence.get("projects", [])

        for project in projects[:5]:

            name = project.get("name")

            if name:
                proof.append(
                    f"GitHub project: {name}"
                )

    if portfolio_evidence:

        for portfolio in portfolio_evidence:

            projects = portfolio.get("projects", [])

            for project in projects[:5]:

                if project:
                    proof.append(
                        f"Portfolio project: {project}"
                    )

    return proof[:10]


def build_strengths(role, matches, github_matches, portfolio_matches):
    strengths = []

    if matches:
        strengths.append(
            f"Resume contains {len(matches)} relevant {role} signals."
        )

    if github_matches:
        strengths.append(
            f"GitHub provides {len(github_matches)} additional technical signals."
        )

    if portfolio_matches:
        strengths.append(
            f"Portfolio provides {len(portfolio_matches)} additional technical signals."
        )

    return strengths


def get_missing_evidence(role, matches):
    important = ROLE_TECHNOLOGIES.get(role, [])

    normalized_matches = {
        normalize(item)
        for item in matches
    }

    missing = []

    for item in important:

        if normalize(item) not in normalized_matches:
            missing.append(item)

    return missing[:8]


def predict_role(
    text,
    ml_prediction=None,
    github_evidence=None,
    portfolio_evidence=None
):

    resume_scores = calculate_resume_role_scores(text)

    github_scores = calculate_github_role_evidence(
        github_evidence
    )

    portfolio_scores = calculate_portfolio_role_evidence(
        portfolio_evidence
    )

    final_scores = {}

    for role in ROLE_TECHNOLOGIES:

        resume_score = resume_scores.get(
            role,
            {}
        ).get("score", 0)

        github_score = github_scores.get(
            role,
            {}
        ).get("score", 0)

        portfolio_score = portfolio_scores.get(
            role,
            {}
        ).get("score", 0)

        # Resume is the primary source.
        final_score = (
            resume_score * 0.70
            + github_score * 0.20
            + portfolio_score * 0.10
        )

        # Existing ML classifier is only a small supporting signal.
        if ml_prediction:
            if normalize(ml_prediction) == normalize(role):
                final_score += 2

        final_scores[role] = round(final_score, 2)

    # Special protection against Python Developer being selected
    # merely because Python is present in an ML resume.
    normalized_text = normalize(text)

    ml_signal_count = len(
        find_matches(
            normalized_text,
            STRONG_ML_SIGNALS
        )
    )

    if ml_signal_count >= 4:

        for role in [
            "Machine Learning Engineer",
            "AI Engineer",
            "Data Scientist",
            "Deep Learning Engineer",
            "NLP Engineer",
            "Computer Vision Engineer",
            "Generative AI Engineer",
        ]:

            if role in final_scores:
                final_scores[role] += 8

        if "Python Developer" in final_scores:
            final_scores["Python Developer"] *= 0.55

    predicted_role = max(
        final_scores,
        key=final_scores.get
    )

    resume_matches = resume_scores.get(
        predicted_role,
        {}
    ).get("matches", [])

    github_matches = github_scores.get(
        predicted_role,
        {}
    ).get("matches", [])

    portfolio_matches = portfolio_scores.get(
        predicted_role,
        {}
    ).get("matches", [])

    project_proof = get_project_proof(
        github_evidence,
        portfolio_evidence,
        predicted_role
    )

    strongest_score = final_scores[predicted_role]

    second_scores = sorted(
        final_scores.values(),
        reverse=True
    )

    second_score = (
        second_scores[1]
        if len(second_scores) > 1
        else 0
    )

    # Confidence is based on evidence and separation between roles.
    if strongest_score <= 0:
        confidence = 0
    else:

        evidence_confidence = min(
            strongest_score * 2.5,
            85
        )

        separation = min(
            max(strongest_score - second_score, 0) * 3,
            15
        )

        confidence = round(
            min(
                evidence_confidence + separation,
                98
            ),
            1
        )

    alternatives = [
        {
            "role": role,
            "score": score
        }
        for role, score in sorted(
            final_scores.items(),
            key=lambda item: item[1],
            reverse=True
        )
        if role != predicted_role
    ][:3]

    strengths = build_strengths(
        predicted_role,
        resume_matches,
        github_matches,
        portfolio_matches
    )

    missing_evidence = get_missing_evidence(
        predicted_role,
        resume_matches
    )

    return {
        "role": predicted_role,
        "confidence": confidence,
        "skills": resume_matches,
        "categories": [],
        "matched_evidence": resume_matches,
        "strengths": strengths,
        "missing_evidence": missing_evidence,
        "alternatives": alternatives,
        "ml_prediction": ml_prediction,
        "github_evidence": github_evidence,
        "portfolio_evidence": portfolio_evidence,
        "github_role_matches": github_matches,
        "portfolio_role_matches": portfolio_matches,
        "github_project_proof": project_proof,
        "portfolio_project_proof": project_proof,
        "role_scores": final_scores,
    }