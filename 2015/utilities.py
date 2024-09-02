import numpy as np
import pyperclip


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

        pyperclip.copy(obj)
        # return obj
    except ImportError:
        pyperclip.copy(obj)
        print(obj)
    return obj


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

    return np.array(
        [
            (row, col)
            for row, col in coordinates
            if 0 <= row < max_row and 0 <= col < max_col
        ]
    )


def aoc_adjacent_coordinates(
    i: int, j: int, include_diagonals: bool = False, only_positive_indices: bool = False
) -> tuple[int, int]:
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
    tuple
        A tuple containing adjacent coordinates. If include_diagonals is True,
        it includes diagonal coordinates (up, down, left, right, upper-left,
        upper-right, lower-left, lower-right). Otherwise, it includes only up,
        down, left, and right coordinates. If only_positive_indices is True, it
        filters out negative row and column indices.
    """

    result = [(i - 1, j), (i + 1, j), (i, j - 1), (i, j + 1)]

    if include_diagonals:
        result += [(i - 1, j - 1), (i - 1, j + 1), (i + 1, j - 1), (i + 1, j + 1)]

    if only_positive_indices:
        result = [(row, col) for row, col in result if row >= 0 and col >= 0]

    return result


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
    """
    return open(filename, encoding="utf-8").read()
