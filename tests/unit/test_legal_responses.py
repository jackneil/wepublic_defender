"""
Unit tests for legal_responses.py

Tests pydantic models for structured LLM responses.
"""

import pytest
from datetime import date
from pydantic import ValidationError
from wepublic_defender.models.legal_responses import (
    CitationVerificationResult,
    OpposingCounselReview,
    DocumentReviewResult,
    LegalResearchResult,
    StrategyRecommendation,
)


class TestCitationVerificationResult:
    """Test CitationVerificationResult model."""

    def test_valid_instance_creation(self):
        """Test creating valid CitationVerificationResult."""
        result = CitationVerificationResult(
            case_name="Smith v. Jones",
            citation="450 S.E.2d 123 (S.C. 2020)",
            still_good_law=True,
            verified_date=date(2025, 10, 11),
            confidence=95
        )

        assert result.case_name == "Smith v. Jones"
        assert result.citation == "450 S.E.2d 123 (S.C. 2020)"
        assert result.still_good_law is True
        assert result.confidence == 95

    @pytest.mark.parametrize("confidence", [-1, 101, 150, -50])
    def test_confidence_validation(self, confidence):
        """Test confidence must be 0-100."""
        with pytest.raises(ValidationError):
            CitationVerificationResult(
                case_name="Test",
                citation="123",
                still_good_law=True,
                verified_date=date.today(),
                confidence=confidence
            )

    def test_confidence_boundary_values(self):
        """Test confidence at boundaries (0 and 100)."""
        # 0 should work
        result_0 = CitationVerificationResult(
            case_name="Test",
            citation="123",
            still_good_law=True,
            verified_date=date.today(),
            confidence=0
        )
        assert result_0.confidence == 0

        # 100 should work
        result_100 = CitationVerificationResult(
            case_name="Test",
            citation="123",
            still_good_law=True,
            verified_date=date.today(),
            confidence=100
        )
        assert result_100.confidence == 100

    def test_llm_prompt_exists(self):
        """Test _llm_prompt computed field exists and is non-empty."""
        result = CitationVerificationResult(
            case_name="Test",
            citation="123",
            still_good_law=True,
            verified_date=date.today(),
            confidence=90
        )

        assert hasattr(result, '_llm_prompt')
        assert isinstance(result._llm_prompt, str)
        assert len(result._llm_prompt) > 50

    def test_optional_fields_default_to_empty(self):
        """Test optional fields have sensible defaults."""
        result = CitationVerificationResult(
            case_name="Test",
            citation="123",
            still_good_law=True,
            verified_date=date.today(),
            confidence=90
        )

        assert result.issues_found == []
        assert result.notes is None
        assert result.supported_propositions == []


class TestOpposingCounselReview:
    """Test OpposingCounselReview model."""

    def test_valid_instance_creation(self):
        """Test creating valid OpposingCounselReview."""
        review = OpposingCounselReview(
            overall_strength="moderate",
            confidence=85
        )

        assert review.overall_strength == "moderate"
        assert review.confidence == 85

    @pytest.mark.parametrize("strength", [
        "weak", "moderate", "strong", "ironclad"
    ])
    def test_valid_strength_values(self, strength):
        """Test all valid strength values."""
        review = OpposingCounselReview(
            overall_strength=strength,
            confidence=90
        )

        assert review.overall_strength == strength

    def test_invalid_strength_raises(self):
        """Test invalid strength value raises ValidationError."""
        with pytest.raises(ValidationError):
            OpposingCounselReview(
                overall_strength="invalid",
                confidence=90
            )

    def test_llm_prompt_is_aggressive(self):
        """Test _llm_prompt contains aggressive language."""
        review = OpposingCounselReview(
            overall_strength="weak",
            confidence=90
        )

        prompt = review._llm_prompt
        # Should be aggressive/adversarial
        assert len(prompt) > 100
        # Check for adversarial keywords
        prompt_lower = prompt.lower()
        assert any(word in prompt_lower for word in ["attack", "weakness", "opposing", "counter"])


class TestDocumentReviewResult:
    """Test DocumentReviewResult model."""

    def test_valid_instance_creation(self):
        """Test creating valid DocumentReviewResult."""
        result = DocumentReviewResult(
            ready_to_file=False,
            iteration=1,
            confidence=90
        )

        assert result.ready_to_file is False
        assert result.iteration == 1
        assert result.confidence == 90

    def test_issue_lists_default_empty(self):
        """Test issue lists default to empty."""
        result = DocumentReviewResult(
            ready_to_file=True,
            iteration=1,
            confidence=95
        )

        assert result.critical_issues == []
        assert result.major_issues == []
        assert result.minor_issues == []
        assert result.strengths == []

    def test_with_issues(self):
        """Test document with various issues."""
        result = DocumentReviewResult(
            critical_issues=["Missing jurisdiction"],
            major_issues=["Weak argument", "No case law"],
            minor_issues=["Typo in header"],
            ready_to_file=False,
            iteration=1,
            confidence=85
        )

        assert len(result.critical_issues) == 1
        assert len(result.major_issues) == 2
        assert len(result.minor_issues) == 1

    def test_llm_prompt_exists(self):
        """Test _llm_prompt exists."""
        result = DocumentReviewResult(
            ready_to_file=True,
            iteration=1,
            confidence=90
        )

        assert len(result._llm_prompt) > 100


class TestLegalResearchResult:
    """Test LegalResearchResult model."""

    def test_valid_instance_creation(self):
        """Test creating valid LegalResearchResult."""
        result = LegalResearchResult(
            query="statute of limitations breach of contract",
            jurisdiction="South Carolina",
            summary="Found 3-year SOL for breach of contract",
            research_date=date.today(),
            confidence=95
        )

        assert result.query == "statute of limitations breach of contract"
        assert result.jurisdiction == "South Carolina"
        assert result.confidence == 95

    def test_with_cases_and_statutes(self):
        """Test research result with cases and statutes."""
        result = LegalResearchResult(
            query="test query",
            jurisdiction="South Carolina",
            cases=[
                {"name": "Smith v. Jones", "citation": "123", "holding": "Test", "relevance": "High"}
            ],
            statutes=[
                {"citation": "S.C. Code § 123", "title": "Test", "summary": "Test", "relevance": "High"}
            ],
            summary="Test summary",
            research_date=date.today(),
            confidence=90
        )

        assert len(result.cases) == 1
        assert len(result.statutes) == 1

    def test_llm_prompt_mentions_web_search(self):
        """Test _llm_prompt mentions using web search."""
        result = LegalResearchResult(
            query="test",
            jurisdiction="SC",
            summary="test",
            research_date=date.today(),
            confidence=90
        )

        prompt_lower = result._llm_prompt.lower()
        assert "web search" in prompt_lower or "search" in prompt_lower


class TestStrategyRecommendation:
    """Test StrategyRecommendation model."""

    def test_valid_instance_creation(self):
        """Test creating valid StrategyRecommendation."""
        strategy = StrategyRecommendation(
            next_actions=[
                {
                    "action": "File motion",
                    "priority": "HIGH",
                    "deadline": "2025-11-01",
                    "rationale": "Need to respond"
                }
            ],
            estimated_timeline="3-6 months",
            confidence=85
        )

        assert len(strategy.next_actions) == 1
        assert strategy.estimated_timeline == "3-6 months"
        assert strategy.confidence == 85

    def test_lists_default_empty(self):
        """Test list fields default to empty."""
        strategy = StrategyRecommendation(
            next_actions=[],
            estimated_timeline="Unknown",
            confidence=50
        )

        assert strategy.procedural_concerns == []
        assert strategy.research_needed == []
        assert strategy.strategic_risks == []

    def test_llm_prompt_exists(self):
        """Test _llm_prompt exists."""
        strategy = StrategyRecommendation(
            next_actions=[],
            estimated_timeline="test",
            confidence=90
        )

        assert len(strategy._llm_prompt) > 100


class TestAllModelsHaveLLMPrompt:
    """Test all models have _llm_prompt computed field."""

    @pytest.mark.parametrize("model_class,required_fields", [
        (CitationVerificationResult, {
            "case_name": "Test",
            "citation": "123",
            "still_good_law": True,
            "verified_date": date.today(),
            "confidence": 90
        }),
        (OpposingCounselReview, {
            "overall_strength": "moderate",
            "confidence": 90
        }),
        (DocumentReviewResult, {
            "ready_to_file": True,
            "iteration": 1,
            "confidence": 90
        }),
        (LegalResearchResult, {
            "query": "test",
            "jurisdiction": "SC",
            "summary": "test",
            "research_date": date.today(),
            "confidence": 90
        }),
        (StrategyRecommendation, {
            "next_actions": [],
            "estimated_timeline": "test",
            "confidence": 90
        }),
    ])
    def test_model_has_llm_prompt(self, model_class, required_fields):
        """Test model has _llm_prompt computed field."""
        instance = model_class(**required_fields)

        assert hasattr(instance, '_llm_prompt')
        assert isinstance(instance._llm_prompt, str)
        assert len(instance._llm_prompt) > 50
        # Prompt should contain instructions
        assert "you" in instance._llm_prompt.lower() or "your" in instance._llm_prompt.lower()


class TestModelSerialization:
    """Test model serialization to/from JSON."""

    def test_citation_verification_to_dict(self):
        """Test CitationVerificationResult serializes to dict."""
        result = CitationVerificationResult(
            case_name="Test",
            citation="123",
            still_good_law=True,
            verified_date=date(2025, 10, 11),
            confidence=90
        )

        data = result.model_dump()

        assert isinstance(data, dict)
        assert data["case_name"] == "Test"
        assert data["confidence"] == 90

    def test_opposing_counsel_to_dict(self):
        """Test OpposingCounselReview serializes to dict."""
        review = OpposingCounselReview(
            overall_strength="moderate",
            confidence=85,
            weaknesses_found=[
                {"issue": "test", "severity": "major", "explanation": "test"}
            ]
        )

        data = review.model_dump()

        assert isinstance(data, dict)
        assert len(data["weaknesses_found"]) == 1
