"""
Document handlers for converting markdown legal documents to Word format.

Handles markdown-to-DOCX conversion with federal court formatting standards.
"""

from docx import Document
from docx.shared import Pt, Inches
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_LINE_SPACING
from docx.oxml.ns import qn
from docx.oxml import OxmlElement
from pathlib import Path
from typing import Optional, Dict
from pydantic import BaseModel, Field
import re


class DocumentFormatConfig(BaseModel):
    """Configuration for federal court document formatting."""

    court_name: str = Field(
        default="IN THE UNITED STATES DISTRICT COURT",
        description="Name of the court"
    )
    court_district: str = Field(
        default="FOR THE [DISTRICT] OF [STATE]",
        description="Court district (must be provided at runtime)"
    )
    court_division: Optional[str] = Field(
        default=None,
        description="Court division (optional)"
    )
    case_number: str = Field(
        default="[CASE NUMBER]",
        description="Case number (must be provided at runtime)"
    )
    plaintiff_name: str = Field(
        default="[PLAINTIFF NAME]",
        description="Plaintiff name (must be provided at runtime)"
    )
    plaintiff_label: str = Field(
        default="Plaintiff",
        description="Plaintiff label (e.g., 'Plaintiff', 'Petitioner')"
    )
    defendant_name: str = Field(
        default="[DEFENDANT NAME]",
        description="Defendant name (must be provided at runtime)"
    )
    defendant_label: str = Field(
        default="Defendant",
        description="Defendant label (e.g., 'Defendant', 'Respondent')"
    )

    # Formatting options
    font_name: str = "Times New Roman"
    font_size: int = 12
    line_spacing: str = "double"  # "single" or "double"
    margin_inches: float = 1.0


class MarkdownToWordConverter:
    """Convert markdown legal documents to properly formatted Word documents."""

    def __init__(self, format_config: Optional[DocumentFormatConfig] = None):
        """
        Initialize converter with formatting configuration.

        Args:
            format_config: Document formatting configuration. If None, uses defaults.
        """
        self.config = format_config or DocumentFormatConfig()

    def setup_document_styles(self, doc: Document):
        """Set up proper federal court document formatting styles."""
        # Set up margins
        sections = doc.sections
        for section in sections:
            section.top_margin = Inches(self.config.margin_inches)
            section.bottom_margin = Inches(self.config.margin_inches)
            section.left_margin = Inches(self.config.margin_inches)
            section.right_margin = Inches(self.config.margin_inches)

        # Modify Normal style for body text
        style = doc.styles['Normal']
        font = style.font
        font.name = self.config.font_name
        font.size = Pt(self.config.font_size)

        paragraph_format = style.paragraph_format
        if self.config.line_spacing == "double":
            paragraph_format.line_spacing_rule = WD_LINE_SPACING.DOUBLE
        else:
            paragraph_format.line_spacing_rule = WD_LINE_SPACING.SINGLE
        paragraph_format.space_before = Pt(0)
        paragraph_format.space_after = Pt(0)

    def add_court_header(self, doc: Document):
        """Add the standard federal court header - centered and bold."""
        p1 = doc.add_paragraph()
        p1.alignment = WD_ALIGN_PARAGRAPH.CENTER
        run = p1.add_run(self.config.court_name)
        run.bold = True
        run.font.size = Pt(self.config.font_size)
        run.font.name = self.config.font_name

        p2 = doc.add_paragraph()
        p2.alignment = WD_ALIGN_PARAGRAPH.CENTER
        run = p2.add_run(self.config.court_district)
        run.bold = True
        run.font.size = Pt(self.config.font_size)
        run.font.name = self.config.font_name

        if self.config.court_division:
            p3 = doc.add_paragraph()
            p3.alignment = WD_ALIGN_PARAGRAPH.CENTER
            run = p3.add_run(self.config.court_division)
            run.bold = True
            run.font.size = Pt(self.config.font_size)
            run.font.name = self.config.font_name

        # Add single blank line after header
        doc.add_paragraph()

    def add_case_caption(self, doc: Document):
        """Add the case caption with proper party formatting using 2-column table."""
        # Create a table for proper alignment (invisible borders) - 2 columns
        table = doc.add_table(rows=6, cols=2)
        table.autofit = False
        table.allow_autofit = False

        # Set column widths - 2 column layout
        table.columns[0].width = Inches(3.5)  # Party names with closing paren
        table.columns[1].width = Inches(3.0)  # Case number area (centered)

        # Remove all borders
        for row in table.rows:
            for cell in row.cells:
                tcPr = cell._element.get_or_add_tcPr()
                tcBorders = OxmlElement('w:tcBorders')
                for border_name in ['top', 'left', 'bottom', 'right', 'insideH', 'insideV']:
                    border = OxmlElement(f'w:{border_name}')
                    border.set(qn('w:val'), 'none')
                    tcBorders.append(border)
                tcPr.append(tcBorders)

        # Row 0: Plaintiff name
        table.rows[0].cells[0].text = f"{self.config.plaintiff_name}, )"

        # Row 1: Plaintiff designation
        table.rows[1].cells[0].text = f"{self.config.plaintiff_label}, )"

        # Row 2: Blank line before v.
        table.rows[2].cells[0].text = " )"

        # Row 3: v. with case number (centered in right column)
        table.rows[3].cells[0].text = "v. )"
        case_label = table.rows[3].cells[1].paragraphs[0]
        case_label.text = self.config.case_number
        case_label.alignment = WD_ALIGN_PARAGRAPH.CENTER
        case_label.runs[0].bold = True
        case_label.runs[0].font.name = self.config.font_name
        case_label.runs[0].font.size = Pt(self.config.font_size)

        # Row 4: Defendant name
        table.rows[4].cells[0].text = f"{self.config.defendant_name}, )"

        # Row 5: Defendant designation
        table.rows[5].cells[0].text = f"{self.config.defendant_label}. )"

        # Reduce row height for compactness
        for row in table.rows:
            row.height = Inches(0.15)

    def add_document_title(self, doc: Document, title: str):
        """Add the document title - centered, bold, all caps."""
        # Add small space before title
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(6)
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        run = p.add_run(title.upper())
        run.bold = True
        run.font.size = Pt(self.config.font_size)
        run.font.name = self.config.font_name

    def process_markdown_line(self, line: str, doc: Document, in_verification: bool = False) -> bool:
        """
        Process a single markdown line and add it to the document.

        Returns:
            Updated in_verification flag
        """
        # Skip horizontal rules (section dividers in markdown)
        if line.strip() == '---':
            return in_verification

        # Skip title (H1) - handled separately
        if line.startswith('# '):
            return in_verification

        # Handle H2 headings (major sections)
        if line.startswith('## '):
            text = line[3:].strip()
            # Check if this is VERIFICATION section
            if 'VERIFICATION' in text.upper():
                in_verification = True
            p = doc.add_paragraph()
            run = p.add_run(text.upper())
            run.bold = True
            run.font.size = Pt(self.config.font_size)
            run.font.name = self.config.font_name
            p.paragraph_format.space_before = Pt(12)
            p.paragraph_format.space_after = Pt(0)
            return in_verification

        # Handle H3 headings (subsections)
        if line.startswith('### '):
            text = line[4:].strip()
            p = doc.add_paragraph()
            run = p.add_run(text)
            run.bold = True
            run.font.size = Pt(self.config.font_size)
            run.font.name = self.config.font_name
            p.paragraph_format.space_before = Pt(6)
            p.paragraph_format.space_after = Pt(0)
            return in_verification

        # Handle H4 headings (sub-subsections)
        if line.startswith('#### '):
            text = line[5:].strip()
            p = doc.add_paragraph()
            run = p.add_run(text)
            run.bold = True
            run.font.size = Pt(self.config.font_size)
            run.font.name = self.config.font_name
            p.paragraph_format.space_before = Pt(3)
            p.paragraph_format.space_after = Pt(0)
            return in_verification

        # Handle blockquotes (lines starting with >)
        if line.strip().startswith('>'):
            text = line.strip()[1:].strip()  # Remove > and trim
            p = doc.add_paragraph()
            p.paragraph_format.left_indent = Inches(0.5)  # Indent blockquote
            p.paragraph_format.space_before = Pt(6)
            p.paragraph_format.space_after = Pt(6)
            # Process bold/italic in blockquote text
            text = re.sub(r'\*\*(.*?)\*\*', lambda m: f'{{BOLD}}{m.group(1)}{{/BOLD}}', text)
            parts = re.split(r'(\{BOLD\}|\{/BOLD\})', text)
            is_bold = False
            for part in parts:
                if part == '{BOLD}':
                    is_bold = True
                elif part == '{/BOLD}':
                    is_bold = False
                elif part:
                    run = p.add_run(part)
                    run.font.name = self.config.font_name
                    run.font.size = Pt(self.config.font_size)
                    if is_bold:
                        run.bold = True
            return in_verification

        # Handle bullet lists (lines starting with -)
        if line.strip().startswith('- '):
            text = line.strip()[2:]  # Remove - and trim
            p = doc.add_paragraph()
            p.style = 'List Bullet'
            p.paragraph_format.left_indent = Inches(0.25)
            p.paragraph_format.space_before = Pt(0)
            p.paragraph_format.space_after = Pt(0)
            run = p.add_run(text)
            run.font.name = self.config.font_name
            run.font.size = Pt(self.config.font_size)
            return in_verification

        # Skip blank lines - double-spacing handles paragraph separation
        if not line.strip():
            return in_verification

        # Handle signature lines and date lines (with more vertical space)
        if line.strip().startswith('_____') or line.strip().startswith('Dated:') or line.strip().startswith('Executed on'):
            # Add more space before signature lines
            if line.strip().startswith('_____'):
                # Add two blank lines before signature line
                doc.add_paragraph()
                doc.add_paragraph()
            p = doc.add_paragraph(line.strip())
            p.paragraph_format.space_before = Pt(12) if line.strip().startswith('Dated:') or line.strip().startswith('Executed on') else Pt(0)
            return in_verification

        # Handle "Respectfully submitted" (with more vertical space)
        if 'Respectfully submitted' in line:
            # Add three blank lines before "Respectfully submitted"
            doc.add_paragraph()
            doc.add_paragraph()
            doc.add_paragraph()
            p = doc.add_paragraph(line.strip())
            p.paragraph_format.space_before = Pt(12)
            return in_verification

        # Handle regular paragraphs
        p = doc.add_paragraph()

        # For verification section, reduce spacing
        if in_verification:
            p.paragraph_format.line_spacing_rule = WD_LINE_SPACING.SINGLE

        # Process bold and italic markdown
        # First, handle bold+italic (***text***)
        line = re.sub(r'\*\*\*(.*?)\*\*\*', lambda m: f'{{BOLDITALIC}}{m.group(1)}{{/BOLDITALIC}}', line)
        # Then handle bold (**text**)
        line = re.sub(r'\*\*(.*?)\*\*', lambda m: f'{{BOLD}}{m.group(1)}{{/BOLD}}', line)
        # Then handle italic (*text*)
        line = re.sub(r'\*(.*?)\*', lambda m: f'{{ITALIC}}{m.group(1)}{{/ITALIC}}', line)

        # Split by formatting markers and add runs
        parts = re.split(r'(\{BOLD\}|\{/BOLD\}|\{ITALIC\}|\{/ITALIC\}|\{BOLDITALIC\}|\{/BOLDITALIC\})', line)

        bold = False
        italic = False

        for part in parts:
            if part == '{BOLD}':
                bold = True
            elif part == '{/BOLD}':
                bold = False
            elif part == '{ITALIC}':
                italic = True
            elif part == '{/ITALIC}':
                italic = False
            elif part == '{BOLDITALIC}':
                bold = True
                italic = True
            elif part == '{/BOLDITALIC}':
                bold = False
                italic = False
            elif part:
                run = p.add_run(part)
                run.bold = bold
                run.italic = italic
                run.font.name = self.config.font_name
                run.font.size = Pt(self.config.font_size)

        return in_verification

    def convert(self, md_file: str, output_file: Optional[str] = None,
                skip_header: bool = True) -> str:
        """
        Convert a markdown file to a properly formatted Word document.

        Args:
            md_file: Path to markdown file
            output_file: Path for output Word file (optional, defaults to same name with .docx)
            skip_header: If True, skips markdown header section (between --- separators)

        Returns:
            Path to created Word document
        """
        if output_file is None:
            output_file = str(Path(md_file).with_suffix('.docx'))

        print(f"Converting {Path(md_file).name}...")

        # Create document
        doc = Document()

        # Set up styles
        self.setup_document_styles(doc)

        # Add court header
        self.add_court_header(doc)

        # Add case caption
        self.add_case_caption(doc)

        # Read markdown file
        with open(md_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()

        # Extract title from first H1
        title = None
        for line in lines:
            if line.startswith('# '):
                title = line[2:].strip().replace('(Jury Trial Demanded)', '').strip()
                break

        # Add document title
        if title:
            self.add_document_title(doc, title)

        # Skip markdown header section if requested
        start_index = 0
        if skip_header:
            separator_count = 0
            for i, line in enumerate(lines):
                if line.strip() == '---':
                    separator_count += 1
                    if separator_count == 2:
                        start_index = i + 1
                        break

            # Also skip the H2 heading that repeats the document title
            title_upper = title.upper() if title else ""
            if start_index < len(lines):
                next_line = lines[start_index].strip()
                if next_line.startswith('## ') and title_upper in next_line.upper():
                    start_index += 1

        # Process each line starting after the header section
        in_verification = False
        for line in lines[start_index:]:
            in_verification = self.process_markdown_line(line.rstrip('\n'), doc, in_verification)

        # Save document
        doc.save(output_file)
        print(f"[OK] Created {Path(output_file).name}")

        return output_file


def convert_markdown_to_word(
    md_file: str,
    output_file: Optional[str] = None,
    court_config: Optional[Dict] = None
) -> str:
    """
    Convenience function to convert markdown to Word with optional court configuration.

    Args:
        md_file: Path to markdown file
        output_file: Path for output Word file (optional)
        court_config: Dictionary of court configuration values (optional)

    Returns:
        Path to created Word document

    Example:
        >>> convert_markdown_to_word(
        ...     "motion.md",
        ...     court_config={"case_number": "1:25-cv-12345"}
        ... )
    """
    config = DocumentFormatConfig(**court_config) if court_config else None
    converter = MarkdownToWordConverter(format_config=config)
    return converter.convert(md_file, output_file)
