# /research Command

Perform legal research on a topic using web search.

## Usage
```
/research [topic]
/research statute of limitations breach of contract South Carolina
/research Fourth Circuit standard for summary judgment
```

## Process

1. **Formulate Search Queries**
   - Break down topic into search queries
   - Include jurisdiction-specific terms
   - Target legal databases (law.cornell.edu, justia.com, etc.)

2. **Execute Web Searches**
   - Use Grok 4 with web search enabled
   - Search multiple sources (web, news, legal databases)
   - Collect relevant cases, statutes, and secondary sources

3. **Analyze Results**
   - Summarize key findings
   - Identify most relevant cases
   - Extract applicable legal rules
   - Note any contrary authority

4. **Save Research**
   - Create markdown file in 06_RESEARCH/
   - Include all citations and sources
   - Add analysis and notes

## Example Output

```
Researching: "statute of limitations breach of contract South Carolina"

Found 8 relevant sources:

KEY FINDINGS:
1. S.C. Code § 15-3-530: 3-year statute of limitations for breach of contract
2. Discovery Rule: SOL starts when plaintiff knew or should have known of breach
3. Continuing Breach Doctrine: Each breach resets the clock

RELEVANT CASES:
- Jones v. Bank of America, 450 S.E.2d 123 (S.C. 2020)
  Holding: Discovery rule applies when defendant conceals breach

- Smith v. Capital One, 380 S.E.2d 456 (S.C. 2018)
  Holding: Continuing breach doctrine applies to ongoing contractual violations

SAVED TO: 06_RESEARCH/statute_of_limitations_contract_SC.md

Cost: $0.85 (web search)
```

## Implementation

```python
from wepublic_defender import WePublicDefender

# Initialize with package config
defender = WePublicDefender()

research_result = await defender.call_agent(
    "research",
    document="",
    web_search=True,
    research_topic=topic
)

# Save to 06_RESEARCH/
filename = f"06_RESEARCH/{topic.replace(' ', '_').lower()}.md"
with open(filename, 'w') as f:
    f.write(research_result['markdown'])
```
