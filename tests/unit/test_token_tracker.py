"""
Unit tests for token_tracker.py

Tests the critical pricing logic including:
- OpenAI priority tier pricing (published prices)
- Grok-4-fast tiered pricing (context-based)
- Service tier multipliers (flex, standard, priority)
- Cache discount calculations
- Edge cases
"""

import pytest
from wepublic_defender.models.token_tracker import TokenTracker, TokenUsage


class TestTokenTrackerPricing:
    """Test updated pricing logic with priority tiers and tiered pricing."""

    @pytest.mark.parametrize("service_tier,expected_input_cost,expected_output_cost", [
        ("standard", 0.00125, 0.01000),  # 1K tokens standard: 1000 * $1.25/M, 1000 * $10/M
        ("priority", 0.00250, 0.02000),  # 1K tokens priority (2x): 1000 * $2.50/M, 1000 * $20/M
        ("flex", 0.000625, 0.00500),     # 1K tokens flex (0.5x): 1000 * $0.625/M, 1000 * $5/M
        ("auto", 0.00125, 0.01000),      # 1K tokens auto (same as standard)
    ])
    def test_gpt5_service_tier_pricing(self, mock_config_with_priority_tier,
                                       service_tier, expected_input_cost, expected_output_cost):
        """Test GPT-5 pricing across service tiers with published priority tier prices."""
        tracker = TokenTracker(mock_config_with_priority_tier)
        tracker.add("gpt-5", inp=1000, out=1000, service_tier=service_tier)

        in_cost, cache_cost, out_cost, total, saved = tracker.cost("gpt-5")

        assert abs(in_cost - expected_input_cost) < 1e-6, \
            f"Input cost mismatch for {service_tier}: expected {expected_input_cost}, got {in_cost}"
        assert abs(out_cost - expected_output_cost) < 1e-6, \
            f"Output cost mismatch for {service_tier}: expected {expected_output_cost}, got {out_cost}"

    def test_priority_tier_uses_published_prices_not_multiplier(self, mock_config_with_priority_tier):
        """Verify priority tier uses exact published prices, not multiplier calculation."""
        tracker = TokenTracker(mock_config_with_priority_tier)
        tracker.add("gpt-5", inp=10000, out=5000, service_tier="priority")

        in_cost, _, out_cost, total, _ = tracker.cost("gpt-5")

        # Should use priority_tier prices: $2.50/M input, $20/M output
        # NOT standard * multiplier
        expected_in = 10000 * 2.50 / 1_000_000  # $0.025
        expected_out = 5000 * 20.0 / 1_000_000  # $0.100
        expected_total = expected_in + expected_out  # $0.125

        assert abs(in_cost - expected_in) < 1e-9
        assert abs(out_cost - expected_out) < 1e-9
        assert abs(total - expected_total) < 1e-9

    @pytest.mark.parametrize("inp,out,expected_tier", [
        (50000, 50000, "under"),    # 100K total < 128K threshold
        (100000, 29000, "over"),    # 129K total > 128K threshold
        (64000, 64000, "under"),    # Exactly 128K (at boundary, should use <=)
        (128000, 1, "over"),        # 128001 total > 128K threshold
        (10000, 10000, "under"),    # Small context well under threshold
        (200000, 50000, "over"),    # Large context well over threshold
    ])
    def test_grok4_fast_tiered_pricing(self, mock_config_with_tiered_pricing,
                                       inp, out, expected_tier):
        """Test Grok-4-fast context-based tiered pricing."""
        tracker = TokenTracker(mock_config_with_tiered_pricing)
        tracker.add("grok-4-fast", inp=inp, out=out)

        in_cost, _, out_cost, _, _ = tracker.cost("grok-4-fast")

        if expected_tier == "under":
            # Under 128K threshold: $0.20/M input, $0.50/M output
            expected_in = inp * 0.20 / 1_000_000
            expected_out = out * 0.50 / 1_000_000
        else:
            # Over 128K threshold: $0.50/M input, $1.00/M output
            expected_in = inp * 0.50 / 1_000_000
            expected_out = out * 1.00 / 1_000_000

        assert abs(in_cost - expected_in) < 1e-9, \
            f"Input cost mismatch for {expected_tier} tier: expected {expected_in}, got {in_cost}"
        assert abs(out_cost - expected_out) < 1e-9, \
            f"Output cost mismatch for {expected_tier} tier: expected {expected_out}, got {out_cost}"

    @pytest.mark.parametrize("cached,input_total", [
        (1000, 10000),   # 10% cached
        (5000, 10000),   # 50% cached
        (10000, 10000),  # 100% cached (edge case)
        (0, 10000),      # 0% cached
        (2500, 10000),   # 25% cached
    ])
    def test_cache_discount_calculations(self, mock_config_with_priority_tier, cached, input_total):
        """Test cache cost calculations with various cache ratios for GPT-5 (90% discount)."""
        tracker = TokenTracker(mock_config_with_priority_tier)
        tracker.add("gpt-5", inp=input_total, out=1000, cache=cached)

        in_cost, cache_cost, out_cost, total, saved = tracker.cost("gpt-5")

        # GPT-5: $1.25/M standard, $0.125/M cached (90% discount)
        expected_in = (input_total - cached) * 1.25 / 1_000_000
        expected_cache = cached * 0.125 / 1_000_000
        expected_saved = cached * (1.25 - 0.125) / 1_000_000  # Saved by caching
        expected_out = 1000 * 10.0 / 1_000_000
        expected_total = expected_in + expected_cache + expected_out

        assert abs(in_cost - expected_in) < 1e-9
        assert abs(cache_cost - expected_cache) < 1e-9
        assert abs(saved - expected_saved) < 1e-9
        assert abs(out_cost - expected_out) < 1e-9
        assert abs(total - expected_total) < 1e-9

    def test_priority_tier_with_cache_discount(self, mock_config_with_priority_tier):
        """Test that priority tier applies to both regular and cached tokens."""
        tracker = TokenTracker(mock_config_with_priority_tier)
        # 10K input, 2K cached, 5K output
        tracker.add("gpt-5", inp=10000, out=5000, cache=2000, service_tier="priority")

        in_cost, cache_cost, out_cost, total, saved = tracker.cost("gpt-5")

        # Priority tier: $2.50/M input, $0.250/M cached, $20/M output
        expected_in = (10000 - 2000) * 2.50 / 1_000_000  # 8K uncached
        expected_cache = 2000 * 0.250 / 1_000_000
        expected_out = 5000 * 20.0 / 1_000_000

        assert abs(in_cost - expected_in) < 1e-9
        assert abs(cache_cost - expected_cache) < 1e-9
        assert abs(out_cost - expected_out) < 1e-9

    @pytest.mark.edge_case
    def test_zero_tokens(self, mock_config_with_priority_tier):
        """Edge case: Zero tokens should cost nothing."""
        tracker = TokenTracker(mock_config_with_priority_tier)
        tracker.add("gpt-5", inp=0, out=0, cache=0)

        in_cost, cache_cost, out_cost, total, saved = tracker.cost("gpt-5")

        assert total == 0.0
        assert in_cost == 0.0
        assert out_cost == 0.0
        assert cache_cost == 0.0
        assert saved == 0.0

    @pytest.mark.edge_case
    def test_all_tokens_cached(self, mock_config_with_priority_tier):
        """Edge case: All input tokens are cached."""
        tracker = TokenTracker(mock_config_with_priority_tier)
        tracker.add("gpt-5", inp=5000, out=1000, cache=5000)

        in_cost, cache_cost, out_cost, total, saved = tracker.cost("gpt-5")

        # All input is cached, so in_cost should be 0, only cache_cost applies
        assert in_cost == 0.0
        expected_cache = 5000 * 0.125 / 1_000_000
        expected_out = 1000 * 10.0 / 1_000_000

        assert abs(cache_cost - expected_cache) < 1e-9
        assert abs(out_cost - expected_out) < 1e-9

    @pytest.mark.edge_case
    def test_very_large_token_counts(self, mock_config_with_priority_tier):
        """Edge case: Very large token counts (millions of tokens)."""
        tracker = TokenTracker(mock_config_with_priority_tier)
        # 10M input, 5M output - simulating huge context
        tracker.add("gpt-5", inp=10_000_000, out=5_000_000)

        in_cost, _, out_cost, total, _ = tracker.cost("gpt-5")

        # Should be: 10M * $1.25/M = $12.50, 5M * $10/M = $50
        expected_in = 12.50
        expected_out = 50.0
        expected_total = 62.50

        assert abs(in_cost - expected_in) < 0.01
        assert abs(out_cost - expected_out) < 0.01
        assert abs(total - expected_total) < 0.01

    def test_fallback_to_priority_multiplier(self, mock_config_with_multiplier_fallback):
        """Test fallback to priority_multiplier when priority_tier not available."""
        tracker = TokenTracker(mock_config_with_multiplier_fallback)
        tracker.add("gpt-4o", inp=1000, out=500, service_tier="priority")

        in_cost, _, out_cost, _, _ = tracker.cost("gpt-4o")

        # Should use standard * priority_multiplier (2.0)
        # Standard: $2.50/M input, $10/M output
        # Priority: $5.00/M input, $20/M output
        expected_in = 1000 * 2.50 * 2.0 / 1_000_000
        expected_out = 500 * 10.0 * 2.0 / 1_000_000

        assert abs(in_cost - expected_in) < 1e-9
        assert abs(out_cost - expected_out) < 1e-9

    def test_multiple_usage_events_aggregation(self, mock_config_with_priority_tier):
        """Test that multiple usage events aggregate correctly."""
        tracker = TokenTracker(mock_config_with_priority_tier)

        # Add multiple events
        tracker.add("gpt-5", inp=1000, out=500, service_tier="standard")
        tracker.add("gpt-5", inp=2000, out=1000, service_tier="priority")
        tracker.add("gpt-5", inp=1500, out=750, cache=500, service_tier="standard")

        in_cost, cache_cost, out_cost, total, _ = tracker.cost("gpt-5")

        # Verify total inputs/outputs are aggregated
        usage = tracker.usage("gpt-5")
        assert usage.input == 4500  # 1000 + 2000 + 1500
        assert usage.output == 2250  # 500 + 1000 + 750
        assert usage.cached == 500

    def test_grok_tiered_pricing_with_cache(self, mock_config_with_tiered_pricing):
        """Test Grok-4-fast tiered pricing works correctly with cached tokens."""
        tracker = TokenTracker(mock_config_with_tiered_pricing)
        # Under threshold with cache
        tracker.add("grok-4-fast", inp=50000, out=25000, cache=10000)

        in_cost, cache_cost, out_cost, total, _ = tracker.cost("grok-4-fast")

        # Under 128K threshold: $0.20/M input, $0.05/M cached, $0.50/M output
        expected_in = (50000 - 10000) * 0.20 / 1_000_000  # 40K uncached
        expected_cache = 10000 * 0.05 / 1_000_000
        expected_out = 25000 * 0.50 / 1_000_000

        assert abs(in_cost - expected_in) < 1e-9
        assert abs(cache_cost - expected_cache) < 1e-9
        assert abs(out_cost - expected_out) < 1e-9


class TestTokenUsageModel:
    """Test TokenUsage pydantic model."""

    def test_token_usage_creation(self):
        """Test creating TokenUsage instance."""
        usage = TokenUsage(
            model="gpt-5",
            input=1000,
            output=500,
            cached=100,
            service_tier="standard",
            notes="test usage"
        )

        assert usage.model == "gpt-5"
        assert usage.input == 1000
        assert usage.output == 500
        assert usage.cached == 100
        assert usage.service_tier == "standard"

    def test_token_usage_total_property(self):
        """Test total tokens calculation."""
        usage = TokenUsage(
            model="gpt-5",
            input=1000,
            output=500,
            cached=100
        )

        # Total = input + output - cached
        assert usage.total == 1400

    def test_token_usage_defaults(self):
        """Test TokenUsage default values."""
        usage = TokenUsage()

        assert usage.input == 0
        assert usage.output == 0
        assert usage.cached == 0
        assert usage.service_tier == "auto"
        assert usage.model is None


class TestTokenTrackerAggregation:
    """Test token tracker aggregation and reporting."""

    def test_clear_history(self, sample_llm_config):
        """Test clearing tracker history."""
        tracker = TokenTracker(sample_llm_config)
        tracker.add("gpt-5", inp=1000, out=500)
        tracker.add("grok-4-fast", inp=2000, out=1000)

        tracker.clear()

        assert len(tracker._usage) == 0
        assert len(tracker._history) == 0

    def test_usage_total_aggregates_all_models(self, sample_llm_config):
        """Test usage_total() aggregates across all models."""
        tracker = TokenTracker(sample_llm_config)
        tracker.add("gpt-5", inp=1000, out=500, cache=100)
        tracker.add("grok-4-fast", inp=2000, out=1000, cache=200)
        tracker.add("gpt-5-mini", inp=1500, out=750, cache=150)

        total = tracker.usage_total()

        assert total.input == 4500
        assert total.output == 2250
        assert total.cached == 450

    def test_cost_for_usage(self, mock_config_with_priority_tier):
        """Test cost_for_usage() calculates cost for specific usage event."""
        tracker = TokenTracker(mock_config_with_priority_tier)

        usage = TokenUsage(
            model="gpt-5",
            input=1000,
            output=500,
            cached=0,
            service_tier="standard"
        )

        in_cost, cache_cost, out_cost, total, saved = tracker.cost_for_usage(usage)

        expected_in = 1000 * 1.25 / 1_000_000
        expected_out = 500 * 10.0 / 1_000_000

        assert abs(in_cost - expected_in) < 1e-9
        assert abs(out_cost - expected_out) < 1e-9
