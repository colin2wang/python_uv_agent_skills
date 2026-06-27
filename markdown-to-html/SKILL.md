---
name: markdown-to-html
description: Convert Markdown files to beautifully styled, self-contained HTML with embedded CSS. Perfect for newsletters, documentation, reports, and email templates.
triggers:
  - convert markdown to html
  - markdown to html
  - render markdown
  - style markdown
dependency:
  python: []
metadata: { "copaw": { "emoji": "✨" } }
---

# Markdown to HTML Converter

A zero-dependency Python tool that converts Markdown files into beautiful, self-contained HTML documents with embedded CSS styling. No external libraries needed — uses only Python's standard library.

## Features

- **Full Markdown support**: Headings, bold, italic, strikethrough, links, images, code blocks with syntax hints, blockquotes, ordered and unordered lists, horizontal rules, and **tables**
- **Two built-in themes**: Light (GitHub-inspired) and Dark mode
- **Self-contained output**: All CSS is embedded inline — works anywhere with no external dependencies
- **Responsive design**: Looks great on desktop and mobile
- **Stdin/Stdout support**: Pipe content in shell pipelines

## Usage

Convert a file with the default light theme:
```bash
uv run python markdown-to-html/markdown2html.py README.md -o readme.html
```

Use the dark theme for a presentation:
```bash
uv run python markdown-to-html/markdown2html.py notes.md -o notes.html --theme dark --title "Meeting Notes"
```

Pipe from another command using stdin:
```bash
cat CHANGELOG.md | uv run python markdown-to-html/markdown2html.py - -o changelog.html
```

Output to stdout (for piping):
```bash
uv run python markdown-to-html/markdown2html.py issue-42.md --title "Lobster Diary #42" > issue.html
```

## Supported Markdown Elements

| Element | Syntax | Supported |
|---------|--------|-----------|
| Headings | `# H1` through `###### H6` | ✅ |
| Bold | `**text**` | ✅ |
| Italic | `*text*` | ✅ |
| Strikethrough | `~~text~~` | ✅ |
| Links | `[text](url)` | ✅ |
| Images | `![alt](url)` | ✅ |
| Code blocks | Triple backtick with language | ✅ |
| Inline code | Single backtick | ✅ |
| Blockquotes | `> text` | ✅ |
| Unordered lists | `- item` or `* item` | ✅ |
| Ordered lists | `1. item` | ✅ |
| Horizontal rules | `---` | ✅ |
| Tables | `\| col \|` with separator row | ✅ |

## CLI Options

- `input` — Markdown file path, or `-` for stdin
- `-o, --output` — Output HTML file (defaults to stdout)
- `--theme` — `light` (default) or `dark`
- `--title` — HTML document title (default: "Document")
