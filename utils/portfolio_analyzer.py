import re
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse


# ============================================================
# SETTINGS
# ============================================================

HEADERS = {
    "User-Agent": "AI-Resume-Screener/1.0"
}

REQUEST_TIMEOUT = 10

MAX_TEXT_LENGTH = 12000


# ============================================================
# CLEAN TEXT
# ============================================================

def clean_text(text):
    """
    Remove unnecessary whitespace from webpage text.
    """

    if not text:
        return ""

    text = re.sub(
        r"\s+",
        " ",
        text
    )

    return text.strip()


# ============================================================
# VALIDATE PORTFOLIO URL
# ============================================================

def is_valid_portfolio_url(url):
    """
    Allow only normal HTTP/HTTPS webpages.
    """

    try:

        parsed = urlparse(url)

        if parsed.scheme not in (
            "http",
            "https"
        ):
            return False

        if not parsed.netloc:
            return False

        return True

    except Exception:

        return False


# ============================================================
# FETCH WEBPAGE
# ============================================================

def fetch_page(url):
    """
    Fetch a public portfolio webpage.
    """

    if not is_valid_portfolio_url(url):

        return None

    try:

        response = requests.get(
            url,
            headers=HEADERS,
            timeout=REQUEST_TIMEOUT,
            allow_redirects=True
        )

        if response.status_code != 200:

            print(
                "Portfolio HTTP error:",
                response.status_code
            )

            return None

        content_type = response.headers.get(
            "Content-Type",
            ""
        ).lower()

        if (
            "text/html" not in content_type
            and "application/xhtml+xml" not in content_type
        ):

            return None

        return response.text

    except requests.RequestException as error:

        print(
            "Portfolio connection error:",
            error
        )

        return None


# ============================================================
# EXTRACT PAGE INFORMATION
# ============================================================

def extract_page_information(html):
    """
    Extract title, headings, paragraphs,
    links and visible text.
    """

    soup = BeautifulSoup(
        html,
        "html.parser"
    )

    # Remove elements that are normally
    # not useful for project analysis.
    for element in soup([
        "script",
        "style",
        "noscript",
        "svg"
    ]):

        element.decompose()

    title = ""

    if soup.title:

        title = clean_text(
            soup.title.get_text(
                " ",
                strip=True
            )
        )

    headings = []

    for heading in soup.find_all([
        "h1",
        "h2",
        "h3",
        "h4"
    ]):

        text = clean_text(
            heading.get_text(
                " ",
                strip=True
            )
        )

        if text:

            headings.append(
                text
            )

    paragraphs = []

    for paragraph in soup.find_all(
        "p"
    ):

        text = clean_text(
            paragraph.get_text(
                " ",
                strip=True
            )
        )

        if text:

            paragraphs.append(
                text
            )

    links = []

    for link in soup.find_all(
        "a",
        href=True
    ):

        link_text = clean_text(
            link.get_text(
                " ",
                strip=True
            )
        )

        href = link.get(
            "href",
            ""
        ).strip()

        if href:

            links.append({

                "text": link_text,

                "url": href

            })

    visible_text = clean_text(
        soup.get_text(
            " ",
            strip=True
        )
    )

    return {

        "title": title,

        "headings": headings,

        "paragraphs": paragraphs,

        "links": links,

        "text": visible_text[:MAX_TEXT_LENGTH]

    }


# ============================================================
# TECHNOLOGY DETECTION
# ============================================================

TECHNOLOGY_KEYWORDS = {

    "Python": [
        "python",
        "flask",
        "django",
        "fastapi",
        "pandas",
        "numpy"
    ],

    "Machine Learning": [
        "machine learning",
        "scikit-learn",
        "sklearn",
        "xgboost",
        "classification",
        "regression",
        "clustering"
    ],

    "Deep Learning": [
        "deep learning",
        "tensorflow",
        "pytorch",
        "keras",
        "cnn",
        "rnn",
        "lstm"
    ],

    "Generative AI": [
        "generative ai",
        "genai",
        "llm",
        "large language model",
        "rag",
        "langchain",
        "openai",
        "gemini",
        "huggingface"
    ],

    "NLP": [
        "nlp",
        "natural language processing",
        "transformers",
        "bert",
        "gpt",
        "text classification",
        "sentiment analysis"
    ],

    "Computer Vision": [
        "computer vision",
        "opencv",
        "object detection",
        "yolo",
        "image classification",
        "image processing"
    ],

    "Data Science": [
        "data science",
        "data analysis",
        "eda",
        "statistics",
        "data visualization",
        "matplotlib",
        "seaborn"
    ],

    "Web Development": [
        "html",
        "css",
        "javascript",
        "react",
        "node.js",
        "node",
        "express",
        "frontend",
        "backend"
    ],

    "Databases": [
        "mysql",
        "postgresql",
        "mongodb",
        "sqlite",
        "database",
        "sql"
    ],

    "Cloud": [
        "aws",
        "azure",
        "google cloud",
        "gcp",
        "docker",
        "kubernetes"
    ]

}


# ============================================================
# DETECT TECHNOLOGIES
# ============================================================

def detect_technologies(text):
    """
    Detect technical technologies and domains
    mentioned on the portfolio.
    """

    normalized_text = text.lower()

    detected = []

    for category, keywords in TECHNOLOGY_KEYWORDS.items():

        matched_keywords = []

        for keyword in keywords:

            if keyword.lower() in normalized_text:

                matched_keywords.append(
                    keyword
                )

        if matched_keywords:

            detected.append({

                "category": category,

                "keywords": matched_keywords

            })

    return detected


# ============================================================
# FIND PROJECT SECTIONS
# ============================================================

def extract_project_evidence(page_info):
    """
    Identify headings and surrounding text that
    may represent portfolio projects.
    """

    projects = []

    headings = page_info.get(
        "headings",
        []
    )

    paragraphs = page_info.get(
        "paragraphs",
        []
    )

    # Look for project-related headings.
    project_words = [
        "project",
        "projects",
        "work",
        "works",
        "portfolio",
        "application",
        "applications"
    ]

    for heading in headings:

        normalized = heading.lower()

        if any(
            word in normalized
            for word in project_words
        ):

            projects.append({

                "name": heading,

                "evidence": heading

            })

    # If the portfolio does not have obvious
    # project headings, use descriptive paragraphs
    # as secondary project evidence.
    if not projects:

        for paragraph in paragraphs[:15]:

            if len(paragraph) >= 30:

                projects.append({

                    "name": "Portfolio project evidence",

                    "evidence": paragraph[:500]

                })

    return projects[:15]


# ============================================================
# MAIN PORTFOLIO ANALYZER
# ============================================================

def analyze_portfolio(url):
    """
    Analyze a public portfolio website.
    """

    result = {

        "available": False,

        "url": url,

        "title": "",

        "headings": [],

        "projects": [],

        "technologies": [],

        "links": [],

        "text": "",

        "proof": [],

        "error": ""

    }

    html = fetch_page(
        url
    )

    if not html:

        result["error"] = (
            "Portfolio could not be accessed."
        )

        return result

    page_info = extract_page_information(
        html
    )

    technologies = detect_technologies(
        page_info["text"]
    )

    projects = extract_project_evidence(
        page_info
    )

    result["available"] = True

    result["title"] = page_info["title"]

    result["headings"] = page_info["headings"]

    result["projects"] = projects

    result["technologies"] = technologies

    result["links"] = page_info["links"]

    result["text"] = page_info["text"]

    # --------------------------------------------------------
    # Human-readable proof
    # --------------------------------------------------------

    if page_info["title"]:

        result["proof"].append(
            "Portfolio title: "
            + page_info["title"]
        )

    for technology in technologies:

        category = technology[
            "category"
        ]

        keywords = technology[
            "keywords"
        ]

        result["proof"].append(
            f"Portfolio evidence for "
            f"{category}: "
            + ", ".join(
                keywords[:8]
            )
        )

    for project in projects[:8]:

        result["proof"].append(
            "Portfolio project evidence: "
            + project["name"]
        )

    return result