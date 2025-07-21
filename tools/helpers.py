import os
import base64
import requests
from typing import Union
from dotenv import load_dotenv

def get_github_context() -> Union[dict, str]:
    token = os.getenv("GITHUB_ACCESS_TOKEN", "")
    owner_repo = os.getenv("GITHUB_REPOSITORY", "").split("/")
    if len(owner_repo) != 2 or not token:
        return "Missing or invalid environment variables."

    owner, repo = owner_repo
    headers = {
        "Accept": "application/vnd.github+json",
        "Authorization": f"Bearer {token}",
        "X-GitHub-Api-Version": "2022-11-28",
    }

    return {
        "token": token,
        "owner": owner,
        "repo": repo,
        "headers": headers,
        "api_base": f"https://api.github.com/repos/{owner}/{repo}",
    }


def fetch_file_from_github(file_path: str) -> Union[str, None]:
    ctx = get_github_context()
    if isinstance(ctx, str):
        return None  # Error message already handled in helper

    url = f"{ctx['api_base']}/contents/{file_path}"
    res = requests.get(url, headers=ctx["headers"])

    if res.status_code == 200:
        content_encoded = res.json().get("content", "")
        return base64.b64decode(content_encoded).decode("utf-8")
    return None
