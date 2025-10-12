"""
wepublic_defender - Adversarial Legal Review System

A Python library for AI-powered legal document review with multiple
providers (OpenAI GPT-5, xAI Grok 4) for redundancy and adversarial testing.

Features:
- Multi-AI adversarial review
- Opposing counsel simulation
- Citation verification with web search
- Iterative refinement loops
- Comprehensive cost tracking
- Legal research with web search
- Strategic case planning

Usage:
    from wepublic_defender import WePublicDefender

    defender = WePublicDefender()
    result = await defender.review_document("path/to/motion.docx")
"""

__version__ = "0.1.0"

from .core import WePublicDefender
from .models import TokenUsage, TokenTracker, SettingsManager

__all__ = [
    "WePublicDefender",
    "TokenUsage",
    "TokenTracker",
    "SettingsManager",
]

# Convenience helpers for simple programmatic use (no CLI)
import asyncio
from typing import Optional, Dict, Any


def run_agent_text(agent: str, text: str, **kwargs) -> Dict[str, Any]:
    """
    Run an agent on provided text. Synchronous wrapper around asyncio.

    Example:
        from wepublic_defender import run_agent_text
        result = run_agent_text('self_review', 'hello world')
        print(result.get('text',''))
    """
    async def _runner() -> Dict[str, Any]:
        wpd = WePublicDefender()
        return await wpd.call_agent(agent, text, **kwargs)

    return asyncio.run(_runner())


def run_agent_file(agent: str, file_path: str, encoding: str = "utf-8", **kwargs) -> Dict[str, Any]:
    """
    Run an agent on the contents of a file.

    Example:
        from wepublic_defender import run_agent_file
        result = run_agent_file('self_review', '07_DRAFTS_AND_WORK_PRODUCT/draft.md')
    """
    p = __import__("pathlib").Path(file_path)
    text = p.read_text(encoding=encoding)
    return run_agent_text(agent, text, **kwargs)
