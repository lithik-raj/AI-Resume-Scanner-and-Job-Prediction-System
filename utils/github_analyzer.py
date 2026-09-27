import re
import requests
from urllib.parse import urlparse


GITHUB_API = "https://api.github.com"

HEADERS = {
    "Accept": "application/vnd.github+json",
    "X-GitHub-Api-Version": "2026-03-10",
    "User-Agent": "AI-Resume-Screener"
}


# ============================================================
# EXTRACT GITHUB USERNAME
# ============================================================

def extract_github_username(github_url):
    """
    Extract the GitHub username from a public GitHub URL.

    Examples:
        https://github.com/example
        https://github.com/example/
        https://github.com/example/project
    """

    if not github_url:
        return None

    try:
        parsed = urlparse(github_url)

        hostname = parsed.netloc.lower().replace(
            "www.",
            ""
        )

        if hostname != "github.com":
            return None

        parts = [
            part
            for part in parsed.path.split("/")
            if part
        ]

        if not parts:
            return None

        username = parts[0]

        # GitHub usernames allow letters, numbers and hyphens.
        if not re.match(
            r"^[A-Za-z0-9-]+$",
            username
        ):
            return None

        return username

    except Exception:
        return None


# ============================================================
# API REQUEST
# ============================================================

def github_get(url, params=None):
    """
    Safely request public GitHub API data.
    """

    try:

        response = requests.get(
            url,
            headers=HEADERS,
            params=params,
            timeout=10
        )

        if response.status_code == 200:
            return response.json()

        print(
            f"GitHub API returned {response.status_code}: "
            f"{url}"
        )

        return None

    except requests.RequestException as error:

        print(
            "GitHub connection error:",
            error
        )

        return None


# ============================================================
# USER PROFILE
# ============================================================

def get_github_profile(username):
    """
    Retrieve public GitHub profile information.
    """

    url = f"{GITHUB_API}/users/{username}"

    data = github_get(url)

    if not data:
        return None

    return {
        "username": data.get(
            "login",
            username
        ),

        "name": data.get(
            "name",
            ""
        ),

        "bio": data.get(
            "bio",
            ""
        ),

        "public_repos": data.get(
            "public_repos",
            0
        ),

        "followers": data.get(
            "followers",
            0
        ),

        "following": data.get(
            "following",
            0
        ),

        "profile_url": data.get(
            "html_url",
            ""
        )
    }


# ============================================================
# REPOSITORIES
# ============================================================

def get_github_repositories(username):
    """
    Retrieve public repositories owned by the GitHub user.
    """

    url = (
        f"{GITHUB_API}/users/"
        f"{username}/repos"
    )

    params = {
        "type": "owner",
        "sort": "updated",
        "direction": "desc",
        "per_page": 30,
        "page": 1
    }

    data = github_get(
        url,
        params
    )

    if not isinstance(
        data,
        list
    ):
        return []

    repositories = []

    for repo in data:

        # Ignore forks because they provide
        # weaker evidence of original project work.
        if repo.get("fork"):
            continue

        repositories.append({

            "name": repo.get(
                "name",
                ""
            ),

            "full_name": repo.get(
                "full_name",
                ""
            ),

            "description": repo.get(
                "description",
                ""
            ),

            "url": repo.get(
                "html_url",
                ""
            ),

            "homepage": repo.get(
                "homepage",
                ""
            ),

            "language": repo.get(
                "language",
                ""
            ),

            "topics": repo.get(
                "topics",
                []
            ),

            "stars": repo.get(
                "stargazers_count",
                0
            ),

            "forks": repo.get(
                "forks_count",
                0
            ),

            "size": repo.get(
                "size",
                0
            ),

            "created_at": repo.get(
                "created_at",
                ""
            ),

            "updated_at": repo.get(
                "updated_at",
                ""
            ),

            "pushed_at": repo.get(
                "pushed_at",
                ""
            ),

            "default_branch": repo.get(
                "default_branch",
                "main"
            )

        })

    return repositories


# ============================================================
# REPOSITORY LANGUAGES
# ============================================================

def get_repository_languages(
    username,
    repository_name
):
    """
    Get language statistics for one repository.
    """

    url = (
        f"{GITHUB_API}/repos/"
        f"{username}/"
        f"{repository_name}/languages"
    )

    data = github_get(url)

    if not isinstance(
        data,
        dict
    ):
        return []

    # GitHub returns byte counts.
    # We only need the language names as
    # evidence for resume-role analysis.
    languages = list(
        data.keys()
    )

    return languages


# ============================================================
# PROJECT EVIDENCE
# ============================================================

def build_project_evidence(
    repositories,
    username
):
    """
    Convert GitHub repositories into
    useful evidence for the prediction engine.
    """

    project_evidence = []

    for repo in repositories:

        repo_name = repo.get(
            "name",
            ""
        )

        languages = []

        if repo_name:

            languages = get_repository_languages(
                username,
                repo_name
            )

        combined_text = " ".join([
            repo.get("name", ""),
            repo.get("description", ""),
            " ".join(
                repo.get(
                    "topics",
                    []
                )
            ),
            repo.get(
                "language",
                ""
            ),
            " ".join(languages)
        ])

        project_evidence.append({

            "project": repo_name,

            "description": repo.get(
                "description",
                ""
            ),

            "url": repo.get(
                "url",
                ""
            ),

            "homepage": repo.get(
                "homepage",
                ""
            ),

            "languages": languages,

            "topics": repo.get(
                "topics",
                []
            ),

            "stars": repo.get(
                "stars",
                0
            ),

            "forks": repo.get(
                "forks",
                0
            ),

            "evidence_text": combined_text

        })

    return project_evidence


# ============================================================
# ROLE-RELEVANT TECHNOLOGY EVIDENCE
# ============================================================

def detect_github_technologies(
    project_evidence
):
    """
    Collect technologies appearing across
    the user's public repositories.
    """

    technologies = []

    for project in project_evidence:

        technologies.extend(
            project.get(
                "languages",
                []
            )
        )

        technologies.extend(
            project.get(
                "topics",
                []
            )
        )

    # Normalize and remove duplicates.
    unique = []
    seen = set()

    for technology in technologies:

        if not technology:
            continue

        normalized = technology.lower().strip()

        if normalized in seen:
            continue

        seen.add(
            normalized
        )

        unique.append(
            technology
        )

    return unique


# ============================================================
# MAIN GITHUB ANALYZER
# ============================================================

def analyze_github(github_url):
    """
    Analyze publicly accessible GitHub information.

    Returns structured evidence that can later be
    combined with resume evidence.
    """

    result = {

        "available": False,

        "url": github_url,

        "username": "",

        "profile": None,

        "repositories": [],

        "project_evidence": [],

        "technologies": [],

        "project_count": 0,

        "proof": [],

        "error": ""

    }

    username = extract_github_username(
        github_url
    )

    if not username:

        result["error"] = (
            "Invalid GitHub profile URL."
        )

        return result

    result["username"] = username

    profile = get_github_profile(
        username
    )

    if not profile:

        result["error"] = (
            "GitHub profile could not be accessed."
        )

        return result

    repositories = get_github_repositories(
        username
    )

    project_evidence = build_project_evidence(
        repositories,
        username
    )

    technologies = detect_github_technologies(
        project_evidence
    )

    result["available"] = True
    result["profile"] = profile
    result["repositories"] = repositories
    result["project_evidence"] = project_evidence
    result["technologies"] = technologies
    result["project_count"] = len(
        project_evidence
    )

    # --------------------------------------------------------
    # Generate human-readable proof
    # --------------------------------------------------------

    if profile.get("public_repos", 0) > 0:

        result["proof"].append(
            f"Public GitHub profile contains "
            f"{profile['public_repos']} repositories."
        )

    for project in project_evidence[:8]:

        project_name = project.get(
            "project",
            "Unnamed project"
        )

        languages = project.get(
            "languages",
            []
        )

        topics = project.get(
            "topics",
            []
        )

        evidence_parts = []

        if languages:

            evidence_parts.append(
                "languages: "
                + ", ".join(
                    languages[:6]
                )
            )

        if topics:

            evidence_parts.append(
                "topics: "
                + ", ".join(
                    topics[:6]
                )
            )

        description = project.get(
            "description",
            ""
        )

        if description:

            evidence_parts.append(
                "description: "
                + description[:180]
            )

        if evidence_parts:

            result["proof"].append(
                f"GitHub project '{project_name}' "
                + " | ".join(
                    evidence_parts
                )
            )

    return result