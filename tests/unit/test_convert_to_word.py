"""
Unit tests for convert_to_word CLI command.

Tests the wpd-convert-to-word command functionality.
"""

import pytest
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock, call
import json
import sys

from wepublic_defender.cli.convert_to_word import (
    load_overrides_from_args,
    main
)
from wepublic_defender.document_handlers import DocumentFormatConfig, Party


class TestLoadOverridesFromArgs:
    """Test command-line argument processing."""

    def test_no_overrides(self):
        """Test with no command-line overrides."""
        args = Mock(
            court_name=None,
            court_district=None,
            court_division=None,
            case_number=None,
            plaintiff=None,
            defendant=None,
            plaintiff_label=None,
            defendant_label=None,
            font_size=None,
            line_spacing=None,
            margins=None
        )

        overrides = load_overrides_from_args(args)
        assert overrides == {}

    def test_court_overrides(self):
        """Test court information overrides."""
        args = Mock(
            court_name="UNITED STATES DISTRICT COURT",
            court_district="FOR THE DISTRICT OF SOUTH CAROLINA",
            court_division="Charleston Division",
            case_number=None,
            plaintiff=None,
            defendant=None,
            plaintiff_label=None,
            defendant_label=None,
            font_size=None,
            line_spacing=None,
            margins=None
        )

        overrides = load_overrides_from_args(args)
        assert overrides['court_name'] == "UNITED STATES DISTRICT COURT"
        assert overrides['court_district'] == "FOR THE DISTRICT OF SOUTH CAROLINA"
        assert overrides['court_division'] == "Charleston Division"

    def test_party_overrides(self):
        """Test party information overrides."""
        args = Mock(
            court_name=None,
            court_district=None,
            court_division=None,
            case_number="3:25-cv-12345",
            plaintiff="John Doe",
            defendant="ABC Corporation",
            plaintiff_label="Petitioner",
            defendant_label="Respondent",
            font_size=None,
            line_spacing=None,
            margins=None
        )

        overrides = load_overrides_from_args(args)
        assert overrides['case_number'] == "3:25-cv-12345"
        assert len(overrides['plaintiffs']) == 1
        assert overrides['plaintiffs'][0].name == "John Doe"
        assert len(overrides['defendants']) == 1
        assert overrides['defendants'][0].name == "ABC Corporation"
        assert overrides['plaintiff_label'] == "Petitioner"
        assert overrides['defendant_label'] == "Respondent"

    def test_formatting_overrides(self):
        """Test formatting overrides."""
        args = Mock(
            court_name=None,
            court_district=None,
            court_division=None,
            case_number=None,
            plaintiff=None,
            defendant=None,
            plaintiff_label=None,
            defendant_label=None,
            font_size=14,
            line_spacing="single",
            margins=1.5
        )

        overrides = load_overrides_from_args(args)
        assert overrides['font_size'] == 14
        assert overrides['line_spacing'] == "single"
        assert overrides['margin_inches'] == 1.5


class TestMainFunction:
    """Test main() function of convert_to_word CLI."""

    @patch('wepublic_defender.cli.convert_to_word.argparse.ArgumentParser.parse_args')
    @patch('wepublic_defender.cli.convert_to_word.DocumentFormatConfig.from_case_config')
    def test_preview_config_mode(self, mock_from_config, mock_parse_args):
        """Test --preview-config mode."""
        mock_args = Mock(
            preview_config=True,
            config=None,
            court_name=None,
            court_district=None,
            court_division=None,
            case_number=None,
            plaintiff=None,
            defendant=None,
            plaintiff_label=None,
            defendant_label=None,
            font_size=None,
            line_spacing=None,
            margins=None
        )
        mock_parse_args.return_value = mock_args

        mock_config = Mock(
            court_name="TEST COURT",
            court_district="TEST DISTRICT",
            court_division=None,
            case_number="TEST-123",
            plaintiffs=[Party(name="Test Plaintiff", type="individual")],
            defendants=[Party(name="Test Defendant", type="individual")],
            plaintiff_label="Plaintiff",
            defendant_label="Defendant",
            font_name="Times New Roman",
            font_size=12,
            line_spacing="double",
            margin_inches=1.0
        )
        mock_config.model_dump.return_value = {
            'court_name': mock_config.court_name,
            'court_district': mock_config.court_district,
            'case_number': mock_config.case_number,
        }
        mock_from_config.return_value = mock_config

        with patch('builtins.print') as mock_print:
            result = main()

        assert result == 0
        # Verify preview was printed
        print_calls = [str(call) for call in mock_print.call_args_list]
        assert any("Current Configuration" in str(call) for call in print_calls)
        assert any("TEST COURT" in str(call) for call in print_calls)

    @patch('wepublic_defender.cli.convert_to_word.argparse.ArgumentParser.parse_args')
    def test_missing_file_argument(self, mock_parse_args):
        """Test error when --file is missing."""
        mock_args = Mock(
            preview_config=False,
            file=None
        )
        mock_parse_args.return_value = mock_args

        with patch('builtins.print') as mock_print:
            result = main()

        assert result == 1
        print_calls = [str(call) for call in mock_print.call_args_list]
        assert any("Error: --file is required" in str(call) for call in print_calls)

    @patch('wepublic_defender.cli.convert_to_word.argparse.ArgumentParser.parse_args')
    @patch('wepublic_defender.cli.convert_to_word.Path')
    def test_input_file_not_found(self, mock_path_class, mock_parse_args):
        """Test error when input file doesn't exist."""
        mock_args = Mock(
            preview_config=False,
            file="nonexistent.md",
            output=None,
            config=None,
            verbose=False
        )
        mock_parse_args.return_value = mock_args

        mock_path = Mock()
        mock_path.exists.return_value = False
        mock_path_class.return_value = mock_path

        with patch('builtins.print') as mock_print:
            result = main()

        assert result == 1
        print_calls = [str(call) for call in mock_print.call_args_list]
        assert any("Error: Input file not found" in str(call) for call in print_calls)

    @patch('wepublic_defender.cli.convert_to_word.argparse.ArgumentParser.parse_args')
    @patch('wepublic_defender.cli.convert_to_word.Path')
    @patch('wepublic_defender.cli.convert_to_word.DocumentFormatConfig.from_case_config')
    @patch('wepublic_defender.cli.convert_to_word.MarkdownToWordConverter')
    def test_successful_conversion(self, mock_converter_class, mock_from_config,
                                   mock_path_class, mock_parse_args):
        """Test successful document conversion."""
        # Set up arguments
        mock_args = Mock(
            preview_config=False,
            file="test.md",
            output=None,
            config=None,
            verbose=False,
            court_name=None,
            court_district=None,
            court_division=None,
            case_number="TEST-123",
            plaintiff=None,
            defendant=None,
            plaintiff_label=None,
            defendant_label=None,
            font_size=None,
            line_spacing=None,
            margins=None,
            include_header=False,
            skip_header=True
        )
        mock_parse_args.return_value = mock_args

        # Set up Path mocks
        mock_input_path = Mock()
        mock_input_path.exists.return_value = True
        mock_input_path.with_suffix.return_value = Path("test.docx")
        mock_path_class.return_value = mock_input_path

        # Set up config mock
        mock_config = Mock()
        mock_config.model_dump.return_value = {'case_number': 'OLD-123'}
        mock_config.case_number = "TEST-123"
        mock_config.court_district = "FOR THE DISTRICT"
        mock_from_config.return_value = mock_config

        # Set up converter mock
        mock_converter = Mock()
        mock_converter.convert.return_value = "test.docx"
        mock_converter_class.return_value = mock_converter

        with patch('builtins.print') as mock_print:
            result = main()

        assert result == 0
        # Verify converter was called
        mock_converter.convert.assert_called_once()
        # Verify success message
        print_calls = [str(call) for call in mock_print.call_args_list]
        assert any("Successfully converted" in str(call) for call in print_calls)

    @patch('wepublic_defender.cli.convert_to_word.argparse.ArgumentParser.parse_args')
    @patch('wepublic_defender.cli.convert_to_word.Path')
    @patch('wepublic_defender.cli.convert_to_word.DocumentFormatConfig.from_case_config')
    @patch('wepublic_defender.cli.convert_to_word.MarkdownToWordConverter')
    def test_conversion_with_exception(self, mock_converter_class, mock_from_config,
                                        mock_path_class, mock_parse_args):
        """Test error handling during conversion."""
        # Set up arguments
        mock_args = Mock(
            preview_config=False,
            file="test.md",
            output=None,
            config=None,
            verbose=False,
            court_name=None,
            court_district=None,
            court_division=None,
            case_number=None,
            plaintiff=None,
            defendant=None,
            plaintiff_label=None,
            defendant_label=None,
            font_size=None,
            line_spacing=None,
            margins=None,
            include_header=False,
            skip_header=True
        )
        mock_parse_args.return_value = mock_args

        # Set up Path mocks
        mock_input_path = Mock()
        mock_input_path.exists.return_value = True
        mock_input_path.with_suffix.return_value = Path("test.docx")
        mock_path_class.return_value = mock_input_path

        # Set up config mock
        mock_config = Mock()
        mock_config.model_dump.return_value = {}
        mock_from_config.return_value = mock_config

        # Set up converter to raise exception
        mock_converter = Mock()
        mock_converter.convert.side_effect = Exception("Conversion failed")
        mock_converter_class.return_value = mock_converter

        with patch('builtins.print') as mock_print:
            result = main()

        assert result == 1
        # Verify error message
        print_calls = [str(call) for call in mock_print.call_args_list]
        assert any("Error during conversion" in str(call) for call in print_calls)


class TestConfigIntegration:
    """Test configuration loading and merging."""

    def test_config_from_case_config_missing_file(self):
        """Test loading config when case_config.json doesn't exist."""
        with patch('wepublic_defender.document_handlers.Path.cwd') as mock_cwd:
            mock_cwd.return_value = Path("/fake/path")
            config = DocumentFormatConfig.from_case_config()

        # Should return default config
        assert "[PLAINTIFF NAME]" in config.plaintiff_name
        assert "[DEFENDANT NAME]" in config.defendant_name
        assert "[CASE NUMBER]" in config.case_number

    def test_config_from_case_config_with_file(self, tmp_path):
        """Test loading config from actual case_config.json file."""
        # Create temporary case_config.json
        config_data = {
            "court": {
                "name": "TEST COURT",
                "district": "TEST DISTRICT"
            },
            "parties": {
                "plaintiffs": [{"name": "Test Plaintiff", "type": "individual"}],
                "defendants": [{"name": "Test Defendant", "type": "corporation"}]
            },
            "case_number": "TEST-123"
        }

        config_file = tmp_path / "case_config.json"
        config_file.write_text(json.dumps(config_data))

        config = DocumentFormatConfig.from_case_config(config_file)

        assert config.court_name == "TEST COURT"
        assert config.court_district == "TEST DISTRICT"
        assert config.case_number == "TEST-123"
        assert len(config.plaintiffs) == 1
        assert config.plaintiffs[0].name == "Test Plaintiff"
        assert len(config.defendants) == 1
        assert config.defendants[0].name == "Test Defendant"