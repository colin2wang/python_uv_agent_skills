---
name: security-scanner
description: Automatically scan code for security vulnerabilities and provide fix recommendations. Use when checking code security, generating vulnerability reports, or getting security remediation advice.
triggers:
  - scan code security
  - security scan
  - vulnerability scan
  - security audit
  - find security issues
dependency:
  python:
    - semgrep>=1.157.0
metadata: { "copaw": { "emoji": "🔒" } }
---

# Code Security Scanner

## Overview

- Automatically scan code repositories for security risks and generate detailed vulnerability reports
- Capabilities: vulnerability identification, risk-level assessment, fix recommendation generation
- Trigger: user requests code security review, vulnerability scan report, or security fix suggestions

## Prerequisites

- Python 3.14+
- Semgrep installed (`uv add semgrep` or `pip install semgrep`)
- Code repository accessible in the current directory

## Usage

### Method 1: Semgrep Automated Scan (Recommended)

Use the `scripts/semgrep_scan.py` script:

```bash
# Scan entire project with readable report
uv run python scripts/semgrep_scan.py ./app --report

# Scan specific files, excluding test directories
uv run python scripts/semgrep_scan.py ./src --exclude tests/,venv/

# Custom timeout for large projects
uv run python scripts/semgrep_scan.py ./large-project --timeout 1800 --report
```

**CLI options:**
| Parameter | Description | Default |
|-----------|-------------|---------|
| `target_path` | Scan target (file or directory). Use absolute paths on Windows. | (required) |
| `--rules` | Semgrep ruleset | `auto` |
| `--exclude` | Paths to exclude (comma-separated) | none |
| `--report` | Generate human-readable report | JSON output |
| `--timeout` | Scan timeout in seconds | 600 |

**Supported rulesets:** `auto`, `p/security-audit`, `p/javascript`, `p/cwe`, `p/owasp-top-10`, or a path to a custom YAML rule file.

**Supported languages:** Python, JavaScript, TypeScript, Java, Go, Ruby, PHP, C/C++, and more.

### Method 2: Manual Agent Analysis

The agent walks through code files and checks for:
- SQL injection, XSS, command injection
- Hardcoded secrets (passwords, API keys)
- Path traversal, insecure deserialization
- Insecure random number generation
- Insecure dependencies

## Risk Levels

| Level | Meaning |
|-------|---------|
| **Critical** | Directly exploitable, leads to data breach or system compromise |
| **High** | Exploitable with moderate effort, significant impact |
| **Medium** | Security concern but harder to exploit |
| **Low** | Minor issue, recommended to fix |

## Output

- **JSON format** (default): Structured data with scan statistics and detailed findings
- **Readable report** (`--report`): Human-readable text with risk levels and fix suggestions

## Report Workflow

1. For each vulnerability, the agent generates a temp markdown file: `.tmp-security-{type}-{number}.md`
2. All temp files are merged into a unified security report
3. Temp files are cleaned up after merge
4. Report template: [assets/report-template.md](assets/report-template.md)

## Resources

- Script: [scripts/semgrep_scan.py](scripts/semgrep_scan.py) — Semgrep automation wrapper
- Reference: [references/security-vulnerabilities.md](references/security-vulnerabilities.md) — vulnerability types, checklists, Semgrep rule examples
- Template: [assets/report-template.md](assets/report-template.md) — report template
