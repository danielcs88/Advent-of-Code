def open_input(filename):
    return open(filename, encoding="utf-8").read()


def nxn_array(dimensions: int) -> list[list]:
    return [[0 for _ in range(dimensions)] for _ in range(dimensions)]


def three_dimensional_array(
    rows: int, columns: int, element_size: int
) -> list[list[list[int]]]:
    return [
        [[0 for _ in range(element_size)] for _ in range(columns)] for _ in range(rows)
    ]
