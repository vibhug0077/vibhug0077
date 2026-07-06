#!/usr/bin/env python3
"""
Reliable text-based GitHub Profile README updater.

This script updates only the text/table section between:
<!--START:DYNAMIC_PROFILE--> and <!--END:DYNAMIC_PROFILE-->

It intentionally does NOT generate external image cards for repositories.
That avoids broken README images caused by third-party stats services.
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

FALLBACK_REPOS = [
    ("Python_Programing", "Python notebooks and programming foundations"),
    ("Linux_Lab", "Linux commands, Bash scripting and lab practice"),
    ("Docker_Containers", "Docker, containers and DevOps labs"),
    ("Mathematics-for-Machine-Learning", "Mathematics foundations for ML"),
    ("Classical_Machine_Learning_First_Course", "Classical ML concepts and examples"),
    ("DSA_Python_Easy_21Day", "Python DSA practice plan"),
]


def fetch_repos(username: str) -> list[dict]:
    """Fetch public repositories sorted by latest update."""
    url = f"https://api.github.com/users/{username}/repos?sort=updated&per_page=20"
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


def clean_description(repo: dict) -> str:
    """Return a concise description for a repository."""
    description = (repo.get("description") or "").strip()
    language = repo.get("language") or "Learning"

    fallback = {
        "Python_Programing": "Python notebooks and programming foundations",
        "Linux_Lab": "Linux commands, Bash scripting and lab practice",
        "Docker_Containers": "Docker, containers and DevOps labs",
        "Mathematics-for-Machine-Learning": "Mathematics foundations for ML",
        "Classical_Machine_Learning_First_Course": "Classical ML concepts and examples",
        "DSA_Python_Easy_21Day": "Python DSA practice plan",
    }

    if repo.get("name") in fallback:
        return fallback[repo["name"]]

    return description if description else f"{language} based learning repository"


def build_dynamic_section() -> str:
    now = datetime.now(ZoneInfo("Asia/Kolkata")).strftime("%Y-%m-%d %H:%M IST")

    rows: list[str] = []

    try:
        repos = fetch_repos(USERNAME)
        repos = [
            repo for repo in repos
            if not repo.get("fork") and repo.get("name") != USERNAME
        ]

        priority = {
            "Python_Programing": 1,
            "Linux_Lab": 2,
            "Docker_Containers": 3,
            "Mathematics-for-Machine-Learning": 4,
            "Classical_Machine_Learning_First_Course": 5,
            "DSA_Python_Easy_21Day": 6,
        }

        repos.sort(key=lambda r: priority.get(r.get("name", ""), 999))

        for repo in repos[:6]:
            name = repo["name"]
            url = repo["html_url"]
            focus = clean_description(repo).replace("|", "-")
            rows.append(f"| [`{name}`]({url}) | {focus} |")

    except Exception as exc:
        print(f"Fallback used because GitHub API could not be reached: {exc}")
        for name, focus in FALLBACK_REPOS:
            rows.append(f"| [`{name}`](https://github.com/{USERNAME}/{name}) | {focus} |")

    repo_rows = "\n".join(rows)

    return f"""<!--START:DYNAMIC_PROFILE-->
### Latest Profile Update

- **Last automated update:** {now}
- **Current focus:** Data Science, Linux Labs, Docker, MLOps and Cloud Deployment
- **Active build mode:** Teaching repositories + practical project templates

### Recently Highlighted Repositories

| Repository | Focus |
|---|---|
{repo_rows}
<!--END:DYNAMIC_PROFILE-->"""


def update_readme() -> None:
    with open(README_PATH, "r", encoding="utf-8") as file:
        content = file.read()

    pattern = r"<!--START:DYNAMIC_PROFILE-->.*?<!--END:DYNAMIC_PROFILE-->"
    replacement = build_dynamic_section()

    updated_content, replacements = re.subn(
        pattern,
        replacement,
        content,
        flags=re.DOTALL,
    )

    if replacements == 0:
        raise RuntimeError("Dynamic markers not found in README.md")

    with open(README_PATH, "w", encoding="utf-8") as file:
        file.write(updated_content)

    print("README.md updated successfully.")


if __name__ == "__main__":
    update_readme()
