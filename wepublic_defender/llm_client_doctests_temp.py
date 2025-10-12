# This file contains the updated _compute_timeout function with doctests
# I'll use this to copy/paste into the actual file

def _compute_timeout(root_cfg: Dict[str, Any], service_tier: str = "auto") -> float:
    """
    Compute a request timeout using the repo's timeoutConfig policy.

    Args:
        root_cfg: Root configuration dict containing timeoutConfig
        service_tier: Service tier ("auto", "flex", "standard", "priority")

    Returns:
        Computed timeout in seconds, capped at maxTimeout

    Examples:
        >>> from typing import Dict, Any
        >>> cfg = {
        ...     "timeoutConfig": {
        ...         "globalDefault": 120,
        ...         "maxTimeout": 600,
        ...         "multipliers": {
        ...             "service_tier": {
        ...                 "flex": 0.5,
        ...                 "standard": 1.0,
        ...                 "priority": 2.0
        ...             }
        ...         }
        ...     }
        ... }
        >>> _compute_timeout(cfg, "standard")
        120.0
        >>> _compute_timeout(cfg, "priority")
        240.0
        >>> _compute_timeout(cfg, "flex")
        60.0

        >>> # Test max timeout cap
        >>> cfg_high = {
        ...     "timeoutConfig": {
        ...         "globalDefault": 500,
        ...         "maxTimeout": 300,
        ...         "multipliers": {"service_tier": {"priority": 2.0}}
        ...     }
        ... }
        >>> _compute_timeout(cfg_high, "priority")
        300.0
    """
    tcfg = root_cfg.get("timeoutConfig", {})
    base = float(tcfg.get("globalDefault", 120))
    mults = tcfg.get("multipliers", {})
    tier_mults = (mults.get("service_tier", {}) or {})
    tier_factor = float(tier_mults.get(service_tier, 1.0))

    # Additional multipliers can be layered here if needed (e.g., file_search)
    timeout = base * tier_factor
    max_timeout = float(tcfg.get("maxTimeout", 43200))
    return min(timeout, max_timeout)
