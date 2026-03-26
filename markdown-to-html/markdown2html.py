#!/usr/bin/env python3
"""markdown-to-html: Convert Markdown to styled HTML with Table support.

This module provides a zero-dependency Markdown to HTML converter with embedded CSS styling.
No external libraries needed — uses only Python's standard library.
"""

import sys
import argparse
import re
import html as html_mod
from dataclasses import dataclass, field
from typing import Optional


# =============================================================================
# CSS Styles
# =============================================================================

@dataclass
class Theme:
    """Represents a color theme for the HTML output."""
    name: str
    css: str


LIGHT_THEME = Theme(
    name="light",
    css="""
/* 引入 PrismJS 语法高亮主题 (Tomorrow Night) */
@import url('https://cdn.staticfile.org/prism/1.29.0/themes/prism-tomorrow.min.css');

body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Helvetica, Arial, sans-serif; max-width: 900px; margin: 2rem auto; padding: 0 1rem; line-height: 1.6; color: #24292e; background: #fff; }
h1,h2,h3,h4,h5,h6 { margin-top: 1.5em; margin-bottom: 0.5em; border-bottom: 1px solid #eaecef; padding-bottom: 0.3em; }
h1 { font-size: 2em; } h2 { font-size: 1.5em; }
code { background: #f6f8fa; padding: 0.2em 0.4em; border-radius: 3px; font-size: 85%; font-family: SFMono-Regular, Consolas, Liberation Mono, Menlo, monospace; }
pre {
    background: linear-gradient(145deg, #2d3748 0%, #1a202c 100%);
    padding: 1.2em;
    border-radius: 8px;
    overflow-x: auto;
    border: 1px solid #4a5568;
    box-shadow: 0 4px 12px rgba(0,0,0,0.15);
    position: relative;
    margin: 1em 0;
}
pre code {
    background: none;
    padding: 0;
    border: none;
    display: block;
    line-height: 1.5;
    font-family: SFMono-Regular, Consolas, Liberation Mono, Menlo, monospace;
    font-size: 14px;
    color: #e2e8f0;
}
pre::before {
    content: attr(data-lang);
    position: absolute;
    top: 0.3em;
    right: 0.5em;
    font-size: 0.75em;
    color: #a0aec0;
    background: rgba(0,0,0,0.3);
    padding: 0.2em 0.5em;
    border-radius: 4px;
    font-weight: 600;
    z-index: 1;
}
/* 覆盖 PrismJS 默认样式 */
pre[class*="language-"] {
    background: linear-gradient(145deg, #2d3748 0%, #1a202c 100%) !important;
    box-shadow: 0 4px 12px rgba(0,0,0,0.15) !important;
    border: 1px solid #4a5568 !important;
}
blockquote { border-left: 4px solid #dfe2e5; margin: 0; padding: 0.5em 1em; color: #6a737d; background: #fafbfc; }
table { border-collapse: collapse; width: 100%; margin: 1.5em 0; display: block; overflow-x: auto; }
th, td { border: 1px solid #dfe2e5; padding: 8px 12px; text-align: left; }
th { background: #f6f8fa; font-weight: 600; white-space: nowrap; }
tr:nth-child(even) { background-color: #fbfbfb; }
tr:hover { background-color: #f6f8fa; }
img { max-width: 100%; }
a { color: #0366d6; text-decoration: none; }
a:hover { text-decoration: underline; }
hr { border: none; border-top: 2px solid #eaecef; margin: 2em 0; }
ul, ol { padding-left: 2em; }
/* Utility classes for report status */
.status-critical { color: #cb2431; font-weight: bold; }
.status-major { color: #d73a49; font-weight: bold; }
.status-ok { color: #22863a; font-weight: bold; }
"""
)

DARK_THEME = Theme(
    name="dark",
    css="""
/* 引入 PrismJS 语法高亮主题 (Tomorrow Night) */
@import url('https://cdn.staticfile.org/prism/1.29.0/themes/prism-tomorrow.min.css');

body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Helvetica, Arial, sans-serif; max-width: 900px; margin: 2rem auto; padding: 0 1rem; line-height: 1.6; color: #c9d1d9; background: #0d1117; }
h1,h2,h3,h4,h5,h6 { margin-top: 1.5em; margin-bottom: 0.5em; border-bottom: 1px solid #21262d; padding-bottom: 0.3em; }
code { background: #161b22; padding: 0.2em 0.4em; border-radius: 3px; font-size: 85%; font-family: SFMono-Regular, Consolas, Liberation Mono, Menlo, monospace; }
pre {
    background: linear-gradient(145deg, #1e293b 0%, #0f172a 100%);
    padding: 1.2em;
    border-radius: 8px;
    overflow-x: auto;
    border: 1px solid #334155;
    box-shadow: 0 4px 12px rgba(0,0,0,0.5);
    position: relative;
    margin: 1em 0;
}
pre code {
    background: none;
    padding: 0;
    border: none;
    display: block;
    line-height: 1.5;
    font-family: SFMono-Regular, Consolas, Liberation Mono, Menlo, monospace;
    font-size: 14px;
    color: #e2e8f0;
}
pre::before {
    content: attr(data-lang);
    position: absolute;
    top: 0.3em;
    right: 0.5em;
    font-size: 0.75em;
    color: #94a3b8;
    background: rgba(255,255,255,0.1);
    padding: 0.2em 0.5em;
    border-radius: 4px;
    font-weight: 600;
    z-index: 1;
}
/* 覆盖 PrismJS 默认样式 */
pre[class*="language-"] {
    background: linear-gradient(145deg, #1e293b 0%, #0f172a 100%) !important;
    box-shadow: 0 4px 12px rgba(0,0,0,0.5) !important;
    border: 1px solid #334155 !important;
}
blockquote { border-left: 4px solid #30363d; margin: 0; padding: 0.5em 1em; color: #8b949e; background: #161b22; }
table { border-collapse: collapse; width: 100%; margin: 1.5em 0; display: block; overflow-x: auto; }
th, td { border: 1px solid #30363d; padding: 8px 12px; text-align: left; }
th { background: #161b22; font-weight: 600; white-space: nowrap; }
tr:nth-child(even) { background-color: #161b22; }
tr:hover { background-color: #21262d; }
img { max-width: 100%; }
a { color: #58a6ff; text-decoration: none; }
a:hover { text-decoration: underline; }
hr { border: none; border-top: 2px solid #21262d; margin: 2em 0; }
ul, ol { padding-left: 2em; }
"""
)

THEMES = {
    'light': LIGHT_THEME,
    'dark': DARK_THEME,
}


# =============================================================================
# Markdown Inline Parser
# =============================================================================

class InlineParser:
    """Processes inline markdown elements like bold, italic, links, code."""
    
    # Regex patterns for inline elements (compiled for performance)
    PATTERNS = [
        (r'!\[([^\]]*)\]\(([^)]+)\)', r'<img src="\2" alt="\1">'),  # Images
        (r'\[([^\]]+)\]\(([^)]+)\)', r'<a href="\2">\1</a>'),  # Links
        (r'\*\*(.+?)\*\*', r'<strong>\1</strong>'),  # Bold
        (r'\*(.+?)\*', r'<em>\1</em>'),  # Italic
        (r'`([^`]+)`', r'<code>\1</code>'),  # Inline code
        (r'~~(.+?)~~', r'<del>\1</del>'),  # Strikethrough
        (r'\*\*\*(.+?)\*\*\*', r'<strong><em>\1</em></strong>'),  # Bold+Italic
    ]
    
    def __init__(self):
        self._compiled_patterns = [(re.compile(p), r) for p, r in self.PATTERNS]
    
    def parse(self, text: str) -> str:
        """Apply all inline markdown transformations to the text."""
        if not text:
            return ""
        
        for pattern, replacement in self._compiled_patterns:
            text = pattern.sub(replacement, text)
        
        return text


# =============================================================================
# Table Parser
# =============================================================================

@dataclass
class TableState:
    """Holds state while parsing markdown tables."""
    in_table: bool = False
    header_pending: list[str] = field(default_factory=list)
    
    def reset(self):
        """Reset table state."""
        self.in_table = False
        self.header_pending = []


class TableParser:
    """Handles markdown table parsing and conversion to HTML."""
    
    SEPARATOR_PATTERN = re.compile(r'^:?\s*-+\s*?:?$')
    
    def __init__(self, inline_parser: InlineParser):
        self.inline_parser = inline_parser
        self.state = TableState()
    
    def is_separator(self, line: str) -> bool:
        """Check if a line is a table separator (e.g., | --- | :---: |)."""
        stripped = line.strip()
        if '|' not in stripped:
            return False
        
        # Remove pipes and split
        content = stripped
        if content.startswith('|'):
            content = content[1:]
        if content.endswith('|'):
            content = content[:-1]
        
        parts = [p.strip() for p in content.split('|')]
        if not parts:
            return False
        
        return all(self.SEPARATOR_PATTERN.match(part) for part in parts)
    
    def parse_row(self, line: str) -> list[str]:
        """Parse a markdown table row into a list of cell contents."""
        content = line.strip()
        
        # Remove leading/trailing pipes
        if content.startswith('|'):
            content = content[1:]
        if content.endswith('|'):
            content = content[:-1]
        
        # Split by pipe and apply inline formatting
        cells = [c.strip() for c in content.split('|')]
        return [self.inline_parser.parse(cell) for cell in cells]
    
    def start_table(self, headers: list[str]) -> str:
        """Generate HTML table start with header row."""
        header_html = ''.join(f'<th>{cell}</th>' for cell in headers)
        return f'<table><thead><tr>{header_html}</tr></thead><tbody>'
    
    def end_table(self) -> str:
        """Close the table element."""
        return '</tbody></table>'
    
    def row_to_html(self, cells: list[str], cell_tag: str = 'td') -> str:
        """Convert a row of cells to HTML table row."""
        row_html = ''.join(f'<{cell_tag}>{cell}</{cell_tag}>' for cell in cells)
        return f'<tr>{row_html}</tr>'
# =============================================================================
# Block State Management
# =============================================================================

@dataclass
class BlockState:
    """Manages state for block-level elements during conversion."""
    in_code_block: bool = False
    in_list: Optional[str] = None  # 'ul' or 'ol'
    in_paragraph: bool = False
    code_lang: str = ''
    
    def reset(self):
        """Reset all block states."""
        self.in_code_block = False
        self.in_list = None
        self.in_paragraph = False
        self.code_lang = ''


# =============================================================================
# Main Converter
# =============================================================================

class MarkdownConverter:
    """Converts Markdown text to HTML with support for tables, code blocks, lists, etc."""
    
    # Regex patterns for block elements
    HEADING_PATTERN = re.compile(r'^(#{1,6})\s+(.+)$')
    HR_PATTERN = re.compile(r'^[-*_]{3,}\s*$')
    BLOCKQUOTE_PATTERN = re.compile(r'^>')
    UL_PATTERN = re.compile(r'^[-*+]\s+(.+)$')
    OL_PATTERN = re.compile(r'^\d+\.\s+(.+)$')
    CODE_BLOCK_MARKER = re.compile(r'^```')
    TABLE_PIPE_INDICATOR = '|'
    
    # Default language replacement rules
    DEFAULT_LANGUAGE_REPLACEMENTS = {
        'typescript': 'javascript',
        'ts': 'javascript',
        'tsx': 'javascript',
        'md': 'markdown',
        'yml': 'yaml',
        'golang': 'go',
        'shell': 'bash',
        'sh': 'bash',
        'zsh': 'bash',
        'c#': 'csharp',
        'cs': 'csharp',
        'vue': 'html',
        'react': 'jsx',
    }
    
    def __init__(self, language_replacements: Optional[dict[str, str]] = None):
        self.inline_parser = InlineParser()
        self.table_parser = TableParser(self.inline_parser)
        self.block_state = BlockState()
        self.html_lines: list[str] = []
        # Use provided replacements or default ones
        self.language_replacements = language_replacements if language_replacements is not None else self.DEFAULT_LANGUAGE_REPLACEMENTS.copy()
    
    def _close_list(self):
        """Close the current list if open."""
        if self.block_state.in_list:
            self.html_lines.append(f'</{self.block_state.in_list}>')
            self.block_state.in_list = None
    
    def _close_paragraph(self):
        """Close the current paragraph if open."""
        if self.block_state.in_paragraph:
            self.html_lines.append('</p>')
            self.block_state.in_paragraph = False
    
    def _close_table(self):
        """Close the current table if open."""
        if self.block_state.in_code_block:
            return
        if self.table_parser.state.in_table:
            self.html_lines.append(self.table_parser.end_table())
            self.table_parser.state.reset()
    
    def _close_all_blocks(self):
        """Close all open block elements."""
        self._close_paragraph()
        self._close_list()
        self._close_table()
    
    def _replace_language(self, lang: str) -> str:
        """Replace language identifier based on replacement rules.
        
        Args:
            lang: The original language identifier.
            
        Returns:
            The replaced language identifier, or the original if no replacement rule applies.
        """
        if not lang:
            return ''
        
        # Case-insensitive lookup
        lang_lower = lang.lower()
        return self.language_replacements.get(lang_lower, lang)
    
    def _handle_code_block_start(self, line: str):
        """Handle the start/end of a code block."""
        lang = line.strip()[3:].strip()
        # Apply language replacement
        lang = self._replace_language(lang)
        self.block_state.code_lang = lang
        
        if self.block_state.in_code_block:
            # End code block
            self.html_lines.append('</code></pre>')
            self.block_state.in_code_block = False
        else:
            # Start code block - add language class for PrismJS
            lang_class = f' class="language-{html_mod.escape(lang)}"' if lang else ''
            lang_attr = f' data-lang="{html_mod.escape(lang)}"' if lang else ''
            self.html_lines.append(f'<pre{lang_attr}><code{lang_class}>')
            self.block_state.in_code_block = True
    
    def _handle_table_line(self, line: str):
        """Process a line that contains a pipe character (potential table)."""
        state = self.table_parser.state
        
        # Check if this looks like a table header (not starting with # or other block elements)
        # If line starts with markdown heading (#), it's not a table
        if line.startswith('#'):
            return False
        
        # Case A: Already inside a table -> Data Row
        if state.in_table:
            cells = self.table_parser.parse_row(line)
            self.html_lines.append(self.table_parser.row_to_html(cells))
            return True
        
        # Case B: Have pending header, current line is separator -> Start Table
        if state.header_pending and self.table_parser.is_separator(line):
            self._close_paragraph()
            self._close_list()
            state.in_table = True
            self.html_lines.append(self.table_parser.start_table(state.header_pending))
            state.header_pending = []
            return True
        
        # Case C: No pending header, looks like a header row -> Tentative Start
        if not state.header_pending and not self.table_parser.is_separator(line):
            self._close_paragraph()
            self._close_list()
            state.header_pending = self.table_parser.parse_row(line)
            return True
        
        return False
    
    def _handle_false_table_start(self):
        """Handle case where a line looked like a table header but wasn't."""
        state = self.table_parser.state
        if state.header_pending:
            self._close_paragraph()
            self._close_list()
            # Reconstruct the pending line as a paragraph
            reconstructed = ' | '.join(state.header_pending)
            self.html_lines.append(f'<p>{reconstructed}</p>')
            state.header_pending = []
    
    def _handle_heading(self, line: str) -> bool:
        """Process a heading line. Returns True if handled."""
        match = self.HEADING_PATTERN.match(line)
        if match:
            level = len(match.group(1))
            content = self.inline_parser.parse(match.group(2))
            self.html_lines.append(f'<h{level}>{content}</h{level}>')
            return True
        return False
    
    def _handle_horizontal_rule(self, line: str) -> bool:
        """Process a horizontal rule. Returns True if handled."""
        if self.HR_PATTERN.match(line):
            self.html_lines.append('<hr>')
            return True
        return False
    
    def _handle_blockquote(self, line: str):
        """Process a blockquote."""
        if line.startswith('>'):
            text = line.lstrip('>').strip()
            self.html_lines.append(f'<blockquote><p>{self.inline_parser.parse(text)}</p></blockquote>')
    
    def _handle_unordered_list(self, line: str):
        """Process an unordered list item."""
        match = self.UL_PATTERN.match(line)
        if match:
            if self.block_state.in_list != 'ul':
                self._close_list()
                self.html_lines.append('<ul>')
                self.block_state.in_list = 'ul'
            self.html_lines.append(f'<li>{self.inline_parser.parse(match.group(1))}</li>')
    
    def _handle_ordered_list(self, line: str):
        """Process an ordered list item."""
        match = self.OL_PATTERN.match(line)
        if match:
            if self.block_state.in_list != 'ol':
                self._close_list()
                self.html_lines.append('<ol>')
                self.block_state.in_list = 'ol'
            self.html_lines.append(f'<li>{self.inline_parser.parse(match.group(1))}</li>')
    
    def _handle_paragraph(self, line: str):
        """Process a paragraph line."""
        if not self.block_state.in_paragraph:
            self._close_list()
            self._close_table()
            self.html_lines.append('<p>')
            self.block_state.in_paragraph = True
        
        self.html_lines.append(self.inline_parser.parse(line))
    
    def convert(self, md_text: str) -> str:
        """Convert Markdown text to HTML.
        
        Args:
            md_text: The Markdown text to convert.
            
        Returns:
            The converted HTML string.
        """
        lines = md_text.split('\n')
        self.html_lines = []
        self.block_state.reset()
        self.table_parser.state.reset()
        
        for line in lines:
            # 1. Code blocks (highest priority)
            if line.strip().startswith('```'):
                self._close_all_blocks()
                self._handle_code_block_start(line)
                continue
            
            if self.block_state.in_code_block:
                self.html_lines.append(html_mod.escape(line))
                continue
            
            stripped = line.strip()
            
            # 2. Empty line (resets all block states)
            if not stripped:
                self._close_all_blocks()
                continue
            
            # 3. Table Logic (but not if it's a heading or other block element)
            if self.TABLE_PIPE_INDICATOR in stripped and not stripped.startswith('#'):
                if self._handle_table_line(stripped):
                    continue
            
            # 4. Handle "False Start" for tables
            self._handle_false_table_start()
            
            # 5. Headings
            if self._handle_heading(stripped):
                continue
            
            # 6. Horizontal Rule
            if self._handle_horizontal_rule(stripped):
                continue
            
            # 7. Blockquote
            if self.BLOCKQUOTE_PATTERN.match(stripped):
                self._close_all_blocks()
                self._handle_blockquote(stripped)
                continue
            
            # 8. Unordered List
            if self.UL_PATTERN.match(stripped):
                self._close_paragraph()
                self._close_table()
                self._handle_unordered_list(stripped)
                continue
            
            # 9. Ordered List
            if self.OL_PATTERN.match(stripped):
                self._close_paragraph()
                self._close_table()
                self._handle_ordered_list(stripped)
                continue
            
            # 10. Paragraph
            self._handle_paragraph(stripped)
        
        # Final cleanup
        self._close_all_blocks()
        if self.block_state.in_code_block:
            self.html_lines.append('</code></pre>')
        
        return '\n'.join(self.html_lines)


def md_to_html(md_text: str, language_replacements: Optional[dict[str, str]] = None) -> str:
    """Convert Markdown to HTML.
    
    This is a convenience function that creates a MarkdownConverter
    instance and converts the provided text.
    
    Args:
        md_text: The Markdown text to convert.
        language_replacements: Optional dictionary mapping language identifiers
                              to their replacements (e.g., {'typescript': 'javascript'}).
                              
    Returns:
        The converted HTML string (body content only, no HTML wrapper).
    """
    converter = MarkdownConverter(language_replacements=language_replacements)
    return converter.convert(md_text)


# =============================================================================
# HTML Document Generator
# =============================================================================

def generate_html_document(body_content: str, title: str, theme: Theme) -> str:
    """Generate a complete HTML document with the given body content.
    
    Args:
        body_content: The HTML content for the body.
        title: The document title.
        theme: The theme to use for styling.
        
    Returns:
        A complete HTML document string.
    """
    escaped_title = html_mod.escape(title)
    
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{escaped_title}</title>
<style>{theme.css}</style>
<!-- 引入 PrismJS 进行语法高亮 (使用国内 CDN) -->
<link rel="stylesheet" href="https://cdn.staticfile.org/prism/1.29.0/themes/prism-tomorrow.min.css">
<script src="https://cdn.staticfile.org/prism/1.29.0/prism.min.js"></script>
<script src="https://cdn.staticfile.org/prism/1.29.0/components/prism-python.min.js"></script>
<script src="https://cdn.staticfile.org/prism/1.29.0/components/prism-javascript.min.js"></script>
<script src="https://cdn.staticfile.org/prism/1.29.0/components/prism-css.min.js"></script>
<script src="https://cdn.staticfile.org/prism/1.29.0/components/prism-bash.min.js"></script>
<script src="https://cdn.staticfile.org/prism/1.29.0/components/prism-json.min.js"></script>
<script src="https://cdn.staticfile.org/prism/1.29.0/components/prism-java.min.js"></script>
<script src="https://cdn.staticfile.org/prism/1.29.0/components/prism-sql.min.js"></script>
</head>
<body>
{body_content}
</body>
</html>"""

# =============================================================================
# CLI Interface
# =============================================================================

def read_markdown_file(input_path: str) -> str:
    """Read markdown content from a file or stdin.
    
    Args:
        input_path: Path to the markdown file, or '-' for stdin.
        
    Returns:
        The markdown content as a string.
        
    Raises:
        FileNotFoundError: If the input file doesn't exist.
    """
    if input_path == '-':
        return sys.stdin.read()
    
    with open(input_path, 'r', encoding='utf-8') as f:
        return f.read()


def write_html_output(content: str, output_path: Optional[str]):
    """Write HTML content to a file or stdout.
    
    Args:
        content: The HTML content to write.
        output_path: Path to the output file, or None for stdout.
    """
    if output_path:
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Successfully written to {output_path}", file=sys.stderr)
    else:
        print(content)


def create_argument_parser() -> argparse.ArgumentParser:
    """Create and configure the argument parser."""
    parser = argparse.ArgumentParser(
        description='Convert Markdown to styled HTML',
        epilog='Examples:\n'
               '  python markdown2html.py README.md -o readme.html\n'
               '  python markdown2html.py notes.md --theme dark -o notes.html\n'
               '  cat CHANGELOG.md | python markdown2html.py - -o changelog.html',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    parser.add_argument(
        'input',
        help='Input markdown file (use - for stdin)'
    )
    parser.add_argument(
        '-o', '--output',
        dest='output',
        help='Output HTML file (default: stdout)'
    )
    parser.add_argument(
        '--theme',
        choices=['light', 'dark'],
        default='light',
        help='Color theme (default: light)'
    )
    parser.add_argument(
        '--title',
        default='Document',
        help='HTML Page Title (default: Document)'
    )
    
    return parser


def main():
    """Main entry point for the CLI."""
    parser = create_argument_parser()
    args = parser.parse_args()
    
    try:
        # Read input
        md_text = read_markdown_file(args.input)
    except FileNotFoundError as e:
        print(f"Error: File '{args.input}' not found.", file=sys.stderr)
        sys.exit(1)
    except IOError as e:
        print(f"Error reading input: {e}", file=sys.stderr)
        sys.exit(1)
    
    # Get theme
    theme = THEMES.get(args.theme, LIGHT_THEME)
    
    # Convert markdown to HTML
    body_html = md_to_html(md_text)
    
    # Generate complete HTML document
    html_document = generate_html_document(body_html, args.title, theme)
    
    # Write output
    write_html_output(html_document, args.output)


if __name__ == '__main__':
    main()