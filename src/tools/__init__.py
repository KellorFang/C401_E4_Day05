"""Tool registry — re-exports all tools for agent.py to import."""

from tools.rag import search_slides
from tools.web_search import search_web
from tools.github import fetch_assignment
from tools.arxiv_search import search_arxiv

ALL_TOOLS = [search_slides, search_web, fetch_assignment, search_arxiv]
