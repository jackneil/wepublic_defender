"""
PDF to Images Converter for Large Legal Documents

This utility converts PDF files (like credit reports, court documents, etc.)
into individual page images so Claude can read them even when the PDF is
too large to process directly.

Usage as CLI:
    wpd-pdf-to-images <path_to_pdf> [--output-dir <dir>] [--dpi <dpi>]

Usage as module:
    from wepublic_defender.utils.pdf_to_images import convert_pdf_to_images
    output_dir = convert_pdf_to_images("credit_report.pdf")

Requirements:
    pip install PyMuPDF (fitz) - Pure Python, no external dependencies!
"""

import argparse
import sys
from pathlib import Path
from typing import Optional

try:
    import fitz  # PyMuPDF
except ImportError as e:
    print(f"Error: Required package not installed: {e}")
    print("\nPlease install PyMuPDF:")
    print("  pip install PyMuPDF")
    print("\nThis is a pure Python package with no external dependencies!")
    sys.exit(1)


def convert_pdf_to_images(
    pdf_path: str,
    output_dir: Optional[str] = None,
    dpi: int = 150,
    image_format: str = "PNG"
) -> Path:
    """
    Convert a PDF file to individual page images.

    Args:
        pdf_path: Path to the PDF file
        output_dir: Directory to save images (if None, creates dir next to PDF)
        dpi: Resolution for the images (higher = better quality but larger files)
        image_format: Image format (PNG, JPEG, etc.)

    Returns:
        Path to the output directory containing the images

    Raises:
        FileNotFoundError: If PDF doesn't exist
        RuntimeError: If poppler is not installed

    Example:
        >>> output_dir = convert_pdf_to_images("credit_report.pdf")
        >>> # Read first page
        >>> from pathlib import Path
        >>> first_page = output_dir / "page_0001.png"
    """
    pdf_path = Path(pdf_path)

    if not pdf_path.exists():
        raise FileNotFoundError(f"PDF not found: {pdf_path}")

    # Create output directory
    if output_dir is None:
        output_dir = pdf_path.parent / f"{pdf_path.stem}_images"
    else:
        output_dir = Path(output_dir)

    output_dir.mkdir(parents=True, exist_ok=True)

    print(f"Converting PDF: {pdf_path}")
    print(f"Output directory: {output_dir}")
    print(f"DPI: {dpi}")
    print(f"Format: {image_format}")
    print()

    try:
        # Open PDF with PyMuPDF
        print("Opening PDF...")
        pdf_document = fitz.open(str(pdf_path))
        total_pages = len(pdf_document)

        print(f"Converting {total_pages} pages to images...")
        print()

        # Convert each page to image
        saved_files = []
        for page_num in range(total_pages):
            page = pdf_document[page_num]

            # Calculate zoom factor for desired DPI
            # Default PDF is 72 DPI, so zoom = desired_dpi / 72
            zoom = dpi / 72.0
            mat = fitz.Matrix(zoom, zoom)

            # Render page to pixmap (image)
            pix = page.get_pixmap(matrix=mat)

            # Save as PNG
            output_path = output_dir / f"page_{page_num + 1:04d}.{image_format.lower()}"

            if image_format.upper() == "PNG":
                pix.save(str(output_path))
            else:
                # For JPEG, convert pixmap
                pix.save(str(output_path), image_format.lower())

            saved_files.append(output_path)
            print(f"  Saved: {output_path.name} (page {page_num + 1}/{total_pages})")

        pdf_document.close()

        print()
        print(f"[SUCCESS] Converted {len(saved_files)} pages")
        print(f"[SUCCESS] Images saved to: {output_dir}")
        print()
        print("You can now read these images using Claude's Read tool")
        print(f"Example: Read(file_path='{output_dir}/page_0001.png')")

        # Create an index file
        index_file = output_dir / "README.txt"
        with open(index_file, 'w', encoding='utf-8') as f:
            f.write(f"PDF to Images Conversion\n")
            f.write(f"========================\n\n")
            f.write(f"Source PDF: {pdf_path}\n")
            f.write(f"Total Pages: {len(saved_files)}\n")
            f.write(f"DPI: {dpi}\n")
            f.write(f"Format: {image_format}\n\n")
            f.write(f"Files:\n")
            for i, file_path in enumerate(saved_files, start=1):
                f.write(f"  Page {i:4d}: {file_path.name}\n")

        print(f"[SUCCESS] Created index file: {index_file.name}")

        return output_dir

    except Exception as e:
        print(f"\n[ERROR] Error during conversion: {e}")
        raise


def main():
    """CLI entry point for wpd-pdf-to-images command."""
    parser = argparse.ArgumentParser(
        description="Convert PDF to images for Claude to read",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Convert with default settings
  wpd-pdf-to-images credit_report.pdf

  # Specify output directory
  wpd-pdf-to-images credit_report.pdf --output-dir F:/images

  # Use higher quality
  wpd-pdf-to-images credit_report.pdf --dpi 300
        """
    )

    parser.add_argument(
        "pdf_path",
        help="Path to the PDF file to convert"
    )

    parser.add_argument(
        "--output-dir",
        help="Directory to save images (default: creates folder next to PDF)"
    )

    parser.add_argument(
        "--dpi",
        type=int,
        default=150,
        help="Resolution for images (default: 150, higher = better quality but larger files)"
    )

    parser.add_argument(
        "--format",
        default="PNG",
        choices=["PNG", "JPEG", "JPG"],
        help="Image format (default: PNG)"
    )

    args = parser.parse_args()

    try:
        output_dir = convert_pdf_to_images(
            pdf_path=args.pdf_path,
            output_dir=args.output_dir,
            dpi=args.dpi,
            image_format=args.format
        )
        return 0
    except Exception as e:
        print(f"\n✗ Error: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
