"""Unit tests for the AI Tutor agent core."""

import os
import sys

import pytest

# Add src/ to path so imports work
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from agent import SYSTEM_PROMPT, create_tutor_agent  # noqa: E402


# --- System Prompt Tests ---


class TestSystemPrompt:
    """Verify the system prompt contains all required sections from the spec."""

    def test_has_persona_section(self):
        assert "<persona>" in SYSTEM_PROMPT

    def test_has_rules_section(self):
        assert "<rules>" in SYSTEM_PROMPT

    def test_has_capabilities_section(self):
        assert "<capabilities>" in SYSTEM_PROMPT

    def test_has_constraints_section(self):
        assert "<constraints>" in SYSTEM_PROMPT

    def test_has_output_format_section(self):
        assert "<output_format>" in SYSTEM_PROMPT

    def test_no_fabrication_rule(self):
        assert "NEVER fabricate" in SYSTEM_PROMPT

    def test_citation_requirement(self):
        assert "cite" in SYSTEM_PROMPT.lower() or "Lecture" in SYSTEM_PROMPT

    def test_language_rule(self):
        """Agent must respond in the student's language."""
        assert "language" in SYSTEM_PROMPT.lower()

    def test_no_complete_solutions_constraint(self):
        """Agent must not write full assignment solutions."""
        assert "NEVER write complete code solutions" in SYSTEM_PROMPT

    def test_retry_limit_constraint(self):
        """Agent must stop retrying after 2 failures."""
        assert "2" in SYSTEM_PROMPT and "repeat" in SYSTEM_PROMPT.lower()


# --- Tool Registration Tests ---


class TestToolScaffolds:
    """Verify all tool functions are callable and return strings."""

    def test_search_slides_callable(self):
        from tools.rag import search_slides

        result = search_slides.invoke("test query")
        assert isinstance(result, str)

    def test_search_web_callable(self):
        from tools.web_search import search_web

        result = search_web.invoke("test query")
        assert isinstance(result, str)

    def test_fetch_assignment_callable(self):
        from tools.github import fetch_assignment

        result = fetch_assignment.invoke("https://github.com/test/repo")
        assert isinstance(result, str)

    def test_search_arxiv_callable(self):
        from tools.arxiv_search import search_arxiv

        result = search_arxiv.invoke("test query")
        assert isinstance(result, str)


# --- Agent Creation Tests (requires API key) ---


class TestAgentCreation:
    """Integration tests -- require OPENAI_API_KEY to run."""

    @pytest.mark.skipif(
        not os.getenv("OPENAI_API_KEY"),
        reason="Requires OPENAI_API_KEY",
    )
    def test_create_tutor_agent_returns_agent(self):
        agent = create_tutor_agent()
        assert agent is not None

    @pytest.mark.skipif(
        not os.getenv("OPENAI_API_KEY"),
        reason="Requires OPENAI_API_KEY",
    )
    def test_agent_is_invocable(self):
        agent = create_tutor_agent()
        assert hasattr(agent, "invoke")
