from typing import Dict
import os
from .init_github_client import init_github_tools


def register_tools(mcp):
    """Register all GitHub tools with the MCP server."""

    @mcp.tool()
    def read_readme_file() -> str:
        """Read the README.md file content from the repository."""
        read_file_tool = init_github_tools()[0]
        if read_file_tool is None:
            return "Read File tool is not initialized. Please initialize GitHub tools first."
        try:
            readme_content = read_file_tool.invoke({"formatted_filepath": "README.md"})
            if "File not found" in readme_content or "404" in readme_content:
                return "README.md file not found in the repository"
            return readme_content
        except Exception as e:
            return f"Error reading README.md: {str(e)}"

    @mcp.tool()
    def get_project_overview() -> str:
        """Get an overview of all files in the main branch of the repository."""
        overview_tool = init_github_tools()[1]
        if overview_tool is None:
            return "Overview tool is not initialized. Please initialize GitHub tools first."
        try:
            overview = overview_tool.invoke({})
            return (
                overview
                + f"\n the project title is {os.getenv('GITHUB_REPOSITORY', 'Unknown Project')}"
            )
        except Exception as e:
            return f"Error getting project overview: {str(e)}"

    @mcp.tool()
    def detect_tech_stack() -> Dict[str, str] | str:
        """Read dependency files to detect technology stack."""
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

        read_file_tool = init_github_tools()[0]
        if read_file_tool is None:
            return "Read File tool is not initialized. Please initialize GitHub tools first."

        tech_stack_files = {}
        for file_name in dependency_files:
            try:
                content = read_file_tool.invoke({"formatted_filepath": file_name})
                if "File not found" not in content and "404" not in content:
                    tech_stack_files[file_name] = content
            except Exception:
                continue

        return tech_stack_files
