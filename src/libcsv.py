import io
import operator
import pathlib
import sys
from collections.abc import Sequence
from csv import QUOTE_NONE, DictReader, DictWriter

# Python 3.7+ allows usage of sys.stdout.reconfigure()
if isinstance(sys.stdout, io.TextIOWrapper) and sys.version_info >= (3, 7):
    # Standardize newline configuration to avoid conflicts with other OSs.
    sys.stdout.reconfigure(newline='\n')

COMPARISON_OPERATORS = {
    '!=': operator.ne,  # Not equal to
    '>=': operator.ge,  # Greater than or equal to
    '<=': operator.le,  # Less than or equal to
    '=': operator.eq,  # Equal to
    '>': operator.gt,  # Greater than
    '<': operator.lt,  # Less than
}


def process_csv_file(
    csv_file_path: str,
    selected_columns: str,
    row_filter_definitions: str,
) -> None:
    csv_data = read_csv_file(csv_file_path)
    process_csv_data(csv_data, selected_columns, row_filter_definitions)


def read_csv_file(csv_file_path: str) -> str:
    with pathlib.Path(csv_file_path).open() as csv_file:
        return csv_file.read()


def process_csv_data(
    csv_data: str,
    selected_columns: str,
    row_filter_definitions: str,
) -> None:
    # read input data
    csv_reader = DictReader(csv_data.splitlines())

    # select and validate columns
    csv_headers = get_headers(csv_reader)
    selected_headers = select_headers(csv_headers, selected_columns)
    validate_headers(selected_headers, csv_headers)
    selected_headers = reorder_headers(selected_headers, csv_headers)

    # apply and validate row filter definitions
    filters = parse_filters(row_filter_definitions)
    validate_filters(filters, csv_headers)
    filtered_rows = filter_csv_data(csv_reader, selected_headers, filters)

    # write output data
    write_csv_data(filtered_rows, selected_headers)


def get_headers(csv_reader: DictReader[str]) -> Sequence[str]:
    csv_headers = csv_reader.fieldnames

    if not csv_headers:
        no_headers_msg = 'CSV data has no headers'
        raise ValueError(no_headers_msg)

    return csv_headers


def select_headers(
    csv_headers: Sequence[str],
    selected_columns: str,
) -> list[str]:
    return (
        selected_columns.split(',') if selected_columns else list(csv_headers)
    )


def validate_headers(
    selected_headers: list[str],
    csv_headers: Sequence[str],
) -> None:
    for header in selected_headers:
        if header not in csv_headers:
            inexistent_selected_headers_msg = (
                f"Header '{header}' not found in CSV file/string"
            )
            raise ValueError(inexistent_selected_headers_msg)


def reorder_headers(
    selected_headers: list[str],
    csv_headers: Sequence[str],
) -> list[str]:
    return [header for header in csv_headers if header in selected_headers]


def parse_filters(
    row_filter_definitions: str,
) -> dict[str, list[tuple[str, str]]]:
    filters: dict[str, list[tuple[str, str]]] = {}
    for filter_definition in row_filter_definitions.splitlines():
        column, cp_operator, value = parse_filter(filter_definition)
        if column not in filters:
            filters[column] = []
        filters[column].append((cp_operator, value))

    return filters


def parse_filter(filter_definition: str) -> tuple[str, str, str]:
    for cp_operator in COMPARISON_OPERATORS:
        if cp_operator in filter_definition:
            column, value = filter_definition.split(cp_operator)

            return column.strip(), cp_operator, value.strip()

    invalid_filter_msg = f"Invalid filter: '{filter_definition}'"
    raise ValueError(invalid_filter_msg)


def validate_filters(
    filters: dict[str, list[tuple[str, str]]],
    csv_headers: Sequence[str],
) -> None:
    for header in filters:
        if header not in csv_headers:
            inexistent_filtered_headers_msg = (
                f"Header '{header}' not found in CSV file/string"
            )
            raise ValueError(inexistent_filtered_headers_msg)


def filter_csv_data(
    csv_reader: DictReader[str],
    selected_headers: list[str],
    filters: dict[str, list[tuple[str, str]]],
) -> list[dict[str, str]]:
    return [
        {col: row[col] for col in selected_headers}
        for row in csv_reader
        if row_meets_filters(row, filters)
    ]


def row_meets_filters(
    row: dict[str, str],
    filters: dict[str, list[tuple[str, str]]],
) -> bool:
    for column, conditions in filters.items():
        column_satisfies_conditions = False

        for comparator, value in conditions:
            if COMPARISON_OPERATORS[comparator](row[column], value):
                column_satisfies_conditions = True
                break  # Exit the loop as one condition is met for this column

        # If none of the conditions for the current column are met
        if not column_satisfies_conditions:
            return False

    # All columns satisfy at least one of their conditions
    return True


def write_csv_data(
    filtered_rows: list[dict[str, str]],
    selected_headers: list[str],
) -> None:
    csv_writer = DictWriter(
        sys.stdout,
        fieldnames=selected_headers,
        lineterminator='\n',
        quotechar=None,
        quoting=QUOTE_NONE,
    )
    csv_writer.writeheader()
    csv_writer.writerows(filtered_rows)
