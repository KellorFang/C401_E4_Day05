"""GitHub Tool — fetches README.md from assignment repos."""

from langchain_core.tools import tool


@tool
def fetch_assignment(repo_url: str) -> str:
    """Fetch the README.md from a GitHub repository to understand assignment
    requirements. Use when a student shares a repo link or asks about an assignment.
    Do NOT use when no repo URL is mentioned."""
    # TODO (Teammate): Implement GitHub REST API call
    # Suggested approach:
    #   1. Parse repo_url to extract owner/repo
    #      e.g. "https://github.com/owner/repo" -> owner, repo
    #   2. Call GitHub REST API: GET /repos/{owner}/{repo}/readme
    #      Headers: {"Authorization": f"token {os.getenv('GITHUB_TOKEN')}"}
    #   3. Decode base64 content from response
    #   4. Return the markdown text
    #   5. Handle errors: 404, private repo, rate limit
    #
    # Teammate's implementation (fetch_github_repo) is available in git history
    # at commit a2749b1 — needs to be adapted to match this interface.
    return f"TODO: Chưa implement — cần kết nối GitHub API. URL: {repo_url}"
