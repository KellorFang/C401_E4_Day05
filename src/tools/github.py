"""
GitHub Tool Module
Truy cập và đọc file `README.md` hoặc mã nguồn từ khóa học/dự án Assignment.
"""

import os

def fetch_assignment_repo(repo_url: str) -> str:
    """
    Kéo script code hoặc requirements từ Github URL sinh viên cung cấp.
    
    Args:
        repo_url (str): Link public hoặc private repo có token.
        
    Returns:
        str: Nội dung code hoặc Markdown báo lỗi nếu link hỏng.
    """
    token = os.getenv("GITHUB_TOKEN")
    # TODO: Parse link github
    # TODO: Gọi Github REST API để đọc file text
    return "Dummy context from Github Repo."
