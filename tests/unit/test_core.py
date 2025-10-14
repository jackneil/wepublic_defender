"""
Unit tests for core.py

Tests WePublicDefender class initialization and agent calling.
"""

import pytest
from unittest.mock import patch
from wepublic_defender import WePublicDefender


class TestWePublicDefenderInit:
    """Test WePublicDefender initialization."""

    @patch.dict('os.environ', {'OPENAI_API_KEY': 'test-key', 'XAI_API_KEY': 'test-key'})
    @patch('wepublic_defender.core.OpenAI')
    def test_initialization_loads_configs(self, mock_openai):
        """Test initialization loads all configs."""
        wpd = WePublicDefender()

        assert wpd.llm_config is not None
        assert wpd.review_settings is not None
        assert wpd.token_tracker is not None
        assert wpd.markdown_format_instructions is not None
        assert "RETURN FORMAT: Markdown" in wpd.markdown_format_instructions

    @patch.dict('os.environ', {'OPENAI_API_KEY': 'test-key', 'XAI_API_KEY': 'test-key'})
    @patch('wepublic_defender.core.OpenAI')
    def test_token_tracker_initialized_with_model_configs(self, mock_openai):
        """Test token tracker is initialized with model configurations."""
        wpd = WePublicDefender()

        # Verify token tracker has model configs
        assert wpd.token_tracker is not None
        assert wpd.token_tracker.cfg is not None
        assert len(wpd.token_tracker.cfg) > 0

    @patch.dict('os.environ', {'OPENAI_API_KEY': 'test-key', 'XAI_API_KEY': 'test-key'})
    @patch('wepublic_defender.core.OpenAI')
    def test_clients_created(self, mock_openai):
        """Test OpenAI and Grok clients are created."""
        WePublicDefender()

        # Should have attempted to create clients
        assert mock_openai.call_count >= 1  # Called for both openai and grok

    @patch.dict('os.environ', {}, clear=True)
    @patch('wepublic_defender.core.OpenAI')
    def test_initialization_without_api_keys_warns(self, mock_openai):
        """Test initialization without API keys prints warnings."""
        wpd = WePublicDefender()

        # Should still initialize but clients might be None
        assert wpd is not None


class TestCallAgent:
    """Test call_agent method."""

    @pytest.fixture
    def wpd(self):
        """Create WePublicDefender instance with mocked clients."""
        with patch.dict('os.environ', {'OPENAI_API_KEY': 'test', 'XAI_API_KEY': 'test'}):
            with patch('wepublic_defender.core.OpenAI'):
                return WePublicDefender()

    @pytest.mark.parametrize("agent_type", [
        "strategy",
        "drafter",
        "self_review",
        "citation_verify",
        "opposing_counsel",
        "final_review",
    ])
    @pytest.mark.asyncio
    @patch('wepublic_defender.core.chat_complete')
    async def test_valid_agent_types(self, mock_chat, wpd, agent_type):
        """Test all valid agent types work."""
        # Return valid JSON matching expected schemas
        valid_json_responses = {
            "strategy": '{"next_actions": [], "estimated_timeline": "test", "confidence": 95}',
            "drafter": '{"sections": [], "citations": [], "confidence": 95}',
            "self_review": '{"ready_to_file": true, "iteration": 1, "confidence": 95}',
            "citation_verify": '{"case_name": "Test v. Case", "citation": "123 F.3d 456", "still_good_law": true, "verified_date": "2025-01-01", "confidence": 95}',
            "opposing_counsel": '{"ready_to_file": true, "iteration": 1, "confidence": 95}',
            "final_review": '{"ready_to_file": true, "iteration": 1, "confidence": 95}',
        }

        mock_chat.return_value = {
            "text": valid_json_responses[agent_type],
            "usage": {
                "input": 100,
                "output": 50,
                "cached": 0,
                "service_tier": "auto"
            }
        }

        result = await wpd.call_agent(agent_type, "Test document content", mode="external-llm")

        assert result["agent"] == agent_type
        assert "text" in result  # Should have returned text
        assert result["text"] == valid_json_responses[agent_type]
        # Some agents have multiple models configured, so may be called multiple times
        assert mock_chat.call_count >= 1

    @pytest.mark.asyncio
    async def test_invalid_agent_type_raises(self, wpd):
        """Test invalid agent type raises ValueError or FileNotFoundError."""
        with pytest.raises((ValueError, FileNotFoundError)):
            await wpd.call_agent("nonexistent_agent", "Test document", mode="guidance")

    @pytest.mark.asyncio
    @patch('wepublic_defender.core.chat_complete')
    async def test_override_model_parameter(self, mock_chat, wpd):
        """Test override_model parameter changes which model is used."""
        mock_chat.return_value = {
            "text": '{"ready_to_file": true, "iteration": 1, "confidence": 95}',
            "usage": {"input": 10, "output": 5, "cached": 0}
        }

        await wpd.call_agent("self_review", "Test", mode="external-llm", override_model="grok-4")

        # Verify chat_complete was called with grok-4
        call_kwargs = mock_chat.call_args.kwargs
        assert call_kwargs["model_key"] == "grok-4"

    @pytest.mark.asyncio
    @patch('wepublic_defender.core.chat_complete')
    async def test_override_service_tier_parameter(self, mock_chat, wpd):
        """Test override_service_tier parameter."""
        mock_chat.return_value = {
            "text": '{"ready_to_file": true, "iteration": 1, "confidence": 95}',
            "usage": {"input": 10, "output": 5, "cached": 0}
        }

        await wpd.call_agent("self_review", "Test", mode="external-llm", override_service_tier="priority")

        call_kwargs = mock_chat.call_args.kwargs
        assert call_kwargs["service_tier"] == "priority"

    @pytest.mark.asyncio
    @patch('wepublic_defender.core.chat_complete')
    async def test_override_effort_parameter(self, mock_chat, wpd):
        """Test override_effort parameter."""
        mock_chat.return_value = {
            "text": '{"next_actions": [], "estimated_timeline": "test", "confidence": 95}',
            "usage": {"input": 10, "output": 5, "cached": 0}
        }

        await wpd.call_agent("strategy", "Test", mode="external-llm", override_effort="high")

        call_kwargs = mock_chat.call_args.kwargs
        assert call_kwargs["effort"] == "high"

    @pytest.mark.asyncio
    @patch('wepublic_defender.core.chat_complete')
    async def test_token_tracking(self, mock_chat, wpd):
        """Test that token usage is tracked."""
        mock_chat.return_value = {
            "text": '{"ready_to_file": true, "iteration": 1, "confidence": 95}',
            "usage": {
                "input": 1000,
                "output": 500,
                "cached": 100,
                "service_tier": "standard"
            }
        }

        await wpd.call_agent("self_review", "Test document", mode="external-llm")

        # Verify tokens were added to tracker
        # The usage should be tracked for the model that was called
        assert len(wpd.token_tracker._history) > 0

    @pytest.mark.asyncio
    @patch('wepublic_defender.core.chat_complete')
    async def test_markdown_instructions_in_prompt(self, mock_chat, wpd):
        """Test that markdown format instructions are included in prompt."""
        mock_chat.return_value = {
            "text": '{"sections": [], "citations": [], "confidence": 95}',
            "usage": {"input": 10, "output": 5, "cached": 0}
        }

        await wpd.call_agent("drafter", "Test", mode="external-llm")

        # Verify system message includes markdown instructions
        call_args = mock_chat.call_args
        messages = call_args.kwargs["messages"]
        system_message = messages[0]["content"]

        assert "RETURN FORMAT: Markdown" in system_message or "markdown" in system_message.lower()

    @pytest.mark.asyncio
    @patch('wepublic_defender.core.chat_complete')
    async def test_jurisdiction_context_added(self, mock_chat, wpd):
        """Test that jurisdiction context is added to prompt when provided."""
        mock_chat.return_value = {
            "text": '{"verified": true, "confidence": 95}',
            "usage": {"input": 10, "output": 5, "cached": 0}
        }

        await wpd.call_agent(
            "citation_verify",
            "Test",
            mode="external-llm",
            override_jurisdiction="South Carolina",
            override_court="U.S. District Court"
        )

        # Verify system message includes jurisdiction context
        call_args = mock_chat.call_args
        messages = call_args.kwargs["messages"]
        system_message = messages[0]["content"]

        assert "South Carolina" in system_message or "JURISDICTION" in system_message

    @pytest.mark.asyncio
    @patch('wepublic_defender.core.chat_complete')
    async def test_error_handling(self, mock_chat, wpd):
        """Test error handling when LLM call fails."""
        mock_chat.side_effect = Exception("API Error")

        result = await wpd.call_agent("self_review", "Test", mode="external-llm")

        # Should return error dict instead of raising
        assert "error" in result
        assert "API Error" in result["error"]

    @pytest.mark.asyncio
    @patch('wepublic_defender.core.chat_complete')
    async def test_web_search_parameter(self, mock_chat, wpd):
        """Test web_search parameter is passed through."""
        mock_chat.return_value = {
            "text": '{"verified": true, "confidence": 95}',
            "usage": {"input": 10, "output": 5, "cached": 0}
        }

        result = await wpd.call_agent("citation_verify", "Test", mode="external-llm", web_search=True)

        assert "web_search" in result
        assert result["web_search"] is True


class TestConvertToWord:
    """Test convert_to_word wrapper method."""

    @pytest.fixture
    def wpd(self):
        """Create WePublicDefender instance."""
        with patch.dict('os.environ', {'OPENAI_API_KEY': 'test', 'XAI_API_KEY': 'test'}):
            with patch('wepublic_defender.core.OpenAI'):
                return WePublicDefender()

    @patch('wepublic_defender.core.convert_markdown_to_word')
    def test_convert_to_word_delegates(self, mock_convert, wpd):
        """Test convert_to_word delegates to document_handlers."""
        mock_convert.return_value = "/path/to/output.docx"

        result = wpd.convert_to_word("test.md")

        assert result == "/path/to/output.docx"
        mock_convert.assert_called_once_with("test.md", None, None)

    @patch('wepublic_defender.core.convert_markdown_to_word')
    def test_convert_to_word_with_court_config(self, mock_convert, wpd):
        """Test convert_to_word passes court_config through."""
        court_config = {"case_number": "TEST-123"}

        wpd.convert_to_word("test.md", court_config=court_config)

        mock_convert.assert_called_once()
        call_args = mock_convert.call_args
        assert call_args[0][2] == court_config or call_args[1].get("court_config") == court_config


class TestCostReporting:
    """Test cost reporting methods."""

    @pytest.fixture
    def wpd(self):
        """Create WePublicDefender instance."""
        with patch.dict('os.environ', {'OPENAI_API_KEY': 'test', 'XAI_API_KEY': 'test'}):
            with patch('wepublic_defender.core.OpenAI'):
                return WePublicDefender()

    def test_get_cost_report(self, wpd):
        """Test get_cost_report returns string."""
        # Add some usage
        wpd.token_tracker.add("gpt-5", inp=1000, out=500)

        report = wpd.get_cost_report()

        assert isinstance(report, str)
        assert len(report) > 0

    def test_get_detailed_cost_report(self, wpd):
        """Test get_detailed_cost_report returns detailed string."""
        wpd.token_tracker.add("gpt-5", inp=1000, out=500, notes="test")

        report = wpd.get_detailed_cost_report()

        assert isinstance(report, str)
        assert len(report) > 0

    def test_reset_costs(self, wpd):
        """Test reset_costs clears tracker."""
        wpd.token_tracker.add("gpt-5", inp=1000, out=500)

        wpd.reset_costs()

        assert len(wpd.token_tracker._usage) == 0
        assert len(wpd.token_tracker._history) == 0


class TestBuildJurisdictionContext:
    """Test _build_jurisdiction_context helper method."""

    @pytest.fixture
    def wpd(self):
        """Create WePublicDefender instance."""
        with patch.dict('os.environ', {'OPENAI_API_KEY': 'test', 'XAI_API_KEY': 'test'}):
            with patch('wepublic_defender.core.OpenAI'):
                return WePublicDefender()

    def test_no_jurisdiction_returns_none(self, wpd):
        """Test that no jurisdiction info returns None."""
        result = wpd._build_jurisdiction_context()

        assert result is None

    def test_jurisdiction_context_formatting(self, wpd):
        """Test jurisdiction context is properly formatted."""
        result = wpd._build_jurisdiction_context(
            jurisdiction="South Carolina",
            court="U.S. District Court",
            circuit="Fourth Circuit"
        )

        assert result is not None
        assert "South Carolina" in result
        assert "U.S. District Court" in result
        assert "Fourth Circuit" in result
        assert "JURISDICTION CONTEXT" in result

    def test_preferred_authority_order(self, wpd):
        """Test preferred authority order is included."""
        result = wpd._build_jurisdiction_context(
            jurisdiction="South Carolina",
            preferred_authority_order=["S.C. Supreme Court", "Fourth Circuit", "Other Federal"]
        )

        assert "S.C. Supreme Court" in result
        assert "Fourth Circuit" in result
