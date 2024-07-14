"""Library for processing CSV data.

This module provides functions for reading CSV files, selecting columns,
applying row filters, and writing processed CSV data.
"""

import io
import operator
import pathlib
from collections.abc import Sequence
from csv import QUOTE_NONE, DictReader, DictWriter

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
) -> str:
    """Process a CSV file by reading its data and calling `process_csv_data`.

    Args:
    ----
        csv_file_path (str): Path to the CSV file.
        selected_columns (str): Columns to be selected from the CSV data.
        row_filter_definitions (str): Filters to be applied to the CSV data.

    Returns:
    -------
        str: Processed CSV data as a string.

    """
    csv_data = read_csv_file(csv_file_path)
    return process_csv_data(csv_data, selected_columns, row_filter_definitions)


def read_csv_file(csv_file_path: str) -> str:
    """Read and return the content of a CSV file given its file path.

    Args:
    ----
        csv_file_path (str): Path to the CSV file.

    Returns:
    -------
        str: Content of the CSV file as a string.

    """
    with pathlib.Path(csv_file_path).open() as csv_file:
        return csv_file.read()


def process_csv_data(
    csv_data: str,
    selected_columns: str,
    row_filter_definitions: str,
) -> str:
    """Process the CSV data by applying filters and selecting columns.

    Args:
    ----
        csv_data (str): CSV data as a string.
        selected_columns (str): Columns to be selected from the CSV data.
        row_filter_definitions (str): Filters to be applied to the CSV data.

    Returns:
    -------
        str: Processed CSV data as a string.

    Raises:
    ------
        ValueError:
            - If the csv has no headers;
            - If a selected header is not found in the CSV file;
            - If a filtered header is not found in the CSV file;
            - If a row filter definition is invalid.

    """
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
    return write_csv_data(filtered_rows, selected_headers)


def get_headers(csv_reader: DictReader[str]) -> Sequence[str]:
    """Get the headers from a CSV file reader.

    Args:
    ----
        csv_reader (DictReader[str]): The CSV file reader object.

    Returns:
    -------
        Sequence[str]: The headers of the CSV file.

    Raises:
    ------
        ValueError: If the CSV data has no headers.

    """
    csv_headers = csv_reader.fieldnames

    if not csv_headers:
        no_headers_msg = 'CSV data has no headers'
        raise ValueError(no_headers_msg)

    return csv_headers


def select_headers(
    csv_headers: Sequence[str],
    selected_columns: str,
) -> list[str]:
    """Select subgroup of a list of CSV headers.

    Args:
    ----
        csv_headers (Sequence[str]): The list of CSV headers.
        selected_columns (str): Columns to be selected, separated by commas.
            If empty, all headers are selected.

    Returns:
    -------
        list[str]: The selected headers.

    Example:
    -------
        >>> select_headers(['a', 'b', 'c'], 'b,c')
        ['b', 'c']

    """
    return (
        selected_columns.split(',') if selected_columns else list(csv_headers)
    )


def validate_headers(
    selected_headers: list[str],
    csv_headers: Sequence[str],
) -> None:
    """Validate that all selected headers exist in the CSV headers.

    Args:
    ----
        selected_headers (list[str]): List of headers to be selected.
        csv_headers (Sequence[str]): Sequence of headers from the CSV
        file/string.

    Raises:
    ------
        ValueError:
            If any of the selected headers are not found in the CSV headers.

    """
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
    """Reorders the headers list based on the order in the original CSV.

    Args:
    ----
        selected_headers (list[str]): The list of headers to be selected.
        csv_headers (Sequence[str]): The list of headers from the CSV file.

    Returns:
    -------
        list[str]: The reordered list of headers.

    Example:
    -------
        >>> selected_headers = ["header2", "header1"]
        >>> csv_headers = ["header1", "header2", "header3"]
        >>> reorder_headers(selected_headers, csv_headers)
        ["header1", "header2"]

    """
    return [header for header in csv_headers if header in selected_headers]


def parse_filters(
    row_filter_definitions: str,
) -> dict[str, list[tuple[str, str]]]:
    """Parse the row filter definitions to create a dictionary of filters.

    Args:
    ----
        row_filter_definitions (str): A string containing multiple row filter
        definitions.

    Returns:
    -------
        dict[str, list[tuple[str, str]]]: A dictionary where keys are column
        names and values are lists of tuples representing the comparison
        operator and the filter value.

    Example:
    -------
        >>> parse_filters("header1=value1,header2>value2")
        {'header1': [('=', 'value1')], 'header2': [('>', 'value2')]}

    """
    filters: dict[str, list[tuple[str, str]]] = {}
    for filter_definition in row_filter_definitions.splitlines():
        column, cp_operator, value = parse_filter(filter_definition)
        if column not in filters:
            filters[column] = []
        filters[column].append((cp_operator, value))

    return filters


def parse_filter(filter_definition: str) -> tuple[str, str, str]:
    """Parse a filter definition string.

    Args:
    ----
        filter_definition (str): A string representing a filter definition.

    Returns:
    -------
        tuple[str, str, str]: A tuple containing the column name (str), the
    comparison operator (str), and the filter value (str).

    Raises:
    ------
        ValueError: If the filter_definition doesn't contain a valid comparison
        operator.

    Example:
    -------
        >>> parse_filter("header1=value1")
        ('header1', '=', 'value1')

    """
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
    """Validate that all filters' headers exist in the CSV headers.

    Args:
    ----
        filters (dict[str, list[tuple[str, str]]): Dictionary of filters with
        headers and values.
        csv_headers (Sequence[str]): Sequence of headers from the CSV
        file/string.

    Raises:
    ------
        ValueError:
            If any of the filtered headers are not found in the CSV headers.

    """
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
    """Filter the CSV data based on the selected headers and filters.

    Args:
    ----
        csv_reader (DictReader[str]): The CSV file reader object.
        selected_headers (list[str]): The list of headers to be selected from
        the CSV data.
        filters (dict[str, list[tuple[str, str]]]): The dictionary of filters
        with headers and values.

    Returns:
    -------
        list[dict[str, str]]: The filtered CSV data as a list of dictionaries,
        where each dictionary represents a row and contains only the selected
        headers.

    """
    return [
        {col: row[col] for col in selected_headers}
        for row in csv_reader
        if row_meets_filters(row, filters)
    ]


def row_meets_filters(
    row: dict[str, str],
    filters: dict[str, list[tuple[str, str]]],
) -> bool:
    """Check if a row meets the specified filters.

    Args:
    ----
        row (dict[str, str]): A dictionary representing a row with column names
        as keys and cell contents as values.
        filters (dict[str, list[tuple[str, str]]]): A dictionary of filters
        where keys are column names and values are lists of tuples representing
        the comparison operator and the filter value.

    Returns:
    -------
        bool: True if the row meets all the specified filters, False otherwise.

    """
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
) -> str:
    r"""Write CSV data to a string buffer and return the buffer content string.

    Args:
    ----
        filtered_rows (list[dict[str, str]]): Rows to be written to the CSV.
        selected_headers (list[str]): Headers to be written to the CSV.

    Returns:
    -------
        str: CSV data as a string.

    """
    output = io.StringIO()
    csv_writer = DictWriter(
        output,
        fieldnames=selected_headers,
        lineterminator='\n',
        quotechar=None,
        quoting=QUOTE_NONE,
    )
    csv_writer.writeheader()
    csv_writer.writerows(filtered_rows)

    return output.getvalue()
