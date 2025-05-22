"""
Test Results Parser

This script parses test execution outputs to extract structured test results.

Input:
    - stdout_file: Path to the file containing standard output from test execution
    - stderr_file: Path to the file containing standard error from test execution

Output:
    - JSON file containing parsed test results with structure:
      {
          "tests": [
              {
                  "name": "test_name",
                  "status": "PASSED|FAILED|SKIPPED|ERROR"
              },
              ...
          ]
      }
"""

import dataclasses
import json
import sys
from enum import Enum
from pathlib import Path
from typing import List
import re


class TestStatus(Enum):
    """The test status enum."""

    PASSED = 1
    FAILED = 2
    SKIPPED = 3
    ERROR = 4


@dataclasses.dataclass
class TestResult:
    """The test result dataclass."""

    name: str
    status: TestStatus

### DO NOT MODIFY THE CODE ABOVE ###
### Implement the parsing logic below ###


def parse_test_output(stdout_content: str, stderr_content: str) -> List[TestResult]:
    """
    Parse the test output content and extract test results.

    Args:
        stdout_content: Content of the stdout file
        stderr_content: Content of the stderr file

    Returns:
        List of TestResult objects

    Note to implementer:
        - Implement the parsing logic here
        - Use regular expressions or string parsing to extract test results
        - Create TestResult objects for each test found
    """

    results: List[TestResult] = []

    # Combine stdout and stderr lines for easier processing of common patterns.
    all_lines = stdout_content.splitlines() + stderr_content.splitlines()

    current_file = None

    for line in all_lines:
        line = line.rstrip()
        if not line:
            continue

        # JEST style: "PASS path/to/testfile.test.ts (0.123 s)"
        m = re.match(r"^(PASS|FAIL|SKIP|SKIPPED?)\s+(\S+)", line)
        if m:
            current_file = m.group(2)
            continue

        # JEST individual test cases (passed)
        m = re.match(r"^\s*[\u2713\u2714✓✔]\s+(.*?)(?:\s+\([0-9\.]+\s*(?:ms|s)\))?\s*$", line)
        if m and current_file:
            test_name = m.group(1).strip()
            results.append(TestResult(f"{current_file}::{test_name}", TestStatus.PASSED))
            continue

        # JEST individual test cases (failed)
        m = re.match(r"^\s*[✕x×✖]\s+(.*?)(?:\s+\([0-9\.]+\s*(?:ms|s)\))?\s*$", line)
        if m and current_file:
            test_name = m.group(1).strip()
            results.append(TestResult(f"{current_file}::{test_name}", TestStatus.FAILED))
            continue

        # JEST skipped tests
        m = re.match(r"^\s*(?:○|◌|-|\*)\s+(.*)", line)
        if m and current_file:
            test_name = m.group(1).strip()
            results.append(TestResult(f"{current_file}::{test_name}", TestStatus.SKIPPED))
            continue

        # Pytest style output: path/to/test_file.py::test_name STATUS
        m = re.match(r"^(\S+\.py)::(\S+)\s+(PASSED|FAILED|SKIPPED|ERROR|XPASS|XFAIL)", line)
        if m:
            file_path, test_name, status_word = m.groups()
            if status_word in {"PASSED", "XPASS"}:
                status = TestStatus.PASSED
            elif status_word == "FAILED":
                status = TestStatus.FAILED
            elif status_word in {"SKIPPED", "XFAIL"}:
                status = TestStatus.SKIPPED
            else:
                status = TestStatus.ERROR
            results.append(TestResult(f"{file_path}::{test_name}", status))
            continue

        # Some error lines may include "ERROR" with the same format in stderr
        m = re.match(r"^(\S+\.py)::(\S+)\s+ERROR", line)
        if m:
            file_path, test_name = m.groups()
            results.append(TestResult(f"{file_path}::{test_name}", TestStatus.ERROR))

    return results


### Implement the parsing logic above ###
### DO NOT MODIFY THE CODE BELOW ###


def export_to_json(results: List[TestResult], output_path: Path) -> None:
    """
    Export the test results to a JSON file.

    Args:
        results: List of TestResult objects
        output_path: Path to the output JSON file
    """

    unique_results = {result.name: result for result in results}.values()

    json_results = {
        'tests': [
            {'name': result.name, 'status': result.status.name} for result in unique_results
        ]
    }

    with open(output_path, 'w') as f:
        json.dump(json_results, f, indent=2)


def main(stdout_path: Path, stderr_path: Path, output_path: Path) -> None:
    """
    Main function to orchestrate the parsing process.

    Args:
        stdout_path: Path to the stdout file
        stderr_path: Path to the stderr file
        output_path: Path to the output JSON file
    """
    # Read input files
    with open(stdout_path) as f:
        stdout_content = f.read()
    with open(stderr_path) as f:
        stderr_content = f.read()

    # Parse test results
    results = parse_test_output(stdout_content, stderr_content)

    # Export to JSON
    export_to_json(results, output_path)


if __name__ == '__main__':
    if len(sys.argv) != 4:
        print('Usage: python parsing.py <stdout_file> <stderr_file> <output_json>')
        sys.exit(1)

    main(Path(sys.argv[1]), Path(sys.argv[2]), Path(sys.argv[3]))