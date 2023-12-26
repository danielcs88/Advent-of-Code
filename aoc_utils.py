# from collections import deque
import itertools


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


def aoc_adj(
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
