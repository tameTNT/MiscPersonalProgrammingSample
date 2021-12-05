from typing import Any, List, Optional


def transpose_2d_list(list_: List[List[Any]]) -> List[List[Any]]:
    """
    Transposes a 2D list (i.e. flips rows and columns).

    See https://en.wikipedia.org/wiki/Transpose
    """

    num_columns = len(list_[0])
    columns = [[] for _ in range(num_columns)]
    for row in list_:
        if len(row) != num_columns:
            raise ValueError('All rows must be of same length.')

        for col_index, item in enumerate(row):
            columns[col_index].append(item)

    return columns


def pad_items(items: List[str], centered: bool) -> None:
    """
    Determines the width of the widest item in items and then pads all items IN-PLACE accordingly

    :param items: List of items to pad
    :param centered: Whether the items should be padded for centre alignment. If False, items are left-aligned
    """

    max_width = 0
    for item in items:
        # updates max_width if current item wider than widest so far
        max_width = max(len(item), max_width)

    for i in range(len(items)):
        current_item = items[i]
        width_dif = max_width - len(current_item)

        if centered:
            if width_dif % 2 == 1:  # odd width difference so make it even so it can be split up evenly
                current_item += ' '
                width_dif -= 1
            half_width_dif = width_dif // 2
            # don't forget 1 space padding either side
            items[i] = f' {" " * half_width_dif}{current_item}{" " * half_width_dif} '
        else:
            items[i] = f' {current_item}{" " * width_dif} '


def build_table_from_rows(rows: List[List[str]], labels_exist: bool) -> str:
    """
    :param rows: 2D list of str items to construct table from
    :param labels_exist: True indicates that the first list in rows contains the column labels
    :return: str to be used with print() to print formatted table
    """

    num_columns = len(rows[0])
    column_widths = {col_index: len(rows[0][col_index]) for col_index in range(num_columns)}

    # top-most line of output_str
    output_str = '┌'
    for i in range(num_columns):
        output_str += '─' * column_widths[i]
        if i == num_columns - 1:  # final column
            output_str += '┐\n'
        else:
            output_str += '┬'

    # (optional) labels section of output_str
    if labels_exist:
        labels = rows[0]
        rows = rows[1:]  # remove labels row from rows

        output_str += f'│{"│".join(labels)}│\n'

        output_str += '├'
        for i in range(num_columns):
            output_str += '─' * column_widths[i]
            if i == num_columns - 1:  # final column
                output_str += '┤\n'
            else:
                output_str += '┼'

    # middle/content rows of output_str
    for row_index in range(len(rows)):
        output_str += f'│{"│".join(rows[row_index])}│\n'

    # bottom line of output_str
    output_str += '└'
    for i in range(num_columns):
        output_str += '─' * column_widths[i]
        if i == num_columns - 1:  # final column
            output_str += '┘'
        else:
            output_str += '┴'

    return output_str


def make_table(rows: List[List[Any]], labels: Optional[List[Any]] = None, centered: bool = False) -> str:
    """
    :param rows: 2D list containing objects that have a single-line representation (via `str`).
        All rows must be of the same length.
    :param labels: List containing the column labels. If present, the length must equal to that of each row.
    :param centered: If the items should be aligned to the center, else they are left aligned.
    :return: A table representing the rows passed in.
    """

    rows_with_labels = list(rows)  # create copy of rows list (to insert labels into) to avoid mutating original args

    if labels:
        num_columns = len(rows[0])
        if len(labels) != num_columns:
            raise ValueError('Length of labels list must equal to length of each row.')

        # adds labels to head of rows list (index 0) to be considered for width later on
        rows_with_labels.insert(0, labels)

    # apply str() to every object
    rows_with_labels: List[List[str]] = [list(map(str, row)) for row in rows_with_labels]

    columns = transpose_2d_list(rows_with_labels)

    for column in columns:
        pad_items(column, centered)

    padded_rows = transpose_2d_list(columns)

    return build_table_from_rows(padded_rows, bool(labels))
