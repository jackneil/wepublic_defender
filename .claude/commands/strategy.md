# /strategy Command

Generate case strategy recommendations and identify next steps.

## Usage
```
/strategy
```

## Process

1. **Analyze Current Case Status**
   - Review 01_CASE_OVERVIEW/ for case summary
   - Read GAMEPLAN.md for current strategy
   - Check 02_PLEADINGS/ for filed documents
   - Review 03_DISCOVERY/ for discovery status

2. **Call StrategyAgent**
   - Use GPT-5 with web search enabled
   - Provide case context and current status
   - Get strategic recommendations

3. **Generate Action Plan**
   - Prioritized list of next steps
   - Deadlines and procedural requirements
   - Research needs
   - Strategic risks

4. **Update GAMEPLAN.md**
   - Add new action items
   - Update strategy based on recommendations

## Example Output

```
Analyzing case status...

CURRENT STATUS:
- Complaint filed: 2025-01-15
- Answer received: 2025-02-05
- Discovery deadline: 2025-06-01
- Summary judgment deadline: 2025-07-15

NEXT ACTIONS (Prioritized):

1. [HIGH PRIORITY] Serve Discovery Requests
   - Deadline: 2025-04-01 (60 days before discovery close)
   - Rationale: Need bank records and internal communications
   - Estimated effort: 2-3 days

2. [HIGH PRIORITY] Research Summary Judgment Standards
   - Deadline: 2025-05-01 (prep for potential MSJ)
   - Rationale: Strong case on breach of contract count
   - Estimated effort: 1 week

3. [MEDIUM] Draft Motion to Compel (if needed)
   - Deadline: Responsive to their discovery responses
   - Rationale: Expect resistance on internal docs
   - Estimated effort: 3-4 days

PROCEDURAL CONCERNS:
- Verify local rule requirements for summary judgment word limits
- Check if mediation is required before trial

RESEARCH NEEDED:
- SC case law on material breach for banking contracts
- Fourth Circuit standards for punitive damages in SCUTPA cases

Cost: $1.20 (strategy analysis with web search)

Updated GAMEPLAN.md with new action items.
```

## Implementation

```python
from wepublic_defender import WePublicDefender

# Initialize with package config
defender = WePublicDefender()

strategy = await defender.call_agent(
    "strategy",
    document="",
    web_search=True,
    case_summary=read_case_overview(),
    gameplan=read_gameplan()
)

# Update GAMEPLAN.md
update_gameplan_with_strategy(strategy)
```
