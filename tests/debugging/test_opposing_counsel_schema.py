#!/usr/bin/env python
"""Test OpposingCounselReview schema generation to debug OpenAI error."""

from wepublic_defender.models.legal_responses import OpposingCounselReview
import json

def test_schema():
    """Check the generated JSON schema for OpposingCounselReview."""
    # Get the JSON schema
    schema = OpposingCounselReview.model_json_schema()

    # Check required fields
    required_fields = schema.get('required', [])
    print("Required fields in schema:")
    for field in required_fields:
        print(f"  - {field}")

    print("\nAll properties in schema:")
    properties = schema.get('properties', {})
    for field_name, field_def in properties.items():
        has_default = 'default' in field_def
        print(f"  - {field_name} (has default: {has_default})")

    print("\nFull schema JSON:")
    print(json.dumps(schema, indent=2))

    # Check if schema follows OpenAI's expected pattern
    print("\n--- Analysis ---")
    print(f"Total properties: {len(properties)}")
    print(f"Required fields: {len(required_fields)}")
    print(f"Optional fields: {len(properties) - len(required_fields)}")

    # Check for any field that might be causing the error
    for field_name in properties:
        if field_name not in required_fields:
            field_def = properties[field_name]
            if 'default' not in field_def and field_def.get('type') in ['array', 'object']:
                print(f"\nWARNING: {field_name} is optional but has no default value!")

if __name__ == "__main__":
    test_schema()