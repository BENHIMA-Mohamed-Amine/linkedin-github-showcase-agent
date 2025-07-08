# Initialize tools first
from langchain_community.utilities.github import GitHubAPIWrapper
from langchain_community.agent_toolkits.github.toolkit import GitHubToolkit
from dotenv import load_dotenv
import os

load_dotenv()

os.environ["GITHUB_APP_ID"] = os.getenv("GITHUB_APP_ID", "")
os.environ["GITHUB_APP_PRIVATE_KEY"] = os.getenv("GITHUB_APP_PRIVATE_KEY", "")
os.environ["GITHUB_REPOSITORY"] = os.getenv("GITHUB_REPOSITORY", "")
os.environ["GOOGLE_API_KEY"] = os.getenv("GOOGLE_API_KEY", "")

# debug the environment variables
# print("GITHUB_APP_ID:", os.getenv("GITHUB_APP_ID"))
# print("GITHUB_REPOSITORY:", os.getenv("GITHUB_REPOSITORY"))
# print("GOOGLE_API_KEY:", os.getenv("GOOGLE_API_KEY"))
# print("GITHUB_APP_PRIVATE_KEY:", os.getenv("GITHUB_APP_PRIVATE_KEY"))  # Print first 10 chars for security
# print(os.getcwd())


def init_github_tools():
    """Initialize GitHub tools from toolkit"""

    github_api = GitHubAPIWrapper()
    toolkit = GitHubToolkit.from_github_api_wrapper(github_api)
    github_tools = toolkit.get_tools()

    read_file_tool = next(
        (tool for tool in github_tools if tool.name == "Read File"), None
    )
    overview_tool = next(
        (
            tool
            for tool in github_tools
            if tool.name == "Overview of existing files in Main branch"
        ),
        None,
    )

    if not read_file_tool or not overview_tool:
        raise ValueError("Required GitHub tools not found")
    return read_file_tool, overview_tool
