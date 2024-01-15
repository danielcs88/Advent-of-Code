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
