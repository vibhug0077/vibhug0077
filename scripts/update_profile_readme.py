#!/usr/bin/env python3
"""
Dynamic GitHub Profile README updater.

What it does:
- Updates the section between <!--START:DYNAMIC_PROFILE--> and <!--END:DYNAMIC_PROFILE-->
- Adds current IST timestamp
- Pulls public repositories from GitHub API when available
- Falls back to a curated repository list if API access fails

No external Python packages required.
"""

from __future__ import annotations

import json
import os
import re
import urllib.request
from datetime import datetime
from zoneinfo import ZoneInfo


USERNAME = "vibhug0077"
README_PATH = "README.md"

CURATED_REPOS = [
    ("Python_Programing", "Python notebooks and programming foundations"),
    ("Linux_Lab", "Linux commands, Bash scripting and lab practice"),
    ("Docker_Containers", "Docker, containers and DevOps labs"),
    ("Mathematics-for-Machine-Learning", "Mathematics foundations for ML"),
    ("Classical_Machine_Learning_First_Course", "Classical ML concepts and examples"),
    ("DSA_Python_Easy_21Day", "Python DSA practice plan"),
]


def fetch_public_repositories(username: str) -> list[dict]:
    """Fetch public repositories from GitHub API."""
    url = f"https://api.github.com/users/{username}/repos?sort=updated&per_page=10"
    headers = {
        "Accept": "application/vnd.github+json",
        "User-Agent": f"{username}-profile-readme-updater",
    }

    token = os.environ.get("GITHUB_TOKEN")
    if token:
        headers["Authorization"] = f"Bearer {token}"

    request = urllib.request.Request(url, headers=headers)

    with urllib.request.urlopen(request, timeout=20) as response:
        return json.loads(response.read().decode("utf-8"))


def describe_repo(repo: dict) -> str:
    """Create a short focus line for a repo."""
    description = repo.get("description") or ""
    language = repo.get("language") or "Learning Resource"

    if description:
        return description.strip()

    focus_by_name = {
        "Python_Programing": "Python notebooks and programming foundations",
        "Linux_Lab": "Linux commands, Bash scripting and lab practice",
        "Docker_Containers": "Docker, containers and DevOps labs",
        "Mathematics-for-Machine-Learning": "Mathematics foundations for ML",
        "Classical_Machine_Learning_First_Course": "Classical ML concepts and examples",
        "DSA_Python_Easy_21Day": "Python DSA practice plan",
    }

    return focus_by_name.get(repo.get("name", ""), f"{language} based learning repository")


def build_dynamic_section() -> str:
    """Build dynamic markdown block."""
    now = datetime.now(ZoneInfo("Asia/Kolkata")).strftime("%Y-%m-%d %H:%M IST")

    rows: list[str] = []

    try:
        repos = fetch_public_repositories(USERNAME)
        repos = [repo for repo in repos if not repo.get("fork") and repo.get("name") != USERNAME]

        for repo in repos[:6]:
            name = repo["name"]
            url = repo["html_url"]
            focus = describe_repo(repo)
            rows.append(f"| [`{name}`]({url}) | {focus} |")
    except Exception as exc:
        print(f"GitHub API fallback used: {exc}")
        for name, focus in CURATED_REPOS:
            rows.append(f"| [`{name}`](https://github.com/{USERNAME}/{name}) | {focus} |")

    repo_table = "\n".join(rows)

    return f"""<!--START:DYNAMIC_PROFILE-->
### Latest Profile Update

- **Last automated update:** {now}
- **Current focus:** Data Science, Linux Labs, Docker, MLOps and Cloud Deployment
- **Active build mode:** Teaching repositories + practical project templates

### Recently Highlighted Repositories

| Repository | Focus |
|---|---|
{repo_table}
<!--END:DYNAMIC_PROFILE-->"""


def update_readme() -> None:
    """Replace the dynamic block inside README.md."""
    with open(README_PATH, "r", encoding="utf-8") as file:
        readme = file.read()

    pattern = r"<!--START:DYNAMIC_PROFILE-->.*?<!--END:DYNAMIC_PROFILE-->"
    replacement = build_dynamic_section()

    updated_readme, replacements = re.subn(
        pattern,
        replacement,
        readme,
        flags=re.DOTALL,
    )

    if replacements == 0:
        raise RuntimeError("Dynamic profile markers not found in README.md")

    with open(README_PATH, "w", encoding="utf-8") as file:
        file.write(updated_readme)

    print("README.md dynamic profile section updated successfully.")


if __name__ == "__main__":
    update_readme()
