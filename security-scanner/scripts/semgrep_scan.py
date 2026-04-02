#!/usr/bin/env python3
"""
Semgrep Code Security Scanner Script

Features:
1. Call Semgrep to perform static code analysis
2. Parse scan results and extract key information
3. Generate structured vulnerability reports

Usage:
    python semgrep_scan.py <target_path> [--rules <rules>] [--exclude <exclude_paths>]

Arguments:
    target_path: Scan target path (file or directory)
    --rules: Semgrep rules (default: auto, automatic detection)
    --exclude: Paths to exclude (comma-separated, e.g.: tests/,venv/,node_modules/)

Output:
    JSON formatted scan results, including summary and detailed vulnerability list
"""

import argparse
import io
import json
import locale
import os
import subprocess
import sys
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, asdict
from enum import Enum


class SeverityLevel(Enum):
    """Severity level enumeration"""
    CRITICAL = "ERROR"
    HIGH = "WARNING"
    MEDIUM = "INFO"
    LOW = "UNKNOWN"


@dataclass
class ScanConfig:
    """Scan configuration data class"""
    target_path: str
    rules: str = "auto"
    exclude: Optional[List[str]] = None
    timeout: int = 600


@dataclass
class ScanStats:
    """Scan statistics data class"""
    target_path: str
    files_scanned: int
    scan_completed: bool
    return_code: int


@dataclass
class Finding:
    """Vulnerability finding data class"""
    rule_id: str
    severity: str
    message: str
    file: str
    line: int
    column: int
    end_line: int
    end_column: int
    code_snippet: str
    fix: Optional[str]
    cwe: List[str]
    references: List[str]


@dataclass
class ScanResult:
    """Scan result data class"""
    error: bool
    message: Optional[str] = None
    details: Optional[str] = None
    summary: Optional[Dict[str, Any]] = None
    findings: List[Finding] = None
    scan_stats: Optional[ScanStats] = None
    
    def __post_init__(self):
        if self.findings is None:
            self.findings = []
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        result = {
            'error': self.error,
        }
        if self.message:
            result['message'] = self.message
        if self.details:
            result['details'] = self.details
        if self.summary:
            result['summary'] = self.summary
        if self.findings:
            result['findings'] = [asdict(f) for f in self.findings]
        if self.scan_stats:
            result['scan_stats'] = asdict(self.scan_stats)
        return result


def check_semgrep_installed() -> bool:
    """Check if semgrep is installed"""
    try:
        result = subprocess.run(
            ["semgrep", "--version"],
            capture_output=True,
            text=True,
            timeout=10
        )
        return result.returncode == 0
    except (FileNotFoundError, subprocess.TimeoutExpired):
        return False


class SemgrepScanner:
    """Semgrep scanner class encapsulating all scan-related operations"""
    
    SUPPORTED_EXTENSIONS = {
        '.py', '.js', '.ts', '.jsx', '.tsx', '.java', '.go', 
        '.c', '.cpp', '.h', '.hpp', '.rb', '.php', '.cs', 
        '.vue', '.svelte'
    }
    
    EXCLUDED_DIRS = {
        '.git', 'node_modules', '__pycache__', '.venv', 'venv'
    }
    
    def __init__(self, config: ScanConfig):
        """
        Initialize scanner
        
        Args:
            config: Scan configuration
        """
        self.config = config
        self.target_path = Path(config.target_path)
    
    def validate_path(self) -> Tuple[bool, Optional[str]]:
        """
        Validate target path
        
        Returns:
            Tuple of (is_valid, error_message)
        """
        if sys.platform == 'win32':
            if not self.target_path.is_absolute():
                return False, f"On Windows, absolute paths must be used. Current path: {self.target_path}"
        
        if not self.target_path.exists():
            return False, f"Target path does not exist: {self.target_path}"
        
        return True, None
    
    def count_code_files(self) -> int:
        """
        Count code files to be scanned
        
        Returns:
            Number of code files
        """
        if not self.target_path.exists():
            return 0
        
        total_files = 0
        
        if self.target_path.is_file():
            if self.target_path.suffix in self.SUPPORTED_EXTENSIONS:
                return 1
            return 0
        
        for root, dirs, files in os.walk(self.target_path):
            # Skip excluded directories
            dirs[:] = [d for d in dirs if d not in self.EXCLUDED_DIRS]
            
            # Count code files
            code_files = [
                f for f in files 
                if Path(f).suffix in self.SUPPORTED_EXTENSIONS
            ]
            total_files += len(code_files)
        
        return total_files
    
    def build_command(self) -> List[str]:
        """
        Build Semgrep command
        
        Returns:
            Command list
        """
        cmd = [
            "semgrep",
            "--json",
            "--config", self.config.rules,
            str(self.target_path)
        ]
        
        if self.config.exclude:
            for path in self.config.exclude:
                cmd.extend(["--exclude", path])
        
        return cmd
    
    def _setup_environment(self) -> Dict[str, str]:
        """Setup environment variables for subprocess"""
        env = os.environ.copy()
        env['PYTHONIOENCODING'] = 'utf-8'
        env['PYTHONUTF8'] = '1'
        return env
    
    def _handle_error(self, message: str, **kwargs) -> ScanResult:
        """Create error result"""
        return ScanResult(
            error=True,
            message=message,
            details=kwargs.get('details'),
            returncode=kwargs.get('returncode'),
            command=kwargs.get('command')
        )
    
    def scan(self) -> ScanResult:
        """
        Execute Semgrep scan
        
        Returns:
            Scan result
        """
        # Validate path
        is_valid, error_msg = self.validate_path()
        if not is_valid:
            return self._handle_error(error_msg)
        
        # Count files
        total_files = self.count_code_files()
        print(f"Scanning directory: {self.target_path}")
        print(f"Found approximately {total_files} code files to scan")
        
        # Build command
        cmd = self.build_command()
        
        print(f"Running Semgrep scan...")
        print(f"   Command: {' '.join(cmd)}")
        if self.config.exclude:
            print(f"   Excluded paths: {', '.join(self.config.exclude)}")
        
        try:
            # Setup environment
            env = self._setup_environment()
            
            # Execute scan
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=self.config.timeout,
                encoding='utf-8',
                errors='replace',
                env=env
            )
            
            # Handle non-zero return codes
            if result.returncode not in [0, 1]:
                print(f"Error: Semgrep scan failed", file=sys.stderr)
                print(f"Return code: {result.returncode}", file=sys.stderr)
                print(f"Stdout: {result.stdout[:500] if result.stdout else 'None'}", file=sys.stderr)
                print(f"Stderr: {result.stderr[:500] if result.stderr else 'None'}", file=sys.stderr)
                print(f"Full command: {' '.join(cmd)}", file=sys.stderr)
                
                return ScanResult(
                    error=True,
                    message="Semgrep scan failed.",
                    details=result.stderr,
                    returncode=result.returncode,
                    stdout=result.stdout,
                    command=' '.join(cmd)
                )
            
            # Parse results
            if result.stdout:
                scan_result = self._parse_semgrep_output(result.stdout, total_files, result.returncode)
            else:
                scan_result = ScanResult(
                    error=False,
                    summary={"total_findings": 0, "by_severity": {}},
                    findings=[],
                    scan_stats=ScanStats(
                        target_path=str(self.target_path),
                        files_scanned=total_files,
                        scan_completed=True,
                        return_code=result.returncode
                    )
                )
            
            return scan_result
            
        except subprocess.TimeoutExpired:
            print("Error: Semgrep scan timed out")
            return self._handle_error("Scan timed out")
        except Exception as e:
            print(f"Error: {str(e)}")
            return self._handle_error(str(e))
    
    def _parse_semgrep_output(self, json_output: str, files_scanned: int, return_code: int) -> ScanResult:
        """Parse Semgrep JSON output"""
        try:
            data = json.loads(json_output)
            results = data.get("results", [])
            
            # Count by severity
            severity_count = {}
            for result in results:
                severity = result.get("extra", {}).get("severity", "UNKNOWN")
                severity_count[severity] = severity_count.get(severity, 0) + 1
            
            # Extract findings
            findings = []
            for result in results:
                finding = Finding(
                    rule_id=result.get("check_id", "unknown"),
                    severity=result.get("extra", {}).get("severity", "UNKNOWN"),
                    message=result.get("extra", {}).get("message", ""),
                    file=result.get("path", ""),
                    line=result.get("start", {}).get("line", 0),
                    column=result.get("start", {}).get("col", 0),
                    end_line=result.get("end", {}).get("line", 0),
                    end_column=result.get("end", {}).get("col", 0),
                    code_snippet=result.get("extra", {}).get("lines", ""),
                    fix=result.get("extra", {}).get("fix"),
                    cwe=result.get("extra", {}).get("metadata", {}).get("cwe", []),
                    references=result.get("extra", {}).get("metadata", {}).get("references", [])
                )
                findings.append(finding)
            
            return ScanResult(
                error=False,
                summary={
                    "total_findings": len(results),
                    "by_severity": severity_count
                },
                findings=findings,
                scan_stats=ScanStats(
                    target_path=str(self.target_path),
                    files_scanned=files_scanned,
                    scan_completed=True,
                    return_code=return_code
                )
            )
        
        except json.JSONDecodeError as e:
            return ScanResult(
                error=True,
                message=f"Failed to parse Semgrep JSON: {str(e)}"
            )


def severity_to_risk_level(severity: str) -> str:
    """Map Semgrep severity to risk level"""
    severity_map = {
        "ERROR": "Critical",
        "WARNING": "High",
        "INFO": "Medium",
        "UNKNOWN": "Low"
    }
    return severity_map.get(severity, "Low")


class ReportGenerator:
    """Generate readable scan reports"""
    
    SEVERITY_ICONS = {
        "Critical": "[CRITICAL]",
        "High": "[HIGH]",
        "Medium": "[MEDIUM]",
        "Low": "[LOW]"
    }
    
    @staticmethod
    def generate(result: ScanResult) -> str:
        """Generate a readable report"""
        if result.error:
            return f"Scan failed: {result.message}"
        
        report = []
        report.append("=" * 80)
        report.append("Semgrep Scan Results")
        report.append("=" * 80)
        
        # Add scan statistics
        if result.scan_stats:
            stats = result.scan_stats
            report.append(f"\nTarget Path: {stats.target_path}")
            report.append(f"Files Scanned: ~{stats.files_scanned}")
            report.append(f"Scan Completed: {'Yes' if stats.scan_completed else 'No'}")
            report.append(f"Return Code: {stats.return_code}")
        
        # Add summary
        if result.summary:
            report.append(f"\nTotal issues found: {result.summary['total_findings']}")
            report.append("\nBreakdown by severity:")
            
            for severity, count in result.summary.get("by_severity", {}).items():
                risk_level = severity_to_risk_level(severity)
                icon = ReportGenerator.SEVERITY_ICONS.get(risk_level, "[UNKNOWN]")
                report.append(f"  {icon} {risk_level} ({severity}): {count}")
        
        # Add detailed findings
        if result.findings:
            report.append("\nDetailed issue list:\n")
            
            for i, finding in enumerate(result.findings, 1):
                ReportGenerator._append_finding(report, finding, i)
        
        return "\n".join(report)
    
    @staticmethod
    def _append_finding(report: List[str], finding: Finding, index: int):
        """Append a single finding to the report"""
        risk_level = severity_to_risk_level(finding.severity)
        icon = ReportGenerator.SEVERITY_ICONS.get(risk_level, "[UNKNOWN]")
        
        report.append(f"{icon} Issue #{index}")
        report.append(f"   Rule ID: {finding.rule_id}")
        report.append(f"   Risk Level: {risk_level}")
        report.append(f"   File: {finding.file}")
        report.append(f"   Location: Line {finding.line}")
        report.append(f"   Description: {finding.message}")
        
        if finding.code_snippet:
            report.append(f"\n   Problem code:")
            for line in finding.code_snippet.split('\n'):
                report.append(f"   {line}")
        
        if finding.fix:
            report.append(f"\n   Fix suggestion:")
            report.append(f"   {finding.fix}")
        
        if finding.cwe:
            report.append(f"\n   CWE Number: {', '.join(map(str, finding.cwe))}")
        
        report.append("\n" + "-" * 80 + "\n")



def setup_encoding():
    """Setup UTF-8 encoding for cross-platform compatibility"""
    # Set environment variables
    os.environ['PYTHONIOENCODING'] = 'utf-8'
    os.environ['PYTHONUTF8'] = '1'
    
    # Try to set locale
    try:
        locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')
    except locale.Error:
        pass
    
    # Force stdin/stdout/stderr encoding on Windows
    if sys.platform == 'win32':
        sys.stdin = io.TextIOWrapper(sys.stdin.buffer, encoding='utf-8', errors='replace')
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
        sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')


def output_json(result: ScanResult):
    """Output result as JSON with proper encoding handling"""
    json_output = json.dumps(result.to_dict(), indent=2, ensure_ascii=False)
    
    try:
        if sys.platform == 'win32':
            # Use buffer write to avoid encoding issues on Windows
            sys.stdout.buffer.write((json_output + '\n').encode('utf-8'))
            sys.stdout.flush()
        else:
            print(json_output)
    except (ValueError, AttributeError, OSError) as e:
        # Fallback for stdout issues
        try:
            old_stdout = sys.stdout
            sys.stdout = io.StringIO()
            sys.stdout = old_stdout
            sys.stdout.write(json_output + '\n')
        except Exception:
            sys.stdout = old_stdout
            sys.stderr.write(json_output + '\n')


def main():
    """Main entry point"""
    # Setup encoding
    setup_encoding()
    
    # Parse arguments
    parser = argparse.ArgumentParser(
        description="Use Semgrep for code security scanning"
    )
    parser.add_argument(
        "target_path",
        help="Scan target path (file or directory)"
    )
    parser.add_argument(
        "--rules",
        default="auto",
        help="Semgrep ruleset (default: auto, automatic detection)"
    )
    parser.add_argument(
        "--exclude",
        help="Paths to exclude (comma-separated, e.g.: tests/,venv/,node_modules/)"
    )
    parser.add_argument(
        "--report",
        action="store_true",
        help="Generate readable report"
    )
    parser.add_argument(
        "--timeout",
        type=int,
        default=600,
        help="Scan timeout in seconds (default: 600)"
    )

    args = parser.parse_args()

    # Check if semgrep is installed
    if not check_semgrep_installed():
        print("Error: Semgrep not detected")
        print("\nPlease install Semgrep:")
        print("  pip install semgrep")
        print("  or")
        print("  macOS: brew install semgrep")
        print("  Linux: python3 -m pip install semgrep")
        sys.exit(1)

    # Parse excluded paths
    exclude_paths = None
    if args.exclude:
        exclude_paths = [path.strip() for path in args.exclude.split(",")]

    # Create scan configuration
    config = ScanConfig(
        target_path=args.target_path,
        rules=args.rules,
        exclude=exclude_paths,
        timeout=args.timeout
    )

    # Create scanner and execute scan
    scanner = SemgrepScanner(config)
    result = scanner.scan()

    # Output results
    if args.report:
        print(ReportGenerator.generate(result))
    else:
        output_json(result)


if __name__ == "__main__":
    main()
