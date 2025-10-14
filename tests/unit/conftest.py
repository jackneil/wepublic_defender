"""
Pytest fixtures for wepublic_defender unit tests.

Provides reusable test fixtures for:
- Mock configurations (LLM configs, review settings)
- Sample token usage instances
- Temporary files for testing
"""

import pytest
import json
from datetime import date
from wepublic_defender.models.token_tracker import TokenUsage


@pytest.fixture
def sample_llm_config():
    """Sample LLM configuration for testing with priority tier pricing."""
    return {
        "gpt-5": {
            "provider": "openai",
            "input_token_ppm": 1.25,
            "output_token_ppm": 10.0,
            "input_token_cached_ppm": 0.125,
            "max_input_tokens": 272000,
            "max_output_tokens": 128000,
            "cached_discount_percent": 90.0,
            "priority_tier": {
                "input_token_ppm": 2.50,
                "output_token_ppm": 20.0,
                "input_token_cached_ppm": 0.250
            }
        },
        "gpt-5-mini": {
            "provider": "openai",
            "input_token_ppm": 0.25,
            "output_token_ppm": 2.0,
            "input_token_cached_ppm": 0.025,
            "max_input_tokens": 272000,
            "max_output_tokens": 128000,
            "priority_tier": {
                "input_token_ppm": 0.45,
                "output_token_ppm": 3.60,
                "input_token_cached_ppm": 0.045
            }
        },
        "grok-4-fast": {
            "provider": "xai",
            "input_token_ppm": 0.20,
            "output_token_ppm": 0.50,
            "input_token_cached_ppm": 0.05,
            "max_input_tokens": 2000000,
            "max_output_tokens": 100000,
            "tiered_pricing": {
                "threshold_tokens": 128000,
                "under_threshold": {
                    "input_token_ppm": 0.20,
                    "output_token_ppm": 0.50,
                    "input_token_cached_ppm": 0.05
                },
                "over_threshold": {
                    "input_token_ppm": 0.50,
                    "output_token_ppm": 1.00,
                    "input_token_cached_ppm": 0.125
                }
            }
        }
    }


@pytest.fixture
def mock_config_with_priority_tier():
    """Model config with priority_tier pricing (OpenAI models)."""
    return {
        "gpt-5": {
            "provider": "openai",
            "input_token_ppm": 1.25,
            "output_token_ppm": 10.0,
            "input_token_cached_ppm": 0.125,
            "priority_tier": {
                "input_token_ppm": 2.50,
                "output_token_ppm": 20.0,
                "input_token_cached_ppm": 0.250
            }
        }
    }


@pytest.fixture
def mock_config_with_tiered_pricing():
    """Grok-4-fast config with context-based tiered pricing."""
    return {
        "grok-4-fast": {
            "provider": "xai",
            "input_token_ppm": 0.20,
            "output_token_ppm": 0.50,
            "input_token_cached_ppm": 0.05,
            "tiered_pricing": {
                "threshold_tokens": 128000,
                "under_threshold": {
                    "input_token_ppm": 0.20,
                    "output_token_ppm": 0.50,
                    "input_token_cached_ppm": 0.05
                },
                "over_threshold": {
                    "input_token_ppm": 0.50,
                    "output_token_ppm": 1.00,
                    "input_token_cached_ppm": 0.125
                }
            }
        }
    }


@pytest.fixture
def mock_config_with_multiplier_fallback():
    """Config without priority_tier for fallback multiplier testing."""
    return {
        "gpt-4o": {
            "provider": "openai",
            "input_token_ppm": 2.50,
            "output_token_ppm": 10.0,
            "input_token_cached_ppm": 1.25,
            "priority_multiplier": 2.0
        }
    }


@pytest.fixture
def sample_token_usage():
    """Sample TokenUsage instance for testing."""
    return TokenUsage(
        model="gpt-5",
        input=1000,
        output=500,
        cached=100,
        service_tier="standard"
    )


@pytest.fixture
def sample_token_usages():
    """Multiple TokenUsage instances for testing history/aggregation."""
    return [
        TokenUsage(model="gpt-5", input=1000, output=500, cached=100, service_tier="standard"),
        TokenUsage(model="gpt-5", input=2000, output=1000, cached=200, service_tier="priority"),
        TokenUsage(model="grok-4-fast", input=50000, output=25000, cached=5000, service_tier="standard"),
    ]


@pytest.fixture
def temp_markdown_file(tmp_path):
    """Create temporary markdown file for testing."""
    md_file = tmp_path / "test_document.md"
    md_file.write_text("""# Motion to Dismiss

## INTRODUCTION

This is a test document for the court.

## ARGUMENT

### First Point

1. Item one
2. Item two

**Bold text** and *italic text* for case names like *Smith v. Jones*.

> This is a blockquote

### Second Point

More content here.

## CONCLUSION

Request for relief.
""")
    return md_file


@pytest.fixture
def temp_review_settings_file(tmp_path, monkeypatch):
    """Create temporary review settings JSON for testing."""
    settings_file = tmp_path / "legal_review_settings.json"
    settings_data = {
        "reviewAgentConfig": {
            "strategy_agent": {
                "models": ["gpt-5", "grok-4"],
                "effort": "high",
                "web_search": True
            },
            "self_review_agent": {
                "models": ["gpt-5-mini"],
                "effort": "medium",
                "web_search": False
            },
            "citation_verifier_agent": {
                "models": ["grok-4", "gpt-5"],
                "effort": "high",
                "web_search": True
            }
        },
        "workflowConfig": {
            "service_tier": "auto",
            "default_effort": "medium"
        }
    }
    settings_file.write_text(json.dumps(settings_data, indent=2))

    # Monkeypatch both load and save paths
    monkeypatch.setattr(
        "wepublic_defender.config._case_settings_dir",
        lambda: tmp_path
    )

    return settings_file


@pytest.fixture
def sample_citation_data():
    """Sample citation verification data for testing."""
    return {
        "case_name": "Smith v. Jones",
        "citation": "450 S.E.2d 123 (S.C. 2020)",
        "still_good_law": True,
        "verified_date": date(2025, 10, 11),
        "confidence": 95,
        "issues_found": [],
        "notes": "Case verified through legal database"
    }


@pytest.fixture
def sample_court_config():
    """Sample court configuration for document formatting."""
    return {
        "court_name": "IN THE UNITED STATES DISTRICT COURT",
        "court_district": "FOR THE DISTRICT OF SOUTH CAROLINA",
        "court_division": "CHARLESTON DIVISION",
        "case_number": "C/A No. 3:25-12345-ABC",
        "plaintiff_name": "JOHN DOE",
        "plaintiff_label": "Plaintiff",
        "defendant_name": "ABC CORPORATION",
        "defendant_label": "Defendant"
    }
