def grid_index_to_row_and_col(index):
    """
    Convert 1D index to 2D row and column coordinates in a 9x9 grid.
    """
    row = index // 9
    col = index % 9

    return row, col


def get_neighbors(cell_id):
    """
    Get all neighbors of a given cell in a 9x9 grid, including cells in the same row, column, and subgrid.
    """
    row, column = grid_index_to_row_and_col(cell_id)

    neighbors = set()

    # get row
    for i in range(9):
        neighbors.add(9 * row + i)

    # get column
    for i in range(9):
        neighbors.add(i * 9 + column)

    # get subgrid
    start_row = row - (row % 3)
    start_column = column - (column % 3)
    for i in range(3):
        for j in range(3):
            neighbors.add((i + start_row) * 9 + (j + start_column))

    neighbors.remove(cell_id)

    return list(neighbors)


def parse_grid_string(sudoku_string):
    """
    Parse a string representing a 9x9 Sudoku grid into a 2D list of integers.
    """
    rows = sudoku_string.strip().split("\n")
    return [[int(num) for num in row.split()] for row in rows]


def is_valid_assignment(grid, number, index):
    """
    Check if assigning a given number to a cell at a given index in the grid violates any constraints of the Sudoku puzzle.
    """
    row, column = grid_index_to_row_and_col(index)

    # check row
    for i in range(9):
        if grid[row][i] == number:
            return False
 
    # check column
    for i in range(9):
        if grid[i][column] == number:
            return False
 
    # check subgrid
    start_row = row - (row % 3)
    start_column = column - (column % 3)
    for i in range(3):
        for j in range(3):
            if grid[i + start_row][j + start_column] == number:
                return False

    return True


def generate_CSP(sudoku_grid_string):
    """
    Generate a Constraint Satisfaction Problem (CSP) for solving a 9x9 Sudoku puzzle.
    """
    N = 9 * 9 # number of cells

    # create the variable list
    variables = [col for col in range(N)]

    # create the domain for each variable in variables list
    domains = {var: [pos for pos in range(1, 10)] for var in variables}

    # find the neighbors for each variable
    neighbors = {var: get_neighbors(var) for var in variables}

    # create a CSP dictionary
    csp = {
        "variables": variables,
        "domains": domains,
        "neighbors": neighbors
    }

    grid = parse_sudoku_grid_string(sudoku_grid_string)

    # update domain with any given values in the Sudoku grid
    for i in range(81):
        row, col = grid_index_to_row_and_col(i)

        given_value = grid[row][col]

        if given_value != 0:
            csp.get("domains")[i] = [given_value]

    return csp


def generate_assignment(CSP):
    """
    Creates an empty assignment dictionary with all variables as keys and empty lists as values.
    """
    return {var: [] for var in CSP.get("variables")}


def generate_sudoku_string(assignment, CSP):
    """
    Generates a string representation of the sudoku grid based on the current assignment.
    """
    grid = ""

    for cell in range(81):
        grid += str(assignment.get(cell, [0])[0])

        if (cell + 1) % 9 == 0:
            if cell != 0 and cell != 80:
                grid += "\n"
        else:
            grid += " "

    return grid


def convert_assignment_to_grid(assignment, CSP):
    """
    Converts the current assignment to a 2D grid (list of lists) representation.
    """
    grid = [[0 for _ in range(9)] for _ in range(9)] 

    for i in range(81):
        given_assignment = CSP.get("domains").get(i)

        if len(given_assignment) == 1:
            row, col = grid_index_to_row_and_col(i)
            grid[row][col] = given_assignment[0]

    for key, dict_value in assignment.items():
        row, col = grid_index_to_row_and_col(key)

        if len(dict_value) != 0:
            grid[row][col] = dict_value[0]

    return grid


def is_consistent(value, variable, assignment, CSP):
    """
    Determines whether a given value is consistent with the current assignment for a given variable.
    """
    for neighbor in CSP.get("neighbors").get(variable):
        if value in assignment.get(neighbor, []):
            return False

    return True


def is_assignment_complete(assignment):
    """
    Checks whether the assignment is complete (i.e. every variable has an assigned value).
    """
    return all(len(value) != 0 for value in assignment.values())


def get_unassigned_variable(assignment, CSP):
    """
    Returns an unassigned variable (i.e. a variable with an empty assignment list).
    """
    return next((var for var, assigned_value in assignment.items() if len(assigned_value) == 0), None)


def none_inference(CSP, variable, assignment):
    """
    Placeholder function for no inference.
    """
    return True, CSP


def get_domain(variable, CSP):
    """
    Returns the domain (list of possible values) for a given variable.
    """
    return CSP.get("domains").get(variable, [])

