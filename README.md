# Python UV Agent Skills

A collection of three independent, ready-to-use skills for AI coding agents. Each skill is a self-contained tool that can be invoked by an agent to perform a specific task.

## Skills

| Skill | Description | Dependencies |
|-------|-------------|--------------|
| [html-to-pdf](html-to-pdf/) | Convert HTML files to high-quality PDFs with full CSS rendering and page-break control | `weasyprint>=68.1` |
| [markdown-to-html](markdown-to-html/) | Convert Markdown to styled, self-contained HTML with embedded CSS themes | None (stdlib only) |
| [security-scanner](security-scanner/) | Scan code for security vulnerabilities using Semgrep and generate fix recommendations | `semgrep>=1.157.0` |

## Quick Start

This project uses [uv](https://docs.astral.sh/uv/) for Python dependency management.

```bash
# Install all dependencies
uv sync

# Run any skill
uv run python html-to-pdf/scripts/html_to_pdf.py input.html
uv run python markdown-to-html/markdown2html.py README.md -o readme.html
uv run python security-scanner/scripts/semgrep_scan.py ./src --report
```

## Project Structure

```
python_uv_agent_skills/
├── html-to-pdf/
│   ├── scripts/html_to_pdf.py        # Conversion script
│   ├── references/html_format_guide.md  # HTML formatting guide
│   └── SKILL.md                      # Skill definition
├── markdown-to-html/
│   ├── markdown2html.py              # Zero-dependency converter
│   └── SKILL.md                      # Skill definition
├── security-scanner/
│   ├── scripts/semgrep_scan.py       # Semgrep wrapper
│   ├── references/security-vulnerabilities.md  # Vulnerability reference
│   ├── assets/report-template.md     # Report template
│   └── SKILL.md                      # Skill definition
├── pyproject.toml                    # Project config & dependencies
└── README.md
```

## Requirements

- Python 3.14+
- [uv](https://docs.astral.sh/uv/) package manager
- System dependencies for html-to-pdf:
  - macOS: `brew install pango cairo`
  - Ubuntu/Debian: `sudo apt-get install libpango-1.0-0 libpangocairo-1.0-0`
  - Windows: bundled with WeasyPrint

## Skill Details

### html-to-pdf

Converts HTML to PDF using WeasyPrint. Supports external CSS libraries (Bootstrap, Tailwind), CSS page-break control, headers/footers, and CJK fonts.

```bash
uv run python html-to-pdf/scripts/html_to_pdf.py input.html --output output.pdf --page-size A4
```

### markdown-to-html

Zero-dependency Markdown-to-HTML converter with two built-in themes (light/dark). Produces self-contained HTML files with embedded CSS. Supports tables, code blocks, and stdin piping.

```bash
uv run python markdown-to-html/markdown2html.py notes.md -o notes.html --theme dark --title "Notes"
```

### security-scanner

Automated security vulnerability scanner powered by Semgrep. Generates structured JSON reports or human-readable text with risk levels, code locations, and fix suggestions.

```bash
uv run python security-scanner/scripts/semgrep_scan.py ./app --report --exclude tests/,venv/
```

## License

MIT
