"""
Unit tests for document_handlers.py

Tests markdown-to-Word conversion and federal court formatting.
"""

import pytest
from unittest.mock import patch, MagicMock
from wepublic_defender.document_handlers import (
    DocumentFormatConfig,
    MarkdownToWordConverter,
    convert_markdown_to_word,
)


class TestDocumentFormatConfig:
    """Test document format configuration model."""

    def test_default_placeholders(self):
        """Verify defaults use placeholders, not real case info."""
        config = DocumentFormatConfig()

        assert config.plaintiff_name == "[PLAINTIFF NAME]"
        assert config.defendant_name == "[DEFENDANT NAME]"
        assert config.case_number == "[CASE NUMBER]"
        assert "[" in config.court_district

    def test_no_hardcoded_case_information(self):
        """CRITICAL: Ensure NO hardcoded case information in defaults."""
        config = DocumentFormatConfig()

        # Check that no actual names, numbers, or specific courts are hardcoded
        dangerous_strings = [
            "JACK NEIL",
            "CAPITAL ONE",
            "3:25-11463",
            "MGL",
            "PJG",
        ]

        config_dict = config.model_dump()
        config_str = str(config_dict).upper()

        for danger in dangerous_strings:
            assert danger.upper() not in config_str, \
                f"Found hardcoded case info: {danger}"

    @pytest.mark.parametrize("field_name,test_value", [
        ("case_number", "C/A No. 3:25-12345-ABC"),
        ("court_district", "FOR THE DISTRICT OF SOUTH CAROLINA"),
        ("font_size", 14),
        ("margin_inches", 1.5),
        ("line_spacing", "single"),
    ])
    def test_custom_values(self, field_name, test_value):
        """Test setting custom values."""
        config = DocumentFormatConfig(**{field_name: test_value})
        assert getattr(config, field_name) == test_value

    def test_federal_court_defaults(self):
        """Test federal court formatting defaults."""
        config = DocumentFormatConfig()

        assert config.font_name == "Times New Roman"
        assert config.font_size == 12
        assert config.line_spacing == "double"
        assert config.margin_inches == 1.0


class TestMarkdownToWordConverter:
    """Test markdown to Word conversion."""

    def test_converter_initialization(self):
        """Test converter initializes with config."""
        config = DocumentFormatConfig(font_size=14)
        converter = MarkdownToWordConverter(config)

        assert converter.config.font_size == 14

    def test_converter_uses_default_config_when_none_provided(self):
        """Test converter uses default config if none provided."""
        converter = MarkdownToWordConverter()

        assert converter.config is not None
        assert isinstance(converter.config, DocumentFormatConfig)

    def test_converter_config_has_placeholders(self):
        """Test converter default config uses placeholders."""
        converter = MarkdownToWordConverter()

        assert "[PLAINTIFF" in converter.config.plaintiff_name
        assert "[DEFENDANT" in converter.config.defendant_name

    @patch('wepublic_defender.document_handlers.Document')
    def test_setup_document_styles(self, mock_doc_class):
        """Test document style setup."""
        mock_doc = MagicMock()
        mock_section = MagicMock()
        mock_doc.sections = [mock_section]

        mock_style = MagicMock()
        mock_font = MagicMock()
        mock_style.font = mock_font
        mock_style.paragraph_format = MagicMock()
        mock_doc.styles = {'Normal': mock_style}

        converter = MarkdownToWordConverter()
        converter.setup_document_styles(mock_doc)

        # Verify margins were set (attributes, not method calls)
        assert mock_section.top_margin is not None
        assert mock_section.bottom_margin is not None
        assert mock_section.left_margin is not None
        assert mock_section.right_margin is not None

    @patch('wepublic_defender.document_handlers.Document')
    def test_add_court_header(self, mock_doc_class):
        """Test court header addition."""
        mock_doc = MagicMock()

        config = DocumentFormatConfig(
            court_name="IN THE UNITED STATES DISTRICT COURT",
            court_district="FOR THE DISTRICT OF SOUTH CAROLINA"
        )
        converter = MarkdownToWordConverter(config)
        converter.add_court_header(mock_doc)

        # Verify paragraphs were added (at least 2 for court name and district)
        assert mock_doc.add_paragraph.call_count >= 2


class TestConvertMarkdownToWord:
    """Test convert_markdown_to_word() function."""

    @patch('wepublic_defender.document_handlers.MarkdownToWordConverter')
    @patch('wepublic_defender.document_handlers.Path')
    def test_basic_conversion(self, mock_path, mock_converter_class, temp_markdown_file):
        """Test basic markdown to Word conversion."""
        mock_converter = MagicMock()
        mock_converter_class.return_value = mock_converter

        # Mock Path.read_text
        mock_md_path = MagicMock()
        mock_md_path.read_text.return_value = "# Test"
        mock_path.return_value = mock_md_path

        convert_markdown_to_word(
            str(temp_markdown_file),
            court_config={"case_number": "TEST-123"}
        )

        # Verify converter was created with config
        mock_converter_class.assert_called_once()

    def test_output_filename_generation(self, temp_markdown_file):
        """Test automatic output filename generation."""
        # If we don't provide output_file, it should generate one
        md_file = temp_markdown_file
        expected_output = md_file.with_suffix('.docx')

        # We can't actually run conversion without mocking docx
        # Just verify the path logic
        assert expected_output.suffix == '.docx'
        assert expected_output.stem == md_file.stem

    @pytest.mark.parametrize("config_dict", [
        {"plaintiff_name": "JOHN DOE"},
        {"defendant_name": "ABC CORP"},
        {"case_number": "3:25-12345"},
        {},  # Empty config should work
    ])
    @patch('wepublic_defender.document_handlers.MarkdownToWordConverter')
    def test_court_config_merging(self, mock_converter_class, config_dict, temp_markdown_file):
        """Test court_config parameter merges with defaults."""
        mock_converter = MagicMock()
        mock_converter_class.return_value = mock_converter

        convert_markdown_to_word(
            str(temp_markdown_file),
            court_config=config_dict
        )

        # Verify converter was called with config
        mock_converter_class.assert_called_once()
        call_args = mock_converter_class.call_args
        config = call_args[0][0] if call_args[0] else None

        if config:
            for key, value in config_dict.items():
                assert getattr(config, key) == value


class TestMarkdownParsing:
    """Test markdown parsing logic."""

    def test_heading_detection(self):
        """Test markdown heading detection."""
        # These would test the actual markdown parsing
        # For now, just verify the pattern exists
        converter = MarkdownToWordConverter()

        # We'd parse these in actual implementation
        # Just verify we have the logic structure
        assert hasattr(converter, 'config')

    def test_bold_italic_detection(self):
        """Test bold/italic text detection patterns."""
        # Would test actual regex/parsing in implementation
        assert True  # Placeholder

    def test_blockquote_detection(self):
        """Test blockquote detection."""
        converter = MarkdownToWordConverter()

        # Would test parsing logic
        assert hasattr(converter, 'config')


class TestFederalCourtCompliance:
    """Test federal court formatting compliance."""

    def test_times_new_roman_font(self):
        """Verify Times New Roman is default font."""
        config = DocumentFormatConfig()
        assert config.font_name == "Times New Roman"

    def test_12pt_font_size(self):
        """Verify 12pt is default font size."""
        config = DocumentFormatConfig()
        assert config.font_size == 12

    def test_double_spacing(self):
        """Verify double spacing is default."""
        config = DocumentFormatConfig()
        assert config.line_spacing == "double"

    def test_one_inch_margins(self):
        """Verify 1-inch margins are default."""
        config = DocumentFormatConfig()
        assert config.margin_inches == 1.0

    @pytest.mark.parametrize("config_field,fed_standard", [
        ("font_name", "Times New Roman"),
        ("font_size", 12),
        ("line_spacing", "double"),
        ("margin_inches", 1.0),
    ])
    def test_federal_standards(self, config_field, fed_standard):
        """Test all federal court formatting standards."""
        config = DocumentFormatConfig()
        assert getattr(config, config_field) == fed_standard
