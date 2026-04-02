#!/usr/bin/env python3
"""
HTML to PDF Conversion Script

Features:
- Convert HTML files to PDF
- Support CSS rendering (external CSS, embedded CSS, inline styles)
- Support page break control
- Support custom page size and margins

Usage:
    python html_to_pdf.py input.html
    python html_to_pdf.py input.html --output output.pdf
    python html_to_pdf.py input.html --page-size A4 --margin "2cm 2cm 2cm 2cm"
"""

import argparse
import sys
from pathlib import Path
from weasyprint import HTML, CSS
from weasyprint.text.fonts import FontConfiguration


def parse_args():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(
        description='Convert HTML files to PDF',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s document.html
  %(prog)s document.html --output result.pdf
  %(prog)s document.html --page-size A4 --margin "2cm 2cm 2cm 2cm"
        """
    )
    
    parser.add_argument(
        'input_file',
        type=str,
        help='Path to the input HTML file'
    )
    
    parser.add_argument(
        '-o', '--output',
        type=str,
        default=None,
        help='Path to the output PDF file (default: same as input file with .pdf extension)'
    )
    
    parser.add_argument(
        '-p', '--page-size',
        type=str,
        default='A4',
        choices=['A3', 'A4', 'A5', 'Letter', 'Legal', 'Tabloid'],
        help='Page size (default: A4)'
    )
    
    parser.add_argument(
        '-m', '--margin',
        type=str,
        default='2cm',
        help='Page margins, can be single value or four values (top right bottom left), e.g., "2cm" or "1cm 2cm 1cm 2cm" (default: 2cm)'
    )
    
    parser.add_argument(
        '-e', '--encoding',
        type=str,
        default='utf-8',
        help='HTML file encoding (default: utf-8)'
    )
    
    return parser.parse_args()


def get_page_size_css(page_size: str, margin: str) -> str:
    """Generate CSS for page size and margins"""
    # Parse margins
    margin_parts = margin.split()
    if len(margin_parts) == 1:
        margin_css = margin_parts[0]
    elif len(margin_parts) == 4:
        margin_css = f"{margin_parts[0]} {margin_parts[1]} {margin_parts[2]} {margin_parts[3]}"
    else:
        print(f"Warning: Invalid margin format, using default 2cm")
        margin_css = "2cm"
    
    # Page size mapping
    size_map = {
        'A3': 'A3',
        'A4': 'A4',
        'A5': 'A5',
        'Letter': 'letter',
        'Legal': 'legal',
        'Tabloid': 'tabloid'
    }
    
    return f"""
    @page {{
        size: {size_map.get(page_size, 'A4')};
        margin: {margin_css};
        
        /* Header and footer areas (can be positioned via elements in HTML) */
        @top-left {{
            content: element(header-left);
        }}
        @top-center {{
            content: element(header-center);
        }}
        @top-right {{
            content: element(header-right);
        }}
        @bottom-left {{
            content: element(footer-left);
        }}
        @bottom-center {{
            content: element(footer-center);
        }}
        @bottom-right {{
            content: element(footer-right);
        }}
    }}
    """


def convert_html_to_pdf(input_file: str, output_file: str = None, 
                        page_size: str = 'A4', margin: str = '2cm',
                        encoding: str = 'utf-8'):
    """
    Convert HTML file to PDF
        
    Args:
        input_file: Path to HTML file
        output_file: Path to PDF output (optional)
        page_size: Page size (A3/A4/A5/Letter/Legal/Tabloid)
        margin: Page margins
        encoding: HTML file encoding
    """
    # Check input file
    input_path = Path(input_file)
    if not input_path.exists():
        raise FileNotFoundError(f"HTML file does not exist: {input_file}")
    
    # Determine output path
    if output_file is None:
        output_path = input_path.with_suffix('.pdf')
    else:
        output_path = Path(output_file)
        
    print(f"Converting: {input_path} -> {output_path}")
    
    # Generate page setup CSS
    page_css = get_page_size_css(page_size, margin)
        
    # Configure fonts
    font_config = FontConfiguration()
    
    try:
        # Read HTML file
        html = HTML(filename=str(input_path), encoding=encoding)
        
        # Create CSS object
        css = CSS(string=page_css, font_config=font_config)
        
        # Convert to PDF
        html.write_pdf(
            target=str(output_path),
            stylesheets=[css],
            font_config=font_config
        )
        
        print(f"✓ Conversion successful: {output_path}")
        print(f"  Page size: {page_size}")
        print(f"  Margins: {margin}")
        
        return str(output_path)
        
    except Exception as e:
        raise Exception(f"PDF conversion failed: {str(e)}")


def main():
    """Main function"""
    args = parse_args()
    
    try:
        output_path = convert_html_to_pdf(
            input_file=args.input_file,
            output_file=args.output,
            page_size=args.page_size,
            margin=args.margin,
            encoding=args.encoding
        )
        sys.exit(0)
        
    except FileNotFoundError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
            
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
