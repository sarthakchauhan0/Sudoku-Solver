from utils import get_neighbors, parse_grid_string, grid_index_to_row_and_col, is_valid_assignment, generate_assignment, generate_CSP
from collections import deque
from helper import recursion_helper
import copy

def generate_CSP(sudoku_string):
    '''
    generates a CSP for a given Sudoku grid string
    '''
    N = 9 * 9  
    variables = [col for col in range(N)]
    domains = {var: [pos for pos in range(1, 10)] for var in variables}
    neighbors = {var: get_neighbors(var) for var in variables}
    csp = {
        "variables": variables,
        "domains": domains,
        "neighbors": neighbors
    }
    grid = parse_grid_string(sudoku_string)
    for i in range(81):
        row, col = grid_index_to_row_and_col(i)
        given_value = grid[row][col]
        if given_value > 0 and given_value < 10:
            grid[row][col] = 0
            if is_valid_assignment(grid, given_value, i):
                csp.get("domains")[i] = [given_value]
            else:
                csp["domains"] = {var: [] for var in variables}
                break
            grid[row][col] = given_value
    return csp


def generate_assignment(CSP):
    '''
    generates an assignment dictionary based on the CSP and given values
    '''
    # create a dictionary with the values as empty lists
    assignment = {var: [] for var in CSP.get("variables")}

    # assigned given values to the variables
    for i in range(81):
        domain = CSP.get("domains").get(i)
        if len(domain) == 1:
            assignment.get(i).append(domain[0])
    return assignment


def bt_solve(grid_string, multipleSolutions=False):
    '''
    solves the Sudoku puzzle using backtracking
    '''
    CSP = generate_CSP(grid_string)
    assignment = generate_assignment(CSP)
    solutions = []
    recursion_helper(assignment, CSP, solutions, multipleSolutions)
    return solutions, CSP


def forward_checking(CSP, variable, assignment):
    '''
    eliminates inconsistent values from the domains of unassigned variables
    '''
    new_CSP = copy.deepcopy(CSP)
    for neighbor in new_CSP.get("neighbors").get(variable):
        if assignment.get(variable)[0] in new_CSP.get("domains").get(neighbor):
            new_CSP.get("domains").get(neighbor).remove(assignment.get(variable)[0])
            if len(new_CSP.get("domains").get(neighbor)) == 0:
                return False, new_CSP
    return True, new_CSP


def fc_solve(grid_string, multipleSolutions = False):
    '''
    solves the Sudoku puzzle using forward checking
    '''
    CSP = generate_CSP(grid_string)
    assignment = generate_assignment(CSP)
    solutions = []
    recursion_helper(assignment, CSP, solutions, multipleSolutions, forward_checking)
    return solutions, CSP

def conflicts(x, y):
    '''
    checks if two values conflict with each other
    '''
    return x == y


def revise_sudoku(CSP, Xi, Xj):
    '''
    eliminates inconsistent values from the domain of a variable using the AC-3 algorithm
    '''
    revised = False
    new_CSP = copy.deepcopy(CSP)
    for x in CSP.get("domains").get(Xi):
        broken = False
        for y in CSP.get("domains").get(Xj):
            if not conflicts(x, y):
                broken = True
                break
        if not broken:
            new_CSP.get("domains").get(Xi).remove(x)
            revised = True
    return revised, new_CSP



# def arc_consistency(CSP, revise=revise_sudoku):
#     '''
#     applies the AC-3 algorithm to ensure arc consistency
#     '''
#     queue = deque([(Xi, Xj) for Xi in CSP.get("variables") for Xj in CSP.get("neighbors").get(Xi)])
#     while len(queue) != 0:
#         Xi, Xj = queue.popleft()
#         revise_state, new_CSP = revise(CSP, Xi, Xj)
#         if revise_state: 
#             if len(new_CSP.get("domains").get(Xi)) == 0:
#                 return False, new_CSP
#             for xk in new_CSP.get("neighbors").get(Xi):
#                 if xk != Xj:
#                     queue.append((xk, Xi))
#             CSP = new_CSP
#     return True, CSP

def arc_consistency(CSP, revise=revise_sudoku):
    '''
    applies a modified version of AC-3 algorithm to ensure arc consistency and improving speed.
    
    '''
    queue = deque([(Xi, Xj) for Xi in CSP.get("variables") for Xj in CSP.get("neighbors").get(Xi)])
    support = {}
    for Xi in CSP.get("variables"):
        for Xk in CSP.get("neighbors").get(Xi):
            for x in CSP.get("domains").get(Xi):
                for y in CSP.get("domains").get(Xk):
                    if not conflicts(x, y):
                        if (Xi, Xk) not in support:
                            support[(Xi, Xk)] = []
                        support[(Xi, Xk)].append((x, y))
    
    while len(queue) != 0:
        Xi, Xj = queue.popleft()
        revised = False
        new_CSP = copy.deepcopy(CSP)
        for x in CSP.get("domains").get(Xi):
            inconsistent = True
            for (xk, yk) in support.get((Xi, Xj), []):
                if xk == x:
                    inconsistent = False
                    break
            if inconsistent:
                new_CSP.get("domains").get(Xi).remove(x)
                revised = True
        if revised:
            if len(new_CSP.get("domains").get(Xi)) == 0:
                return False, new_CSP
            for Xk in CSP.get("neighbors").get(Xi):
                if Xk != Xj:
                    queue.append((Xk, Xi))
            CSP = new_CSP
    return True, CSP


def ac_solve(grid_string, multipleSolutions = False):
    '''
    solves the Sudoku puzzle using arc consistency checking
    '''
    CSP = generate_CSP(grid_string)
    assignment = generate_assignment(CSP)
    solutions = []

    is_arc_consistent, new_csp = arc_consistency(CSP)

    if (is_arc_consistent):
        recursion_helper(assignment, new_csp, solutions, multipleSolutions)

    return solutions, new_csp

