#! /usr/bin/env python3

from json import dump, loads
from sys import stdin, stdout
from typing import TypedDict


class InputDiagnosticPosition(TypedDict):
	begin: int
	end: int


class InputDiagnosticLocation(TypedDict):
	lines: InputDiagnosticPosition


class InputDiagnostic(TypedDict):
	description: str
	location: InputDiagnosticLocation


class OutputDiagnosticPosition(TypedDict):
	line: int
	character: int


class OutputDiagnosticRange(TypedDict):
	start: OutputDiagnosticPosition
	end: OutputDiagnosticPosition


class OutputDiagnostic(TypedDict):
	message: str
	severity: str
	range: OutputDiagnosticRange


def process_diagnostic(diagnostic: InputDiagnostic) -> OutputDiagnostic:
	range_start = diagnostic["location"]["lines"]["begin"] - 1
	range_length = diagnostic["location"]["lines"]["end"]
	offset = 1 if range_length > 0 else 0

	return {
		"severity": "Error",
		"message": diagnostic["description"],
		"range": {
			"start": {"line": range_start, "character": 0},
			"end": {"line": range_start + range_length + offset, "character": offset},
		},
	}

if __name__ == "__main__":
	for line in stdin.readlines():
		input_diagnostics = loads(line)
		output_diagnostics = list(map(process_diagnostic, input_diagnostics))
		dump(output_diagnostics, stdout)
