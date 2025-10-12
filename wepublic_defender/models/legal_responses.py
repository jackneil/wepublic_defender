"""
Pydantic models for structured LLM responses in legal review workflows.

These models define the expected structure of responses from various
review agents (citation verification, opposing counsel, document review, etc.).
"""

from pydantic import BaseModel, Field, ConfigDict
from typing import List, Optional, Literal, Dict
from datetime import date


class CitationVerificationResult(BaseModel):
    """Result from citation verification agent checking validity and relevance."""

    case_name: str = Field(..., description="Full case name (e.g., 'Smith v. Jones')")
    citation: str = Field(..., description="Full citation (e.g., '450 S.E.2d 123 (S.C. 2020)')")
    still_good_law: bool = Field(..., description="True if case is still good law and not overruled")
    verified_date: date = Field(..., description="Date verification was performed")
    issues_found: List[str] = Field(
        default_factory=list,
        description="List of issues (overruled, distinguished, incorrect citation, negative treatment, etc.)",
    )
    confidence: int = Field(..., ge=0, le=100, description="Confidence score 0-100")
    notes: Optional[str] = Field(None, description="Additional notes about verification")

    # Relevance and support to our argument
    holding: Optional[str] = Field(
        None, description="One-paragraph plain-English holding relevant to our issue"
    )
    supports_position: Optional[bool] = Field(
        None, description="Does this case support the position we cited it for?"
    )
    supported_propositions: List[str] = Field(
        default_factory=list, description="Specific propositions this case supports"
    )
    contrary_authority: List[str] = Field(
        default_factory=list,
        description="Ways this case may cut against us or how it has been distinguished",
    )
    key_passages: List[str] = Field(
        default_factory=list,
        description="Quoted key language that matters to our issue",
    )
    pin_cites: List[str] = Field(
        default_factory=list, description="Pinpoint citations for key passages"
    )
    relevance: Optional[str] = Field(
        None,
        description="Brief explanation of why (or why not) this case supports our specific argument",
    )
    jurisdiction: Optional[str] = Field(
        None, description="Jurisdiction (e.g., 'South Carolina', 'Fourth Circuit')"
    )
    court: Optional[str] = Field(None, description="Court name (e.g., 'S.C. Sup. Ct.', '4th Cir.')")
    year: Optional[int] = Field(None, description="Decision year if readily available")
    applies_to_sections: List[str] = Field(
        default_factory=list,
        description="Document sections/claims this case supports (e.g., 'Count II – Negligence')",
    )

    # Class-level prompt constant (not included in JSON schema)
    _llm_prompt: str = """
Listen up: You're a citation verification specialist and you WILL NOT screw this up. Your job is to 1) verify legal citations are accurate and still good law and 2) confirm whether the case actually supports the argument we cited it for. If you half-ass this, someone's case gets dismissed. No excuses.

For each citation provided, do ALL of the following - and I mean ALL:
1. Verify the case name and citation formatting (don't you dare skip this)
2. Check for negative treatment (overruled, reversed, distinguished) and whether it's still good law - if you miss that a case got overruled, that's malpractice
3. Summarize the relevant holding in 1 short paragraph - be precise, not vague
4. Determine whether it actually supports the position asserted in our document (supports_position) - don't just assume it does
5. List the specific propositions it supports (supported_propositions) or how it cuts against us (contrary_authority) - be brutally honest
6. Provide 1-3 key quoted passages with pin cites (key_passages, pin_cites) - actual quotes with page numbers, not summaries
7. Identify which sections/claims this case supports (applies_to_sections) if provided
8. Provide an overall confidence score - and be real about your confidence, don't bullshit

Return a CitationVerificationResult object with:
- case_name (str)
- citation (str)
- still_good_law (bool)
- verified_date (date, today)
- issues_found (list[str]) - if you find ANY issues, list them ALL
- confidence (int 0-100)
- notes (str | null)
- holding (str | null)
- supports_position (bool | null)
- supported_propositions (list[str])
- contrary_authority (list[str])
- key_passages (list[str])
- pin_cites (list[str])
- relevance (str | null)
- jurisdiction (str | null)
- court (str | null)
- year (int | null)
- applies_to_sections (list[str])

Use web search to verify current status of cases and to retrieve authoritative summaries. Prefer primary sources, recent decisions, and controlling jurisdictions (South Carolina, Fourth Circuit) when applicable. This is federal court - mistakes have consequences. Do your damn job.
"""


class OpposingCounselReview(BaseModel):
    """Result from opposing counsel simulation attack on legal document."""

    model_config = ConfigDict(extra="forbid")

    class WeaknessFinding(BaseModel):
        """Structured weakness entry for strict JSON schema parsing."""

        model_config = ConfigDict(extra="forbid")

        issue: str = Field(..., description="Brief description of the weakness")
        severity: Literal["critical", "major", "minor"] = Field(
            ..., description='Severity level ("critical", "major", or "minor")'
        )
        explanation: str = Field(
            ..., description="Detailed explanation and how to exploit the weakness"
        )

    class SeverityRatings(BaseModel):
        """Numeric severity ratings by category (0-10)."""

        model_config = ConfigDict(extra="forbid")

        procedural: int = Field(..., ge=0, le=10, description="Procedural defects severity 0-10")
        substantive: int = Field(..., ge=0, le=10, description="Substantive flaws severity 0-10")
        evidentiary: int = Field(..., ge=0, le=10, description="Evidentiary issues severity 0-10")

    weaknesses_found: List[WeaknessFinding] = Field(
        default_factory=list,
        description="List of weaknesses found (issue, severity, explanation)"
    )
    counter_arguments: List[str] = Field(
        default_factory=list,
        description="Potential counter-arguments opposing counsel might raise"
    )
    severity_ratings: SeverityRatings = Field(
        default_factory=lambda: OpposingCounselReview.SeverityRatings(
            procedural=0, substantive=0, evidentiary=0
        ),
        description="Numeric ratings (0-10) by category: procedural, substantive, evidentiary"
    )
    overall_strength: Literal["weak", "moderate", "strong", "ironclad"] = Field(
        ...,
        description="Overall assessment of document strength"
    )
    recommended_revisions: List[str] = Field(
        default_factory=list,
        description="Specific revisions recommended to strengthen document"
    )
    confidence: int = Field(
        ...,
        ge=0,
        le=100,
        description="Confidence in this adversarial review"
    )

    # Class-level prompt constant (not included in JSON schema)
    _llm_prompt: str = """
You are opposing counsel and your goal is to absolutely DESTROY this document. No mercy. Find EVERY weakness, exploit EVERY gap, attack EVERY argument. Someone's paying you to win, and this document better not stand a chance.

Your mission (and you WILL execute it):
1. Find weaknesses in legal arguments - shred them apart
2. Identify procedural defects - even the tiniest technical violations
3. Spot evidentiary problems - inadmissible evidence, hearsay, whatever
4. Generate counter-arguments - make them pay for every claim
5. Rate severity of each issue - be harsh but accurate

For each weakness found, provide:
- issue: Brief description (be specific, not generic)
- severity: "critical", "major", or "minor" (critical means the doc gets tossed)
- explanation: Detailed explanation of the problem and how to exploit it

Return an OpposingCounselReview object with:
- weaknesses_found: List of ALL weaknesses - don't miss a damn thing
- counter_arguments: Arguments opposing counsel would make to destroy this
- severity_ratings: Numeric ratings (0-10) by category - 10 means catastrophic
- overall_strength: Your brutal assessment (weak/moderate/strong/ironclad) - be honest
- recommended_revisions: Specific fixes needed to survive your attack
- confidence: How confident you are in this review

Be ruthlessly aggressive and adversarial. Your job is to find problems and exploit them, period. If you think "oh that's probably fine" - IT'S NOT. Dig deeper.
Use web search to research counter-arguments and recent case law.
If jurisdiction context is provided, prioritize controlling authorities and local procedural requirements for that jurisdiction.
"""


class DocumentReviewResult(BaseModel):
    """Result from document review agent checking legal sufficiency."""

    critical_issues: List[str] = Field(
        default_factory=list,
        description="Critical issues that MUST be fixed (filing would be rejected)"
    )
    major_issues: List[str] = Field(
        default_factory=list,
        description="Major issues that should be fixed (would weaken case)"
    )
    minor_issues: List[str] = Field(
        default_factory=list,
        description="Minor issues (style, formatting, clarity improvements)"
    )
    ready_to_file: bool = Field(
        ...,
        description="True if document meets filing standards (0 critical, <=2 major issues)"
    )
    iteration: int = Field(
        ...,
        description="Which review iteration this is"
    )
    strengths: List[str] = Field(
        default_factory=list,
        description="Strengths of the document"
    )
    confidence: int = Field(
        ...,
        ge=0,
        le=100,
        description="Confidence in this review"
    )
    notes: Optional[str] = Field(
        None,
        description="Additional reviewer notes"
    )

    # Class-level prompt constant (not included in JSON schema)
    _llm_prompt: str = """
You are a senior attorney reviewing a legal document for quality and legal sufficiency. This document will be filed in FEDERAL COURT where judges don't tolerate sloppiness. Your reputation is on the line.

Evaluate the document with extreme scrutiny:
1. Legal sufficiency (arguments supported by law) - vague citations don't count
2. Procedural compliance (proper format, service, etc.) - one violation = document rejected
3. Factual support (claims supported by evidence) - assertions without evidence get struck
4. Clarity and organization - if a judge can't follow it, you lose
5. Citation accuracy - wrong cites = sanctions

Categorize issues by severity (and be honest):
- CRITICAL: Document would be rejected or case dismissed - this is career-ending stuff
- MAJOR: Significantly weakens case or could cause serious problems
- MINOR: Style, formatting, or clarity improvements

Return a DocumentReviewResult object with:
- critical_issues: List of critical problems (if there are ANY, this doc is NOT ready)
- major_issues: List of major problems (more than 2 and you're gambling)
- minor_issues: List of minor improvements
- ready_to_file: True ONLY if 0 critical and <=2 major issues (be conservative)
- iteration: The iteration number provided to you
- strengths: What the document does well (if anything)
- confidence: 0-100 confidence in this review
- notes: Any additional comments

Be thorough and brutally honest. Don't let garbage through just to be nice. Acknowledge actual strengths while identifying real problems. This is federal court - mistakes have consequences.
Use any provided jurisdiction context to prioritize controlling authority and applicable procedures.
"""


class LegalResearchResult(BaseModel):
    """Result from legal research agent performing web search."""

    query: str = Field(
        ...,
        description="The research query that was performed"
    )
    jurisdiction: str = Field(
        ...,
        description="Jurisdiction focus (e.g., 'South Carolina', 'Fourth Circuit')"
    )
    cases: List[Dict[str, str]] = Field(
        default_factory=list,
        description="Relevant cases found. Each dict has 'name', 'citation', 'holding', 'relevance'"
    )
    statutes: List[Dict[str, str]] = Field(
        default_factory=list,
        description="Relevant statutes. Each dict has 'citation', 'title', 'summary', 'relevance'"
    )
    summary: str = Field(
        ...,
        description="1-2 paragraph summary of key findings"
    )
    key_principles: List[str] = Field(
        default_factory=list,
        description="Key legal principles extracted from research"
    )
    contrary_authority: List[str] = Field(
        default_factory=list,
        description="Any contrary authority or unfavorable cases found"
    )
    research_date: date = Field(
        ...,
        description="Date research was performed"
    )
    sources_searched: List[str] = Field(
        default_factory=list,
        description="Sources that were searched (web, news, legal databases)"
    )
    confidence: int = Field(
        ...,
        ge=0,
        le=100,
        description="Confidence in research completeness"
    )

    # Class-level prompt constant (not included in JSON schema)
    _llm_prompt: str = """
You are a legal research specialist and you need to conduct research that will ACTUALLY hold up in court. Half-assed research gets cases dismissed. Period.

For the given research query and jurisdiction, you WILL:
1. Search for relevant case law - controlling authority first, persuasive second
2. Find applicable statutes and regulations - cite them precisely
3. Identify key legal principles - be specific, not generic
4. Look for contrary authority - if you skip this, you're incompetent
5. Synthesize findings into clear summary - 1-2 paragraphs, not an essay

Return a LegalResearchResult object with:
- query: The research query provided
- jurisdiction: The jurisdiction provided
- cases: List of relevant cases with actual holdings (not just names)
- statutes: List of relevant statutes with actual text snippets
- summary: 1-2 paragraph overview of findings (be clear and actionable)
- key_principles: Bullet list of key legal rules (specific, not vague)
- contrary_authority: Any unfavorable cases or arguments (don't hide these)
- research_date: Today's date
- sources_searched: List of sources used (web, news, legal databases, etc.)
- confidence: 0-100 confidence in completeness (be honest about gaps)

Use web search extensively and intelligently. Focus on recent cases and current law - old cases that got overruled are worthless.
Include both favorable AND unfavorable authority. If you only show favorable authority, you're setting up an ambush.
If jurisdiction context is provided, prioritize controlling authorities and relevant local rules for that jurisdiction. This isn't advisory - it's mandatory.
"""


class StrategyRecommendation(BaseModel):
    """Strategic recommendations for case management and next steps."""

    next_actions: List[Dict[str, str]] = Field(
        ...,
        description="Prioritized next actions. Each dict has 'action', 'priority', 'deadline', 'rationale'"
    )
    procedural_concerns: List[str] = Field(
        default_factory=list,
        description="Procedural issues to watch out for (deadlines, local rules, etc.)"
    )
    research_needed: List[str] = Field(
        default_factory=list,
        description="Additional legal research needed"
    )
    strategic_risks: List[str] = Field(
        default_factory=list,
        description="Strategic risks to consider"
    )
    strategic_advantages: List[str] = Field(
        default_factory=list,
        description="Strategic advantages to leverage"
    )
    estimated_timeline: str = Field(
        ...,
        description="Estimated timeline for case progression"
    )
    confidence: int = Field(
        ...,
        ge=0,
        le=100,
        description="Confidence in strategy recommendations"
    )

    # Class-level prompt constant (not included in JSON schema)
    _llm_prompt: str = """
You are a senior litigator providing strategic guidance on case management. Your recommendations better be actionable, or they're worthless.

Analyze the current case status and provide SPECIFIC guidance:
1. Prioritized next actions with actual deadlines - "soon" is not a deadline
2. Procedural concerns and deadlines - missing a deadline = case over
3. Additional research needed - be specific about what topics
4. Strategic risks and how to mitigate - don't just identify risks, solve them
5. Strategic advantages to leverage - find them and exploit them
6. Timeline estimate - realistic, not optimistic bullshit

Return a StrategyRecommendation object with:
- next_actions: List of actions with priority (HIGH/MEDIUM/LOW), actual deadline dates, specific rationale
- procedural_concerns: Specific deadlines, local rules, procedural traps to avoid
- research_needed: Specific topics requiring additional research (not vague categories)
- strategic_risks: Real risks to case strategy with mitigation plans
- strategic_advantages: Actual strengths to emphasize (not generic platitudes)
- estimated_timeline: Realistic overall case timeline estimate
- confidence: 0-100 confidence in recommendations (if you're not at least 80%, say why)

Use web search to verify procedural requirements and recent case trends. Don't guess about deadlines - look them up.
Be specific with deadlines and action items. "File motion" is useless. "File Motion to Dismiss by 2025-11-15 per local Rule 7.1" is useful.
If jurisdiction context is provided, align recommendations with that court's specific rules and controlling authorities. Generic federal advice doesn't cut it.
"""


# Export all models
__all__ = [
    "CitationVerificationResult",
    "OpposingCounselReview",
    "DocumentReviewResult",
    "LegalResearchResult",
    "StrategyRecommendation",
]
