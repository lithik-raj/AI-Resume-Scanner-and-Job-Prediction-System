import re
from urllib.parse import urlparse


# ============================================================
# URL EXTRACTION
# ============================================================

URL_PATTERN = re.compile(
    r"(https?://[^\s<>\"]+|"
    r"www\.[^\s<>\"]+|"
    r"(?:github\.com|gitlab\.com|bitbucket\.org|"
    r"linkedin\.com|[a-zA-Z0-9-]+\.(?:com|in|io|dev|me|net|org))"
    r"/[^\s<>\"]+)",
    re.IGNORECASE
)


# ============================================================
# CLEAN URL
# ============================================================

def clean_url(url):
    """
    Clean punctuation that may have been captured from
    the end of a sentence in a resume.
    """

    if not url:
        return ""

    url = url.strip()

    # Remove common punctuation accidentally captured.
    url = url.rstrip(
        ".,;:!?)]}>\"'"
    )

    # Add protocol if missing.
    if not url.startswith(
        ("http://", "https://")
    ):

        url = "https://" + url

    return url


# ============================================================
# VALIDATE URL
# ============================================================

def is_valid_url(url):
    """
    Check whether the extracted string has a valid
    HTTP/HTTPS URL structure.
    """

    try:

        parsed = urlparse(url)

        return (
            parsed.scheme in (
                "http",
                "https"
            )
            and bool(parsed.netloc)
        )

    except Exception:

        return False


# ============================================================
# IDENTIFY URL TYPE
# ============================================================

def identify_url_type(url):
    """
    Identify the source represented by the URL.
    """

    try:

        hostname = urlparse(
            url
        ).netloc.lower()

    except Exception:

        return "website"

    # Remove www.
    hostname = hostname.replace(
        "www.",
        ""
    )

    if hostname == "github.com":
        return "github"

    if hostname == "gitlab.com":
        return "gitlab"

    if hostname == "bitbucket.org":
        return "bitbucket"

    if hostname == "linkedin.com":
        return "linkedin"

    return "portfolio"


# ============================================================
# EXTRACT URLS
# ============================================================

def extract_urls(text):
    """
    Extract unique public URLs from resume text.

    Returns a list of dictionaries containing:
        url
        type
    """

    if not text:
        return []

    matches = URL_PATTERN.findall(
        text
    )

    results = []
    seen = set()

    for raw_url in matches:

        url = clean_url(
            raw_url
        )

        if not url:
            continue

        if not is_valid_url(
            url
        ):
            continue

        normalized = url.lower().rstrip("/")

        if normalized in seen:
            continue

        seen.add(
            normalized
        )

        results.append({

            "url": url,

            "type": identify_url_type(
                url
            )

        })

    return results


# ============================================================
# EXTRACT GITHUB URLS
# ============================================================

def extract_github_urls(text):
    """
    Return only GitHub URLs found in the resume.
    """

    urls = extract_urls(
        text
    )

    return [
        item["url"]
        for item in urls
        if item["type"] == "github"
    ]


# ============================================================
# EXTRACT PORTFOLIO URLS
# ============================================================

def extract_portfolio_urls(text):
    """
    Return portfolio/personal website URLs.

    GitHub, GitLab, Bitbucket and LinkedIn are excluded.
    """

    urls = extract_urls(
        text
    )

    return [
        item["url"]
        for item in urls
        if item["type"] == "portfolio"
    ]


# ============================================================
# GROUP ALL EXTERNAL LINKS
# ============================================================

def get_external_links(text):
    """
    Organize detected links by source.
    """

    urls = extract_urls(
        text
    )

    grouped = {

        "github": [],

        "gitlab": [],

        "bitbucket": [],

        "linkedin": [],

        "portfolio": []

    }

    for item in urls:

        url_type = item["type"]

        if url_type in grouped:

            grouped[url_type].append(
                item["url"]
            )

    return grouped