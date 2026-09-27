import re


# ============================================================
# AI / ML / DATA SCIENCE RESUME KNOWLEDGE BASE
# ============================================================

SKILLS_DB = {

    # --------------------------------------------------------
    # PROGRAMMING LANGUAGES
    # --------------------------------------------------------
    "programming": [
        "python",
        "java",
        "c++",
        "c#",
        "c",
        "r programming",
        "r language",
        "javascript",
        "typescript",
        "php",
        "scala",
        "kotlin",
        "go",
        "rust",
        "matlab",
        "bash",
        "shell scripting"
    ],

    # --------------------------------------------------------
    # MACHINE LEARNING
    # --------------------------------------------------------
    "machine_learning": [
        "machine learning",
        "supervised learning",
        "unsupervised learning",
        "semi supervised learning",
        "reinforcement learning",
        "classification",
        "regression",
        "clustering",
        "dimensionality reduction",
        "feature engineering",
        "feature selection",
        "model selection",
        "model evaluation",
        "cross validation",
        "hyperparameter tuning",
        "ensemble learning",
        "decision tree",
        "random forest",
        "gradient boosting",
        "xgboost",
        "lightgbm",
        "catboost",
        "support vector machine",
        "svm",
        "knn",
        "k nearest neighbors",
        "naive bayes",
        "logistic regression",
        "linear regression"
    ],

    # --------------------------------------------------------
    # DEEP LEARNING
    # --------------------------------------------------------
    "deep_learning": [
        "deep learning",
        "neural network",
        "artificial neural network",
        "ann",
        "cnn",
        "convolutional neural network",
        "rnn",
        "recurrent neural network",
        "lstm",
        "gru",
        "transformer",
        "attention mechanism",
        "autoencoder",
        "vae",
        "variational autoencoder",
        "gan",
        "generative adversarial network",
        "transfer learning",
        "fine tuning",
        "deep neural network"
    ],

    # --------------------------------------------------------
    # GENERATIVE AI / LLM
    # --------------------------------------------------------
    "generative_ai": [
        "generative ai",
        "genai",
        "large language model",
        "llm",
        "llms",
        "chatgpt",
        "gemini",
        "claude",
        "openai",
        "generative ai",
        "prompt engineering",
        "prompt design",
        "retrieval augmented generation",
        "rag",
        "vector database",
        "embeddings",
        "semantic search",
        "langchain",
        "llamaindex",
        "hugging face",
        "huggingface",
        "transformer models",
        "fine tuning llm",
        "ai agents",
        "agentic ai",
        "ai chatbot",
        "chatbot"
    ],

    # --------------------------------------------------------
    # NATURAL LANGUAGE PROCESSING
    # --------------------------------------------------------
    "nlp": [
        "natural language processing",
        "nlp",
        "text classification",
        "text mining",
        "sentiment analysis",
        "named entity recognition",
        "ner",
        "tokenization",
        "stemming",
        "lemmatization",
        "word embeddings",
        "tf idf",
        "tf-idf",
        "word2vec",
        "bert",
        "roberta",
        "spacy",
        "nltk"
    ],

    # --------------------------------------------------------
    # COMPUTER VISION
    # --------------------------------------------------------
    "computer_vision": [
        "computer vision",
        "image processing",
        "image classification",
        "object detection",
        "image segmentation",
        "face recognition",
        "opencv",
        "open cv",
        "yolo",
        "yolov5",
        "yolov8",
        "resnet",
        "efficientnet",
        "mobilenet",
        "ocr",
        "optical character recognition"
    ],

    # --------------------------------------------------------
    # DATA SCIENCE
    # --------------------------------------------------------
    "data_science": [
        "data science",
        "data analysis",
        "data analytics",
        "exploratory data analysis",
        "eda",
        "statistical analysis",
        "statistics",
        "data preprocessing",
        "data cleaning",
        "data visualization",
        "predictive analytics",
        "predictive modeling",
        "business analytics",
        "time series",
        "forecasting",
        "a b testing",
        "ab testing"
    ],

    # --------------------------------------------------------
    # PYTHON DATA / ML LIBRARIES
    # --------------------------------------------------------
    "python_libraries": [
        "numpy",
        "pandas",
        "scikit learn",
        "scikit-learn",
        "sklearn",
        "tensorflow",
        "keras",
        "pytorch",
        "torch",
        "matplotlib",
        "seaborn",
        "plotly",
        "scipy",
        "statsmodels",
        "xgboost",
        "lightgbm",
        "catboost",
        "opencv",
        "nltk",
        "spacy",
        "transformers",
        "streamlit",
        "gradio"
    ],

    # --------------------------------------------------------
    # DATABASES
    # --------------------------------------------------------
    "databases": [
        "sql",
        "mysql",
        "postgresql",
        "postgres",
        "mongodb",
        "sqlite",
        "oracle",
        "redis",
        "firebase",
        "dynamodb",
        "nosql",
        "database management",
        "database design"
    ],

    # --------------------------------------------------------
    # WEB DEVELOPMENT
    # --------------------------------------------------------
    "web_development": [
        "html",
        "html5",
        "css",
        "css3",
        "javascript",
        "typescript",
        "react",
        "react.js",
        "angular",
        "vue",
        "node.js",
        "nodejs",
        "express",
        "express.js",
        "flask",
        "django",
        "fastapi",
        "spring boot",
        "rest api",
        "restful api",
        "api development",
        "full stack development",
        "frontend development",
        "backend development"
    ],

    # --------------------------------------------------------
    # CLOUD
    # --------------------------------------------------------
    "cloud": [
        "aws",
        "amazon web services",
        "azure",
        "microsoft azure",
        "google cloud",
        "gcp",
        "google cloud platform",
        "ec2",
        "s3",
        "lambda",
        "cloud computing",
        "cloud deployment"
    ],

    # --------------------------------------------------------
    # DEVOPS / MLOPS
    # --------------------------------------------------------
    "devops_mlops": [
        "docker",
        "kubernetes",
        "jenkins",
        "github actions",
        "ci/cd",
        "cicd",
        "continuous integration",
        "continuous deployment",
        "mlops",
        "model deployment",
        "model serving",
        "mlflow",
        "dvc",
        "terraform",
        "linux",
        "git",
        "github",
        "gitlab"
    ],

    # --------------------------------------------------------
    # BUSINESS INTELLIGENCE
    # --------------------------------------------------------
    "business_intelligence": [
        "power bi",
        "tableau",
        "excel",
        "advanced excel",
        "pivot table",
        "power query",
        "data studio",
        "looker",
        "dashboard development",
        "business intelligence"
    ],

    # --------------------------------------------------------
    # AI CONCEPTS
    # --------------------------------------------------------
    "ai_concepts": [
        "artificial intelligence",
        "ai",
        "machine intelligence",
        "knowledge representation",
        "expert systems",
        "fuzzy logic",
        "genetic algorithm",
        "optimization",
        "recommendation system",
        "recommender system"
    ],

    # --------------------------------------------------------
    # ENGINEERING / DEVELOPMENT TOOLS
    # --------------------------------------------------------
    "tools": [
        "git",
        "github",
        "gitlab",
        "bitbucket",
        "visual studio code",
        "vs code",
        "jupyter",
        "jupyter notebook",
        "google colab",
        "postman",
        "anaconda",
        "pycharm"
    ],

    # --------------------------------------------------------
    # SOFTWARE ENGINEERING
    # --------------------------------------------------------
    "software_engineering": [
        "object oriented programming",
        "oop",
        "data structures",
        "algorithms",
        "data structures and algorithms",
        "software development",
        "software engineering",
        "debugging",
        "unit testing",
        "test automation",
        "version control",
        "agile",
        "scrum"
    ]
}


# ============================================================
# ROLE-RELATED KEYWORDS
# These will later be used by the prediction engine.
# ============================================================

ROLE_KEYWORDS = {

    "Machine Learning Engineer": [
        "machine learning",
        "scikit learn",
        "sklearn",
        "tensorflow",
        "pytorch",
        "model training",
        "model deployment",
        "feature engineering",
        "classification",
        "regression",
        "xgboost",
        "mlops"
    ],

    "AI Engineer": [
        "artificial intelligence",
        "machine learning",
        "deep learning",
        "generative ai",
        "llm",
        "rag",
        "ai agents",
        "tensorflow",
        "pytorch",
        "model deployment"
    ],

    "Data Scientist": [
        "data science",
        "data analysis",
        "machine learning",
        "statistics",
        "pandas",
        "numpy",
        "scikit learn",
        "predictive modeling",
        "eda",
        "data visualization",
        "python"
    ],

    "Data Analyst": [
        "data analysis",
        "data analytics",
        "sql",
        "excel",
        "power bi",
        "tableau",
        "data visualization",
        "statistics",
        "dashboard",
        "reporting"
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
        "computer vision"
    ],

    "NLP Engineer": [
        "natural language processing",
        "nlp",
        "text classification",
        "bert",
        "transformers",
        "nltk",
        "spacy",
        "llm",
        "language model",
        "text mining"
    ],

    "Computer Vision Engineer": [
        "computer vision",
        "opencv",
        "object detection",
        "image classification",
        "image segmentation",
        "yolo",
        "cnn",
        "image processing"
    ],

    "Generative AI Engineer": [
        "generative ai",
        "genai",
        "llm",
        "rag",
        "prompt engineering",
        "embeddings",
        "vector database",
        "langchain",
        "hugging face",
        "ai agents"
    ],

    "Python Developer": [
        "python",
        "flask",
        "django",
        "fastapi",
        "rest api",
        "pandas",
        "numpy",
        "sql",
        "github"
    ],

    "Web Developer": [
        "html",
        "css",
        "javascript",
        "react",
        "node.js",
        "nodejs",
        "express",
        "frontend",
        "backend",
        "rest api"
    ],

    "Java Developer": [
        "java",
        "spring boot",
        "hibernate",
        "maven",
        "rest api",
        "sql",
        "mysql"
    ]
}


# ============================================================
# TEXT NORMALIZATION
# ============================================================

def normalize_text(text):
    """
    Normalize resume text while preserving useful technology
    names and keywords.
    """

    if not text:
        return ""

    text = text.lower()

    replacements = {
        "scikit-learn": "scikit learn",
        "scikit learn": "scikit learn",
        "node.js": "nodejs",
        "react.js": "react",
        "open-cv": "opencv",
        "open cv": "opencv",
        "power-bi": "power bi",
        "machine-learning": "machine learning",
        "deep-learning": "deep learning",
        "data-science": "data science",
        "artificial-intelligence": "artificial intelligence",
        "generative-ai": "generative ai",
        "natural-language-processing": "natural language processing"
    }

    for old, new in replacements.items():
        text = text.replace(old, new)

    # Normalize whitespace.
    text = re.sub(r"\s+", " ", text)

    return text.strip()


# ============================================================
# SAFE SKILL MATCHING
# ============================================================

def skill_exists(text, skill):
    """
    Detect a skill using word boundaries where possible.

    This prevents false matches such as detecting 'c'
    from ordinary words containing the letter c.
    """

    skill = skill.lower().strip()

    if not skill:
        return False

    # Special handling for very short skills.
    if len(skill) <= 2:
        pattern = r"(?<![a-z0-9+#])" + re.escape(skill) + r"(?![a-z0-9+#])"
    else:
        pattern = r"(?<![a-z0-9])" + re.escape(skill) + r"(?![a-z0-9])"

    return re.search(pattern, text) is not None


# ============================================================
# EXTRACT ALL DETECTED SKILLS
# ============================================================

def extract_skills(text):
    """
    Extract technical skills from the complete resume.

    Returns a unique list of detected skills.
    """

    text = normalize_text(text)

    if not text:
        return []

    found_skills = []

    for category, skills in SKILLS_DB.items():

        for skill in skills:

            if skill_exists(text, skill):

                display_skill = skill

                # Avoid duplicate variations.
                if display_skill not in found_skills:
                    found_skills.append(display_skill)

    return found_skills


# ============================================================
# EXTRACT SKILLS BY CATEGORY
# ============================================================

def extract_skills_by_category(text):
    """
    Return detected skills grouped by technical category.
    This will be useful for evidence-based prediction.
    """

    text = normalize_text(text)

    result = {}

    if not text:
        return result

    for category, skills in SKILLS_DB.items():

        detected = []

        for skill in skills:

            if skill_exists(text, skill):

                if skill not in detected:
                    detected.append(skill)

        if detected:
            result[category] = detected

    return result


# ============================================================
# ROLE EVIDENCE ANALYSIS
# ============================================================

def calculate_role_evidence(text):
    """
    Calculate evidence for each possible career role.

    This does NOT blindly predict a role.
    It measures how many relevant keywords are actually
    present in the resume.
    """

    text = normalize_text(text)

    role_evidence = {}

    if not text:
        return role_evidence

    for role, keywords in ROLE_KEYWORDS.items():

        matched = []

        for keyword in keywords:

            if skill_exists(text, keyword):
                matched.append(keyword)

        total_keywords = len(keywords)

        if total_keywords == 0:
            score = 0
        else:
            score = (len(matched) / total_keywords) * 100

        role_evidence[role] = {
            "score": round(score, 2),
            "matched_keywords": matched,
            "matched_count": len(matched),
            "total_keywords": total_keywords
        }

    return role_evidence