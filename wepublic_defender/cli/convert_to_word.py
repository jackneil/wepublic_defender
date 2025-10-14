#!/usr/bin/env python
"""
CLI command for converting markdown legal documents to Word format.

Usage:
    wpd-convert-to-word --file motion.md
    wpd-convert-to-word --file brief.md --output final_brief.docx
    wpd-convert-to-word --file motion.md --case-number "3:25-cv-12345-MGL"
"""

import argparse
import json
import sys
from pathlib import Path
from typing import Optional, Dict, Any

from wepublic_defender.document_handlers import (
    DocumentFormatConfig,
    MarkdownToWordConverter,
    Party
)


def load_overrides_from_args(args) -> Dict[str, Any]:
    """Build configuration overrides from command-line arguments.

    Args:
        args: Parsed command-line arguments

    Returns:
        Dictionary of configuration overrides
    """
    overrides = {}

    # Court information
    if args.court_name:
        overrides['court_name'] = args.court_name
    if args.court_district:
        overrides['court_district'] = args.court_district
    if args.court_division:
        overrides['court_division'] = args.court_division

    # Case number
    if args.case_number:
        overrides['case_number'] = args.case_number

    # Parties
    if args.plaintiff:
        overrides['plaintiffs'] = [Party(name=args.plaintiff, type="individual")]
    if args.defendant:
        overrides['defendants'] = [Party(name=args.defendant, type="individual")]

    # Party labels
    if args.plaintiff_label:
        overrides['plaintiff_label'] = args.plaintiff_label
    if args.defendant_label:
        overrides['defendant_label'] = args.defendant_label

    # Formatting
    if args.font_size:
        overrides['font_size'] = args.font_size
    if args.line_spacing:
        overrides['line_spacing'] = args.line_spacing
    if args.margins:
        overrides['margin_inches'] = args.margins

    return overrides


def main():
    """Main entry point for wpd-convert-to-word command."""
    parser = argparse.ArgumentParser(
        prog='wpd-convert-to-word',
        description='Convert markdown legal documents to properly formatted Word documents',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Basic conversion using case_config.json
  wpd-convert-to-word --file motion.md

  # Specify output file
  wpd-convert-to-word --file brief.md --output final_brief.docx

  # Override case number
  wpd-convert-to-word --file motion.md --case-number "3:25-cv-12345-MGL"

  # Override parties
  wpd-convert-to-word --file motion.md --plaintiff "John Doe" --defendant "ABC Corp"

  # Use custom config file
  wpd-convert-to-word --file motion.md --config my_case_config.json

  # Preview configuration without converting
  wpd-convert-to-word --preview-config
"""
    )

    # Required arguments
    parser.add_argument(
        '--file',
        type=str,
        help='Path to markdown file to convert'
    )

    # Output options
    parser.add_argument(
        '--output',
        type=str,
        help='Output Word file path (default: same name with .docx extension)'
    )

    # Configuration file
    parser.add_argument(
        '--config',
        type=str,
        help='Path to case configuration JSON file (default: .wepublic_defender/case_config.json)'
    )

    # Court information overrides
    parser.add_argument(
        '--court-name',
        type=str,
        help='Override court name'
    )
    parser.add_argument(
        '--court-district',
        type=str,
        help='Override court district'
    )
    parser.add_argument(
        '--court-division',
        type=str,
        help='Override court division'
    )

    # Case information overrides
    parser.add_argument(
        '--case-number',
        type=str,
        help='Override case number'
    )

    # Party overrides (simple single party)
    parser.add_argument(
        '--plaintiff',
        type=str,
        help='Override plaintiff name (for single plaintiff)'
    )
    parser.add_argument(
        '--defendant',
        type=str,
        help='Override defendant name (for single defendant)'
    )
    parser.add_argument(
        '--plaintiff-label',
        type=str,
        help='Override plaintiff label (e.g., Petitioner, Appellant)'
    )
    parser.add_argument(
        '--defendant-label',
        type=str,
        help='Override defendant label (e.g., Respondent, Appellee)'
    )

    # Formatting overrides
    parser.add_argument(
        '--font-size',
        type=int,
        help='Override font size (default: 12)'
    )
    parser.add_argument(
        '--line-spacing',
        choices=['single', 'double'],
        help='Override line spacing'
    )
    parser.add_argument(
        '--margins',
        type=float,
        help='Override margin size in inches (default: 1.0)'
    )

    # Utility options
    parser.add_argument(
        '--preview-config',
        action='store_true',
        help='Preview the configuration that would be used without converting'
    )
    parser.add_argument(
        '--skip-header',
        action='store_true',
        default=True,
        help='Skip markdown header section between --- separators (default: True)'
    )
    parser.add_argument(
        '--include-header',
        action='store_true',
        help='Include markdown header section in output'
    )
    parser.add_argument(
        '--verbose',
        action='store_true',
        help='Show detailed output'
    )

    args = parser.parse_args()

    # Check if preview mode
    if args.preview_config:
        # Load configuration
        if args.config:
            config_path = Path(args.config)
        else:
            config_path = None

        config = DocumentFormatConfig.from_case_config(config_path)

        # Apply overrides
        overrides = load_overrides_from_args(args)
        if overrides:
            # Create new config with overrides
            config_dict = config.model_dump()
            config_dict.update(overrides)
            config = DocumentFormatConfig(**config_dict)

        # Display configuration
        print("Current Configuration:")
        print("-" * 40)
        print(f"Court Name: {config.court_name}")
        print(f"Court District: {config.court_district}")
        if config.court_division:
            print(f"Court Division: {config.court_division}")
        print(f"Case Number: {config.case_number}")
        print(f"\nPlaintiff(s):")
        for p in config.plaintiffs:
            print(f"  - {p.name} ({p.type})")
        print(f"  Label: {config.plaintiff_label}")
        print(f"\nDefendant(s):")
        for d in config.defendants:
            print(f"  - {d.name} ({d.type})")
        print(f"  Label: {config.defendant_label}")
        print(f"\nFormatting:")
        print(f"  Font: {config.font_name} {config.font_size}pt")
        print(f"  Line Spacing: {config.line_spacing}")
        print(f"  Margins: {config.margin_inches} inches")
        print("-" * 40)
        print("\nUse --file <path> to convert a document with this configuration")
        return 0

    # Require file for conversion
    if not args.file:
        print("Error: --file is required for conversion (or use --preview-config)")
        parser.print_help()
        return 1

    # Check input file exists
    input_path = Path(args.file)
    if not input_path.exists():
        print(f"Error: Input file not found: {input_path}")
        return 1

    # Determine output path
    if args.output:
        output_path = Path(args.output)
    else:
        output_path = input_path.with_suffix('.docx')

    # Load configuration
    if args.config:
        config_path = Path(args.config)
        if not config_path.exists():
            print(f"Warning: Config file not found: {config_path}")
            print("Using default configuration...")
            config_path = None
    else:
        config_path = None

    if args.verbose:
        if config_path:
            print(f"Loading configuration from: {config_path}")
        else:
            default_path = Path.cwd() / ".wepublic_defender" / "case_config.json"
            if default_path.exists():
                print(f"Loading configuration from: {default_path}")
            else:
                print("No configuration file found, using defaults")

    # Load base configuration
    config = DocumentFormatConfig.from_case_config(config_path)

    # Apply command-line overrides
    overrides = load_overrides_from_args(args)
    if overrides:
        if args.verbose:
            print(f"Applying overrides: {list(overrides.keys())}")
        config_dict = config.model_dump()
        config_dict.update(overrides)
        config = DocumentFormatConfig(**config_dict)

    # Create converter
    converter = MarkdownToWordConverter(format_config=config)

    # Determine skip_header setting
    skip_header = not args.include_header if args.include_header else args.skip_header

    try:
        # Convert the document
        if args.verbose:
            print(f"Converting {input_path} to {output_path}...")

        output_file = converter.convert(
            str(input_path),
            str(output_path),
            skip_header=skip_header
        )

        print(f"[SUCCESS] Converted to: {output_file}")

        # Display any warnings
        if "[" in config.case_number or "[" in config.court_district:
            print("\n[WARNING] Configuration contains placeholder values")
            print("  Update .wepublic_defender/case_config.json or use command-line overrides")

        return 0

    except Exception as e:
        print(f"Error during conversion: {e}")
        if args.verbose:
            import traceback
            traceback.print_exc()
        return 1


if __name__ == '__main__':
    sys.exit(main())