---
name: html-to-pdf
description: Convert HTML files to high-quality PDFs with full CSS rendering (including external CSS libraries) and smart page-break control. Use when converting web pages or HTML documents to PDF while preserving styles and layout.
triggers:
  - convert html to pdf
  - html to pdf
  - html to pdf conversion
  - generate pdf from html
  - print html to pdf
dependency:
  python:
    - weasyprint>=68.1
metadata: { "copaw": { "emoji": "📄" } }
---

# HTML to PDF Converter

## Overview

- Convert HTML files to high-quality PDF documents
- Full CSS rendering support, including external CSS libraries (Bootstrap, Tailwind, etc.)
- Smart page-break control via CSS rules
- Preserves original HTML styles, layout, and typography

## Prerequisites

- Python 3.14+
- WeasyPrint requires system-level dependencies on macOS/Linux:
  - macOS: `brew install pango cairo`
  - Ubuntu/Debian: `sudo apt-get install libpango-1.0-0 libpangocairo-1.0-0`
  - Windows: bundled with WeasyPrint, no extra install needed

## Usage

### Basic conversion
```bash
uv run python scripts/html_to_pdf.py input.html
```

### Specify output path
```bash
uv run python scripts/html_to_pdf.py input.html --output output.pdf
```

### Custom page settings
```bash
uv run python scripts/html_to_pdf.py input.html \
  --page-size A4 \
  --margin "2cm 2cm 2cm 2cm" \
  --output custom.pdf
```

### Full CLI options
```
-o, --output       Output PDF path (default: input file with .pdf extension)
-p, --page-size    Page size: A3, A4, A5, Letter, Legal, Tabloid (default: A4)
-m, --margin       Margins, single value or four values e.g. "1cm 2cm 1cm 2cm" (default: 2cm)
-e, --encoding     HTML file encoding (default: utf-8)
```

## CSS Support

Supported CSS reference methods:
- External CSS files: `<link rel="stylesheet" href="styles.css">`
- CDN references: `<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">`
- Embedded styles: `<style>...</style>`
- Inline styles: `style="..."`

For detailed HTML formatting, page-break control, headers/footers, and Chinese font setup, see [references/html_format_guide.md](references/html_format_guide.md).

## Resources

- Script: [scripts/html_to_pdf.py](scripts/html_to_pdf.py) — main conversion script
- Guide: [references/html_format_guide.md](references/html_format_guide.md) — HTML format spec, CSS page-break properties, troubleshooting

## Troubleshooting

| Issue | Solution |
|-------|----------|
| CSS not applied | Verify CSS file paths; check if external CSS is accessible |
| Poor page breaks | Use `page-break-before`, `page-break-after`, `page-break-inside` CSS properties |
| Chinese characters as blocks | Install Chinese fonts or specify a CJK font via CSS `@font-face` |
| Images not showing | Use relative or absolute paths; ensure images are accessible |
| Network-dependent CSS fails | Use local CSS files instead of CDN for offline environments |
