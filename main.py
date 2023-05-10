from sudoku_solver import bt_solve, fc_solve, ac_solve
from utils import generate_sudoku_string
from sudoku_data import sudoku_strings
import time

def printer(solutions, CSP):
    if len(solutions) == 0:
        print("No solution found\n")
    else:
        for solution in solutions:
            print(generate_sudoku_string(solution, CSP))
            print()


def main():
    '''
    Each value is separated by a space
    A zero means an empty cell on the sudoku grid
    '''

    # Store execution time for backtracking
    bt_times = []
    print("Solutions\n")
    for i in sudoku_strings :
        print("Backtracking \n")
        start_time = time.time()
        printer(*bt_solve(i))
        end_time = time.time()
        bt_times.append(end_time - start_time)

    # Store execution time for forward checking
    fc_times = []
    for i in sudoku_strings :
        print("Forward Checking\n")
        start_time = time.time()
        printer(*fc_solve(i))
        end_time = time.time()
        fc_times.append(end_time - start_time)

    # Store execution time for arc consistency
    ac_times = []
    for i in sudoku_strings :
        print("Arc Consistency\n")
        start_time = time.time()
        printer(*ac_solve(i))
        end_time = time.time()
        ac_times.append(end_time - start_time)

    # Print the execution time arrays
    print("Backtracking times:", bt_times)
    print("Forward checking times:", fc_times)
    print("Arc consistency times:", ac_times)



if __name__ == "__main__":
    main()
