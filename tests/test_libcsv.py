import pathlib
from dataclasses import dataclass

import pytest
import yaml

from src import libcsv

ROOT = pathlib.Path(__file__).parent.parent.resolve()

with pathlib.Path(ROOT / 'tests' / 'test_cases.yaml').open(
    encoding='utf-8',
) as static_test_cases_file:
    static_test_cases = yaml.safe_load(static_test_cases_file)['test_cases']


@dataclass
class DataTestCase:
    csv_data: str
    selected_columns: str
    row_filter_definitions: str
    expected_output: str
    name: str


test_cases = [
    *[
        DataTestCase(
            csv_data=case.get('csv_data'),
            selected_columns=case.get('selected_columns') or '',
            row_filter_definitions=case.get('row_filter_definitions') or '',
            expected_output=case.get('expected_output'),
            name=case.get('name'),
        )
        for case in static_test_cases
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
    expected_output: None,
) -> None:
    """
    Test the process_csv_data function.

    Args:
        csv_data (str): CSV data to be processed.
        selected_columns (str): Columns to be selected from the CSV data.
        row_filter_definitions (str): Filters to be applied to the CSV data.
        expected_output (None): Expected output of the function.
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
