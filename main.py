import csv
import operator
import pathlib
import sys

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
    with pathlib.Path(csv_file_path).open() as csv_file:
        csv_data = csv_file.read()
    process_csv_data(csv_data, selected_columns, row_filter_definitions)


def process_csv_data(
    csv_data: str,
    selected_columns: str,
    row_filter_definitions: str,
) -> None:
    csv_reader = csv.DictReader(csv_data.splitlines())
    headers = csv_reader.fieldnames

    if not headers:
        no_headers_msg = 'CSV data has no headers'
        raise ValueError(no_headers_msg)

    selected_headers = (
        selected_columns.split(',') if selected_columns else list(headers)
    )

    filters = parse_filters(row_filter_definitions)
    filtered_rows = [
        {col: row[col] for col in selected_headers}
        for row in csv_reader
        if row_meets_filters(row, filters)
    ]

    csv_writer = csv.DictWriter(sys.stdout, fieldnames=selected_headers)
    csv_writer.writeheader()
    csv_writer.writerows(filtered_rows)


def parse_filters(row_filter_definitions: str) -> list[tuple[str, str, str]]:
    filters = []
    for filter_definition in row_filter_definitions.splitlines():
        column, cp_operator, value = parse_filter(filter_definition)
        filters.append((column, cp_operator, value))

    return filters


def parse_filter(filter_definition: str) -> tuple[str, str, str]:
    for cp_operator in COMPARISON_OPERATORS:
        if cp_operator in filter_definition:
            column, value = filter_definition.split(cp_operator)
            return column.strip(), cp_operator, value.strip()

    invalid_filter_msg = f'Invalid filter: {filter_definition}'
    raise ValueError(invalid_filter_msg)


def row_meets_filters(
    row: dict[str, str],
    filters: list[tuple[str, str, str]],
) -> bool:
    return all(
        COMPARISON_OPERATORS[comparator](int(row[header]), int(value))
        for header, comparator, value in filters
    )


if __name__ == '__main__':
    csv_data = 'header1,header2,header3,header4\n1,2,3,4\n5,6,7,8\n9,10,11,12'
    selected_columns = 'header1,header3,header4'
    row_filter_definitions = 'header1>1\nheader3<10'
    process_csv_data(csv_data, selected_columns, row_filter_definitions)
