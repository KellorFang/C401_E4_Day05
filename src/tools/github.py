"""
GitHub Fetch Tool for LangGraph
Hỗ trợ:
- Public repo
- Private repo (dùng GitHub token)
- Lấy README.md hoặc file cụ thể từ GitHub REST API
"""

import base64
import os
from typing import Optional
from urllib.parse import urlparse

import requests
from dotenv import load_dotenv
from langchain_core.tools import tool

load_dotenv()


def _parse_repo_url(repo_url: str) -> tuple[str, str]:
    """Tách owner/repo từ GitHub URL."""
    cleaned_url = repo_url.strip().rstrip("/")
    if cleaned_url.endswith(".git"):
        cleaned_url = cleaned_url[:-4]

    if cleaned_url.startswith("git@github.com:"):
        repo_path = cleaned_url.split(":", 1)[1]
    else:
        parsed = urlparse(cleaned_url)
        if parsed.netloc not in {"github.com", "www.github.com"}:
            raise ValueError("Repo URL phải thuộc github.com")
        repo_path = parsed.path.lstrip("/")

    parts = repo_path.split("/")
    if len(parts) < 2 or not parts[0] or not parts[1]:
        raise ValueError("Repo URL không hợp lệ")

    return parts[0], parts[1]


@tool
def fetch_github_repo(
    repo_url: str,
    branch: str = "main",
    file_filter: Optional[str] = None,
    github_token: Optional[str] = None,
) -> str:
    """
    Fetch nội dung README.md hoặc file cụ thể từ GitHub repository.

    Args:
        repo_url (str): URL repo GitHub (public hoặc private).
                        Ví dụ: https://github.com/user/repo
        branch (str): Nhánh cần lấy (default: main)
        file_filter (str, optional): Tên file cần lấy, ví dụ "README.md"
        github_token (str, optional): Token nếu repo private

    Returns:
        str: Nội dung markdown/code từ GitHub
    """
    try:
        owner, repo = _parse_repo_url(repo_url)
        access_token = (
            github_token
            or os.getenv("GITHUB_PERSONAL_ACCESS_TOKEN")
            or os.getenv("GITHUB_TOKEN")
        )

        headers = {
            "Accept": "application/vnd.github+json",
            "User-Agent": "langgraph-github-tool",
        }
        if access_token:
            headers["Authorization"] = f"token {access_token}"

        target_file = file_filter.strip("/") if file_filter else "README.md"
        if target_file.lower() in {"readme", "readme.md", "readme.txt", "readme.rst"}:
            api_url = f"https://api.github.com/repos/{owner}/{repo}/readme"
        else:
            api_url = f"https://api.github.com/repos/{owner}/{repo}/contents/{target_file}"

        response = requests.get(api_url, headers=headers, params={"ref": branch}, timeout=20)

        if response.status_code == 404:
            return f"❌ Không tìm thấy repo/file/branch: {owner}/{repo} (branch='{branch}', file='{target_file}')"
        if response.status_code == 401:
            return "❌ GitHub token không hợp lệ hoặc đã hết hạn"
        if response.status_code == 403:
            if response.headers.get("X-RateLimit-Remaining") == "0":
                return "❌ Đã vượt GitHub rate limit. Hãy thử lại sau hoặc cấu hình `GITHUB_TOKEN`."
            return "❌ Bị GitHub từ chối truy cập. Repo có thể là private hoặc token chưa đủ quyền."

        response.raise_for_status()
        data = response.json()

        encoded_content = data.get("content")
        if not encoded_content:
            return "⚠️ GitHub API không trả về nội dung file"

        decoded_content = base64.b64decode(encoded_content).decode("utf-8", errors="replace")
        file_name = data.get("name", target_file)
        html_url = data.get("html_url", repo_url)

        return (
            f"✅ Loaded `{file_name}` from `{owner}/{repo}` on branch `{branch}`\n"
            f"URL: {html_url}\n\n"
            f"{decoded_content[:5000]}"
        )

    except ValueError as e:
        return f"❌ Repo URL không hợp lệ: {str(e)}"
    except requests.RequestException as e:
        return f"❌ Lỗi kết nối GitHub API: {str(e)}"
    except Exception as e:
        return f"❌ Lỗi khi fetch repo: {str(e)}"


if __name__ == "__main__":
    repo_url = "https://github.com/a20-ai-thuc-chien/Day03_2A202600040"
    print(fetch_github_repo.invoke({"repo_url": repo_url, "file_filter": "README.md"}))
