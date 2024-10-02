# from collections import deque
from typing import Any
from markdownify import markdownify as md
import requests
import numpy as np
import pyperclip


def aoc_open_input(filename: str) -> str:
    """
    Opens and reads the contents of a file.
    Parameters
    ----------
    filename : str
        The name of the file to be opened.
    Returns
    -------
    str
        The contents of the file as a string.
    Raises
    ------
    FileNotFoundError
        If the file does not exist.
    PermissionError
        If the user doesn't have permission to read the file.
    IOError
        For other I/O related errors.
    """
    try:
        with open(filename, encoding="utf-8") as file:
            return file.read()
    except (FileNotFoundError, PermissionError, IOError) as e:
        raise e


def aoc_adjacent_coordinates(
    i: int, j: int, include_diagonals: bool = False, only_positive_indices: bool = False
) -> np.ndarray:
    """
    Get adjacent coordinates of a given position, optionally including
    diagonals.

    Parameters
    ----------
    i : int
        Row index.
    j : int
        Column index.
    include_diagonals : bool, optional
        Flag indicating whether to include diagonal coordinates, by default
        False.
    only_positive_indices : bool, optional
        Flag indicating whether to include only positive row and column indices,
        by default False.

    Returns
    -------
    np.ndarray
        An array containing adjacent coordinates. If include_diagonals is True,
        it includes diagonal coordinates (up, down, left, right, upper-left,
        upper-right, lower-left, lower-right). Otherwise, it includes only up,
        down, left, and right coordinates. If only_positive_indices is True, it
        filters out negative row and column indices.
    """
    # Generate coordinates using meshgrid
    row_offsets = np.array([-1, 1, 0, 0])
    col_offsets = np.array([0, 0, -1, 1])

    if include_diagonals:
        row_offsets = np.concatenate([row_offsets, [-1, -1, 1, 1]])
        col_offsets = np.concatenate([col_offsets, [-1, 1, -1, 1]])

    adjacent_coordinates = np.column_stack((i + row_offsets, j + col_offsets))

    if only_positive_indices:
        # Filter out negative indices
        positive_indices_mask = (adjacent_coordinates >= 0).all(axis=1)
        adjacent_coordinates = adjacent_coordinates[positive_indices_mask]

    return adjacent_coordinates


def aoc_grid(test_string: str) -> dict:
    """
    Create a dictionary representing a grid from a string.

    Parameters
    ----------
    test_string : str
        Input string representing the grid.

    Returns
    -------
    dict
        A dictionary where keys are tuple coordinates (i, j) and values are
        corresponding characters from the grid.
    """

    return {
        (i, j): x
        for i, row in enumerate(test_string.splitlines())
        for j, x in enumerate(row)
    }


def aoc_shape(input_str: str) -> tuple[int, int]:
    """
    Determine the shape of a grid represented by the input string.

    Parameters
    ----------
    input_str : str
        Input string representing the grid.

    Returns
    -------
    tuple[int, int]
        A tuple containing the shape of the grid, where the first element is the
        number of columns (length_columns) and the second element is the number
        of rows (length_rows).
    """

    listed_str = input_str.splitlines()

    return {
        "length_rows": len(listed_str),
        "length_columns": max(len(line) for line in listed_str),
    }


def aoc_nxn_array(dimensions: int) -> list[list]:
    """
    Creates a 2D array (list of lists) with dimensions NxN, initialized with zeros.

    Parameters
    ----------
    dimensions : int
        The number of rows and columns in the array.

    Returns
    -------
    list[list]
        A 2D array of dimensions NxN filled with zeros.
    """
    return [[0 for _ in range(dimensions)] for _ in range(dimensions)]


def aoc_three_dimensional_array(
    rows: int, columns: int, element_size: int
) -> list[list[list[int]]]:
    """
    Creates a 3D array (list of lists of lists) with specified dimensions,
    where each element in the array is initialized to zero.

    Parameters
    ----------
    rows : int
        The number of rows in the array.
    columns : int
        The number of columns in each row.
    element_size : int
        The size of each element in the innermost list.

    Returns
    -------
    list[list[list[int]]]
        A 3D array with specified dimensions,
        initialized with zeros in each element.
    """
    return [
        [[0 for _ in range(element_size)] for _ in range(columns)] for _ in range(rows)
    ]


def aoc_grid_dictionary(
    grid_size: int, default_value: int
) -> dict[tuple[int, int], int]:
    """
    Create a dictionary representing a grid of given size with default values.

    Parameters
    ----------
    grid_size : int
        The size of the grid in both dimensions (width and height).
    default_value : int
        The default value to associate with each coordinate in the grid.

    Returns
    -------
    dict[tuple[int, int], int]
        A dictionary where keys are (x, y) coordinates within the specified
        grid_size, and values are set to the provided default_value.

    Example
    -------
    >>> grid = aoc_grid_dictionary(3, 0)
    >>> print(grid)
    {
        (0, 0): 0, (0, 1): 0, (0, 2): 0,
        (1, 0): 0, (1, 1): 0, (1, 2): 0,
        (2, 0): 0, (2, 1): 0, (2, 2): 0
    }
    """
    return {
        (x, y): default_value
        for x, y in itertools.product(range(grid_size), range(grid_size))
    }


def aoc_answer_display(obj):
    r"""
    Attempt to display an object using IPython.display, or print if unavailable.

    Parameters
    ----------
    obj : any
        The object to be displayed or printed.

    Returns
    -------
    obj
        Object

    Examples
    --------
    >>> try_display("Hello, World!")
    Hello, World!
    """
    try:
        from IPython.display import display
        from aoc_utils import aoc_open_input

        pyperclip.copy(obj)
        # return obj
    except ImportError:
        pyperclip.copy(obj)
        print(obj)
    return obj


def aoc_print_functions(verbose: bool = False):
    """
    Print all functions in the local namespace that start with "aoc_".
    """
    # Get all items in the local namespace
    # local_items = locals().items()
    global_items = globals().items()

    # Filter and print functions that start with "aoc_"
    aoc_functions = {
        name: obj
        for name, obj in global_items
        if callable(obj) and name.startswith("aoc_")
    }

    print(aoc_functions)

    if verbose:
        for name, function in aoc_functions.items():
            print(f"Function: {name}")
            print(f"{'-' * 40}")
            print(function.__doc__)
            print("\n" + "=" * 40 + "\n")


def aoc_head_dict(d: dict, n: int) -> dict:
    """
    Create a new dictionary containing the first `n` items from the input
    dictionary.

    Parameters
    ----------
    d : dict
        The input dictionary.
    n : int
        The number of items to include in the new dictionary.

    Returns
    -------
    dict
        A new dictionary containing the first `n` items from the input
        dictionary.
    """
    return {k: v for i, (k, v) in enumerate(d.items()) if i < n}


def aoc_filter_valid_coordinates(
    arr: np.ndarray, coordinates: np.ndarray
) -> np.ndarray:
    """
    Filters out coordinates that do not exist in array.

    Parameters
    ----------
    arr : np.ndarray
        The input array
    coordinates : np.ndarray
        The array of coordinates of `arr`

    Returns
    -------
    np.ndarray
        Filtered out array with valid coordinates
    """
    max_row, max_col = arr.shape

    # Create boolean masks for valid rows and columns
    valid_rows = (coordinates[:, 0] >= 0) & (coordinates[:, 0] < max_row)
    valid_cols = (coordinates[:, 1] >= 0) & (coordinates[:, 1] < max_col)

    # Combine the boolean masks to get the final valid coordinates
    valid_coordinates_mask = valid_rows & valid_cols

    # Use boolean indexing to filter out invalid coordinates
    valid_coordinates = coordinates[valid_coordinates_mask]

    return valid_coordinates


def aoc_transpose_list_of_lists(input_list: list[list[Any]]) -> list[list[Any]]:
    """
    Transposes a list of lists (matrix) such that the rows become columns and vice versa.

    Parameters
    ----------
    input_list : list[list[Any]]
        A list of lists representing a matrix, where each inner list is a row.

    Returns
    -------
    list[list[Any]]
        A new list of lists where the rows of the input are converted into columns.
        The ith row in the output corresponds to the ith column in the input.

    Examples
    --------
    >>> input_list = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    >>> aoc_transpose_list_of_lists(input_list)
    [[1, 4, 7], [2, 5, 8], [3, 6, 9]]
    """
    return list(map(lambda *x: list(x), *(input_list)))


def aoc_retrive_question_text() -> None:
    url = pyperclip.paste()
    text = (
        md(requests.get(url).text)
        .replace("\n* ", "\n- ")
        .replace(r"\-\-\-", "---")
        .replace("*", "**")
        .replace("\n\n", "\n")
    )
    start = text.find("---")
    end = text.find("To play,")

    final_draft = text[start:end].replace("--- Day", "## --- Day").splitlines()

    lines_to_delete = {1: "", -1: ""}

    for k, v in lines_to_delete.items():
        final_draft[k] = v

    final_text = "\n".join(final_draft)

    pyperclip.copy(final_text)


def aoc_part_two_text() -> None:
    pyperclip.copy(pyperclip.paste().replace("*", "**"))
