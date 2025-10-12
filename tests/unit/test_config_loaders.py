"""
Unit tests for config/__init__.py

Tests configuration loading, saving, and manipulation functions.
"""

import pytest
import json
from pathlib import Path
from wepublic_defender.config import (
    load_llm_providers,
    load_review_settings,
    get_review_settings_path,
    save_review_settings,
    update_agent_preference,
    get_model_config,
    get_provider_config,
    get_agent_config,
)


class TestConfigLoaders:
    """Test configuration loading functions."""

    def test_llm_providers_structure(self):
        """Verify llm_providers.json has expected structure."""
        config = load_llm_providers()

        assert "llm_providers" in config
        assert "modelConfigurations" in config
        assert "timeoutConfig" in config

        # Verify provider entries
        assert "openai" in config["llm_providers"]
        assert "xai" in config["llm_providers"]

    def test_llm_providers_has_priority_tier_pricing(self):
        """Verify GPT models have priority_tier pricing."""
        config = load_llm_providers()
        models = config["modelConfigurations"]

        # All GPT models should have priority_tier
        for model_name in ["gpt-5", "gpt-5-mini", "gpt-5-nano", "gpt-4o"]:
            assert model_name in models
            assert "priority_tier" in models[model_name], \
                f"{model_name} missing priority_tier"

            tier = models[model_name]["priority_tier"]
            assert "input_token_ppm" in tier
            assert "output_token_ppm" in tier
            assert "input_token_cached_ppm" in tier

    def test_grok_4_fast_has_tiered_pricing(self):
        """Verify grok-4-fast has tiered_pricing structure."""
        config = load_llm_providers()
        grok = config["modelConfigurations"]["grok-4-fast"]

        assert "tiered_pricing" in grok
        tiered = grok["tiered_pricing"]

        assert "threshold_tokens" in tiered
        assert tiered["threshold_tokens"] == 128000

        assert "under_threshold" in tiered
        assert "over_threshold" in tiered

        # Verify both tiers have pricing
        for tier_name in ["under_threshold", "over_threshold"]:
            tier = tiered[tier_name]
            assert "input_token_ppm" in tier
            assert "output_token_ppm" in tier
            assert "input_token_cached_ppm" in tier

    def test_review_settings_structure(self):
        """Verify legal_review_settings.json has expected structure."""
        settings = load_review_settings()

        assert "reviewAgentConfig" in settings
        assert "workflowConfig" in settings

        # Check agent configs exist
        agents = settings["reviewAgentConfig"]
        required_agents = [
            "strategy_agent",
            "drafter_agent",
            "self_review_agent",
            "citation_verifier_agent",
            "opposing_counsel_agent",
            "final_review_agent",
        ]

        for agent in required_agents:
            assert agent in agents, f"Missing {agent} in reviewAgentConfig"

    @pytest.mark.parametrize("model_name", [
        "gpt-5", "gpt-5-mini", "gpt-5-nano", "gpt-4o",
        "grok-4", "grok-4-fast"
    ])
    def test_all_models_have_required_fields(self, model_name):
        """Verify all models have required pricing and capability fields."""
        config = load_llm_providers()
        model = config["modelConfigurations"][model_name]

        # Required pricing fields
        assert "input_token_ppm" in model
        assert "output_token_ppm" in model
        assert "input_token_cached_ppm" in model

        # Required token limit fields
        assert "max_input_tokens" in model
        assert "max_output_tokens" in model

        # Required metadata
        assert "provider" in model
        assert model["provider"] in ["openai", "xai"]


class TestGetModelConfig:
    """Test get_model_config() function."""

    def test_get_gpt5_config(self):
        """Test retrieving GPT-5 configuration."""
        gpt5 = get_model_config("gpt-5")

        assert gpt5["provider"] == "openai"
        assert gpt5["input_token_ppm"] == 1.25
        assert gpt5["output_token_ppm"] == 10.0
        assert "priority_tier" in gpt5

    def test_get_grok_4_fast_config(self):
        """Test retrieving Grok-4-fast configuration."""
        grok = get_model_config("grok-4-fast")

        assert grok["provider"] == "xai"
        assert "tiered_pricing" in grok
        assert grok["max_input_tokens"] == 2000000  # 2M context

    def test_get_model_config_raises_on_invalid(self):
        """Test get_model_config raises KeyError for invalid model."""
        with pytest.raises(KeyError):
            get_model_config("nonexistent-model")


class TestGetProviderConfig:
    """Test get_provider_config() function."""

    def test_get_openai_provider(self):
        """Test retrieving OpenAI provider configuration."""
        openai = get_provider_config("openai")

        assert openai["name"] == "OpenAI"
        assert openai["base_url"] == "https://api.openai.com/v1"
        assert openai["api_key_env_var"] == "OPENAI_API_KEY"
        assert "service_tiers" in openai["supported_features"]

    def test_get_xai_provider(self):
        """Test retrieving xAI provider configuration."""
        xai = get_provider_config("xai")

        assert xai["name"] == "xAI Grok"
        assert xai["base_url"] == "https://api.x.ai/v1"
        assert xai["api_key_env_var"] == "XAI_API_KEY"
        assert xai["supported_features"]["web_search"] is True

    def test_get_provider_config_raises_on_invalid(self):
        """Test get_provider_config raises KeyError for invalid provider."""
        with pytest.raises(KeyError):
            get_provider_config("fake-provider")


class TestGetAgentConfig:
    """Test get_agent_config() function."""

    @pytest.mark.parametrize("agent_name", [
        "strategy_agent",
        "drafter_agent",
        "self_review_agent",
        "citation_verifier_agent",
        "opposing_counsel_agent",
        "final_review_agent",
    ])
    def test_get_valid_agents(self, agent_name):
        """Test retrieving all valid agent configurations."""
        agent = get_agent_config(agent_name)

        assert agent is not None
        # Should have either 'model' or 'models' field
        assert "model" in agent or "models" in agent

    def test_get_agent_config_raises_on_invalid(self):
        """Test get_agent_config raises KeyError for invalid agent."""
        with pytest.raises(KeyError):
            get_agent_config("fake_agent")

        with pytest.raises(KeyError):
            get_agent_config("")


class TestUpdateAgentPreference:
    """Test update_agent_preference() function."""

    def test_update_models_list(self, temp_review_settings_file):
        """Test updating agent models preference."""
        # Update preference
        result = update_agent_preference(
            "strategy_agent",
            models=["grok-4", "gpt-5", "gpt-5-mini"]
        )

        # Verify update
        agent = result["reviewAgentConfig"]["strategy_agent"]
        assert agent["models"] == ["grok-4", "gpt-5", "gpt-5-mini"]

        # Verify file was actually written
        saved_data = json.loads(temp_review_settings_file.read_text())
        assert saved_data["reviewAgentConfig"]["strategy_agent"]["models"] == \
            ["grok-4", "gpt-5", "gpt-5-mini"]

    def test_update_effort_level(self, temp_review_settings_file):
        """Test updating agent effort preference."""
        result = update_agent_preference(
            "self_review_agent",
            effort="high"
        )

        assert result["reviewAgentConfig"]["self_review_agent"]["effort"] == "high"

    def test_update_web_search_flag(self, temp_review_settings_file):
        """Test updating agent web_search preference."""
        result = update_agent_preference(
            "self_review_agent",
            web_search=True
        )

        assert result["reviewAgentConfig"]["self_review_agent"]["web_search"] is True

    def test_update_multiple_fields(self, temp_review_settings_file):
        """Test updating multiple agent fields at once."""
        result = update_agent_preference(
            "citation_verifier_agent",
            models=["gpt-5"],
            effort="high",
            web_search=True
        )

        agent = result["reviewAgentConfig"]["citation_verifier_agent"]
        assert agent["models"] == ["gpt-5"]
        assert agent["effort"] == "high"
        assert agent["web_search"] is True

    def test_update_agent_raises_on_invalid_agent(self, temp_review_settings_file):
        """Test update_agent_preference raises KeyError for invalid agent."""
        with pytest.raises(KeyError, match="Agent not found"):
            update_agent_preference("fake_agent", models=["gpt-5"])


class TestConfigDataIntegrity:
    """Test configuration data integrity and consistency."""

    def test_all_model_prices_are_positive(self):
        """Verify all model prices are positive numbers."""
        config = load_llm_providers()

        for model_name, model_config in config["modelConfigurations"].items():
            assert model_config["input_token_ppm"] > 0
            assert model_config["output_token_ppm"] > 0
            assert model_config["input_token_cached_ppm"] > 0

            # If priority_tier exists, verify prices
            if "priority_tier" in model_config:
                tier = model_config["priority_tier"]
                assert tier["input_token_ppm"] > 0
                assert tier["output_token_ppm"] > 0
                assert tier["input_token_cached_ppm"] > 0

    def test_cached_prices_less_than_regular(self):
        """Verify cached token prices are less than regular prices."""
        config = load_llm_providers()

        for model_name, model_config in config["modelConfigurations"].items():
            assert model_config["input_token_cached_ppm"] < model_config["input_token_ppm"], \
                f"{model_name}: cached price should be less than regular price"

    def test_max_tokens_are_reasonable(self):
        """Verify token limits are within reasonable ranges."""
        config = load_llm_providers()

        for model_name, model_config in config["modelConfigurations"].items():
            # Input tokens should be at least 32K
            assert model_config["max_input_tokens"] >= 32000, \
                f"{model_name}: max_input_tokens too low"

            # Output tokens should be at least 4K
            assert model_config["max_output_tokens"] >= 4000, \
                f"{model_name}: max_output_tokens too low"

    def test_priority_tier_is_more_expensive(self):
        """Verify priority tier costs more than standard tier."""
        config = load_llm_providers()

        for model_name, model_config in config["modelConfigurations"].items():
            if "priority_tier" in model_config:
                tier = model_config["priority_tier"]
                # Priority should cost more than standard
                assert tier["input_token_ppm"] > model_config["input_token_ppm"]
                assert tier["output_token_ppm"] > model_config["output_token_ppm"]
