"""Unit tests for libcsv."""

import pathlib
from dataclasses import dataclass

import pytest
import yaml

from src import libcsv

ROOT = pathlib.Path(__file__).parent.parent.resolve()

with pathlib.Path(ROOT / 'tests' / 'test_cases.yaml').open(
    encoding='utf-8',
) as test_cases_file:
    f = yaml.safe_load(test_cases_file)
    raw_test_cases: list[dict[str, str]] = f['test_cases']
    standard_test_case_data: str = f['standard_test_case']['csv_data']


@dataclass
class DataTestCase:
    """Data class representing test cases imported from the YAML file."""

    csv_data: str
    selected_columns: str
    row_filter_definitions: str
    expected_output: str
    name: str


test_cases = [
    *[
        DataTestCase(
            csv_data=case.get('csv_data') or standard_test_case_data,
            selected_columns=case.get('selected_columns') or '',
            row_filter_definitions=case.get('row_filter_definitions') or '',
            expected_output=case['expected_output'],
            name=case['name'],
        )
        for case in raw_test_cases
    ],
]

params = [
    pytest.param(
        case.csv_data,
        case.selected_columns,
        case.row_filter_definitions,
        case.expected_output,
        id=case.name,
    )
    for case in test_cases
]


@pytest.mark.parametrize(
    (
        'csv_data',
        'selected_columns',
        'row_filter_definitions',
        'expected_output',
    ),
    params,
)
def test_process_csv_data(
    csv_data: str,
    selected_columns: str,
    row_filter_definitions: str,
    expected_output: str,
) -> None:
    """Test the process_csv_data function.

    Args:
    ----
        csv_data (str): CSV data to be processed.
        selected_columns (str): Columns to be selected from the CSV data.
        row_filter_definitions (str): Filters to be applied to the CSV data.
        expected_output (str): Expected output of the function.

    """
    try:
        captured_output = libcsv.process_csv_data(
            csv_data,
            selected_columns,
            row_filter_definitions,
        )

    except ValueError as err:
        captured_output = str(err) + '\n'

    assert captured_output == expected_output, 'Output mismatch'


@pytest.mark.parametrize(
    (
        'csv_data',
        'selected_columns',
        'row_filter_definitions',
        'expected_output',
    ),
    params,
)
def test_process_csv_file(
    csv_data: str,
    selected_columns: str,
    row_filter_definitions: str,
    expected_output: str,
    tmp_path: pathlib.Path,
) -> None:
    """Test the process_csv_file function.

    Args:
    ----
        csv_data (str): CSV data to be processed.
        selected_columns (str): Columns to be selected from the CSV data.
        row_filter_definitions (str): Filters to be applied to the CSV data.
        expected_output (str): Expected output of the function.
        tmp_path (pathlib.Path): Temporary path provided by pytest.

    """
    # Create a temporary CSV file with the csv_data content
    csv_file_path = tmp_path / 'test.csv'
    csv_file_path.write_text(csv_data)

    try:
        captured_output = libcsv.process_csv_file(
            str(csv_file_path),
            selected_columns,
            row_filter_definitions,
        )

    except ValueError as err:
        captured_output = str(err) + '\n'

    assert captured_output == expected_output, 'Output mismatch'
