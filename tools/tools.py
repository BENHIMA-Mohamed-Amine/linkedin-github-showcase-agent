from tools.helpers import get_github_context, fetch_file_from_github
from typing import Dict, Union
import os, requests, base64
from dotenv import load_dotenv
load_dotenv()


def register_tools(mcp):
    """Register all GitHub tools with the MCP server."""

    @mcp.tool()
    def get_readme_content() -> str:
        """Get the content of the README.md file from the GitHub repository."""
        ctx = get_github_context()
        if isinstance(ctx, str):
            return ctx  # Return error message

        url = f"{ctx['api_base']}/contents/README.md"

        try:
            response = requests.get(url, headers=ctx['headers'])
            if response.status_code == 200:
                content_encoded = response.json().get("content", "")
                content = base64.b64decode(content_encoded).decode("utf-8")
                return f"# {ctx['owner']}/{ctx['repo']} README.md\n\n{content}"
            else:
                return f"Error: {response.status_code} - {response.text}"
        except Exception as e:
            return f"Exception: {str(e)}"

    @mcp.tool()
    def get_project_overview() -> Union[str, dict]:
        """Get an overview of all files in the main branch of the repository using GitHub API."""
        ctx = get_github_context()
        if isinstance(ctx, str):
            return ctx  # Return error message

        url = f"{ctx['api_base']}/git/trees/main?recursive=1"

        try:
            response = requests.get(url, headers=ctx['headers'])
            if response.status_code == 200:
                tree = response.json().get("tree", [])
                overview = [item["path"] for item in tree]
                return {"overview": overview, "project_title": os.getenv("GITHUB_REPOSITORY", "Unknown Project")}
            else:
                return f"Error: {response.status_code} - {response.text}"
        except Exception as e:
            return f"Exception: {str(e)}"


    @mcp.tool()
    def get_tech_stack() -> Union[Dict[str, str], str]:
        """Detect tech stack using dependency files from GitHub API."""
        dependency_files = [
            "package.json",
            "requirements.txt",
            "Cargo.toml",
            "pom.xml",
            "build.gradle",
            "go.mod",
            "composer.json",
            "Gemfile",
            "poetry.lock",
            "yarn.lock",
            "Pipfile",
        ]

        tech_stack_files = {}
        for file_name in dependency_files:
            content = fetch_file_from_github(file_name)
            if content:
                tech_stack_files[file_name] = content

        return tech_stack_files if tech_stack_files else "No dependency files found."

    @mcp.tool()
    def get_commit_messages_and_comments() -> list[str]:
        """Get commit messages from the GitHub repository."""
        ctx = get_github_context()
        if isinstance(ctx, str):
            print(ctx)
            return []

        url = f"{ctx['api_base'].replace('/contents', '')}/commits"

        try:
            response = requests.get(url, headers=ctx['headers'])
            if response.status_code == 200:
                return [commit["commit"]["message"] for commit in response.json()]
            else:
                print("Error:", response.status_code, response.text)
                return []
        except Exception as e:
            print("Exception:", str(e))
            return []
