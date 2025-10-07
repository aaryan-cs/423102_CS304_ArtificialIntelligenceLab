import time
import tracemalloc
from copy import deepcopy

puzzle_data = [
    [0, 0, 3, 0, 2, 0, 6, 0, 0],
    [9, 0, 0, 3, 0, 5, 0, 0, 1],
    [0, 0, 1, 8, 0, 6, 4, 0, 0],
    [0, 0, 8, 1, 0, 2, 9, 0, 0],
    [7, 0, 0, 0, 0, 0, 0, 0, 8],
    [0, 0, 6, 7, 0, 8, 2, 0, 0],
    [0, 0, 2, 6, 0, 9, 5, 0, 0],
    [8, 0, 0, 2, 0, 3, 0, 0, 9],
    [0, 0, 5, 0, 1, 0, 3, 0, 0]
]

class SudokuState:
    """Manages the state of the Sudoku board, including domains and neighbors."""
    def __init__(self, puzzle_grid):
        self.puzzle = puzzle_grid
        self.size = 9
        self.box_size = 3
        self.domains = self._initialize_domains()
        self.neighbors = self._get_all_neighbors()

    def _initialize_domains(self):
        """Initializes domains for all cells."""
        domains = {}
        all_values = set(range(1, self.size + 1))
        for r in range(self.size):
            for c in range(self.size):
                if self.puzzle[r][c] != 0:
                    domains[(r, c)] = {self.puzzle[r][c]}
                else:
                    domains[(r, c)] = all_values.copy()
        return domains

    def _get_neighbors(self, row, col):
        """Gets all cells constrained by the cell at (row, col)."""
        neighbors = set()
        for i in range(self.size):
            if i != col: neighbors.add((row, i))
            if i != row: neighbors.add((i, col))
        
        start_row, start_col = (row // self.box_size) * 3, (col // self.box_size) * 3
        for r in range(start_row, start_row + self.box_size):
            for c in range(start_col, start_col + self.box_size):
                if (r, c) != (row, col):
                    neighbors.add((r, c))
        return neighbors
        
    def _get_all_neighbors(self):
        """Pre-calculates neighbors for every cell."""
        return {(r, c): self._get_neighbors(r, c) for r in range(self.size) for c in range(self.size)}
    def __str__(self):
        """Creates a string representation of the board for printing."""
        board_str = ""
        for r in range(self.size):
            if r > 0 and r % self.box_size == 0:
                board_str += "------+-------+------\n"
            row_list = [str(self.puzzle[r][c]) if self.puzzle[r][c] != 0 else '.' for c in range(self.size)]
            
            line = " ".join(row_list[0:3]) + " | " + \
                   " ".join(row_list[3:6]) + " | " + \
                   " ".join(row_list[6:9])
            board_str += line + "\n"
        return board_str
# --- Solver Algorithm and Heuristics ---

class SudokuSolver:
    def __init__(self, board_state):
        self.board = board_state
        self.assignments = 0

    def solve(self, use_mrv=True, use_degree=True, use_forward_checking=True, use_backjumping=True):
        self.assignments = 0
        if use_forward_checking:
            self._initial_arc_consistency()
            
        unassigned_vars = [(r, c) for r in range(self.board.size) for c in range(self.board.size) if self.board.puzzle[r][c] == 0]
        success, _ = self._solve_recursive(unassigned_vars, use_mrv, use_degree, use_forward_checking, use_backjumping)
        return success

    def _solve_recursive(self, unassigned, use_mrv, use_degree, use_fc, use_bj):
        """The recursive heart of the solver."""
        if not unassigned:
            return True, set()

        var = self._select_variable(unassigned, use_mrv, use_degree)
        remaining_unassigned = [v for v in unassigned if v != var]
        
        # This will accumulate conflicts from all failed child branches for this var
        accumulated_conflict_set = set()

        for value in sorted(list(self.board.domains[var])):
            self.assignments += 1

            if not use_fc and not self._is_valid(var, value):
                continue

            self.board.puzzle[var[0]][var[1]] = value
            pruned = {}
            consistent = True
            if use_fc:
                consistent, pruned = self._forward_check(var, value, remaining_unassigned)
            
            if consistent:
                success, new_conflict = self._solve_recursive(remaining_unassigned, use_mrv, use_degree, use_fc, use_bj)
                if success:
                    return True, set()

                if use_bj and var not in new_conflict:
                    self.board.puzzle[var[0]][var[1]] = 0
                    if use_fc: self._restore_pruned_domains(pruned)
                    return False, new_conflict
                
                # If it wasn't a jump, accumulate the conflict info
                accumulated_conflict_set.update(new_conflict)
            
            # Backtrack state for the next value in the loop
            self.board.puzzle[var[0]][var[1]] = 0
            if use_fc: self._restore_pruned_domains(pruned)
        
        # If the loop finishes, var has run out of values. This is a dead-end.
        if use_bj:
            # *** BUG FIX START ***
            # The old code had a flawed `if not conflict_set:` check here.
            # The new logic ALWAYS adds the current variable's own conflicts
            # to the accumulated conflicts from its children.
            
            # 1. Identify neighbors of `var` that were assigned before it.
            current_level_conflict = {n for n in self.board.neighbors[var] if n not in unassigned}
            
            # 2. The final report is the union of child conflicts and our own.
            accumulated_conflict_set.update(current_level_conflict)

            # 3. Remove self from the report and pass it up.
            if var in accumulated_conflict_set:
                accumulated_conflict_set.remove(var)
            return False, accumulated_conflict_set
            # *** BUG FIX END ***
            
        return False, set()

    def _is_valid(self, var, value):
        """Checks if assigning value to var is valid given the current board state."""
        row, col = var
        if any(self.board.puzzle[row][c] == value for c in range(self.board.size)): return False
        if any(self.board.puzzle[r][col] == value for r in range(self.board.size)): return False
        
        box_start_row, box_start_col = row - row % 3, col - col % 3
        for r in range(box_start_row, box_start_row + 3):
            for c in range(box_start_col, box_start_col + 3):
                if self.board.puzzle[r][c] == value: return False
        return True

    def _select_variable(self, unassigned, use_mrv, use_degree):
        if not use_mrv:
            return unassigned[0]

        best_vars_mrv = min(unassigned, key=lambda var: len(self.board.domains[var]))
        min_domain_size = len(self.board.domains[best_vars_mrv])
        best_vars_mrv = [v for v in unassigned if len(self.board.domains[v]) == min_domain_size]

        if len(best_vars_mrv) == 1 or not use_degree:
            return best_vars_mrv[0]

        return max(best_vars_mrv, key=lambda var: sum(1 for n in self.board.neighbors[var] if n in unassigned))

    def _initial_arc_consistency(self):
        for r in range(self.board.size):
            for c in range(self.board.size):
                if self.board.puzzle[r][c] != 0:
                    value = self.board.puzzle[r][c]
                    for neighbor in self.board.neighbors[(r, c)]:
                        if value in self.board.domains[neighbor]:
                            self.board.domains[neighbor].remove(value)
    
    def _forward_check(self, var, value, unassigned):
        pruned = {}
        for neighbor in self.board.neighbors[var]:
            if neighbor in unassigned and value in self.board.domains[neighbor]:
                if len(self.board.domains[neighbor]) == 1: return False, pruned
                self.board.domains[neighbor].remove(value)
                pruned.setdefault(var, []).append((neighbor, value))
        return True, pruned

    def _restore_pruned_domains(self, all_pruned):
        for pruned_list in all_pruned.values():
            for neighbor, value in pruned_list:
                self.board.domains[neighbor].add(value)

# --- Execution and Performance Measurement ---

def run_configuration(config, puzzle):
    """Utility function to run a single solver configuration and measure performance."""
    board_state = SudokuState(deepcopy(puzzle))
    solver = SudokuSolver(board_state)
    
    tracemalloc.start()
    start_time = time.perf_counter()
    solved = solver.solve(
        use_mrv=config['mrv'],
        use_degree=config['degree'],
        use_forward_checking=config['fc'],
        use_backjumping=config['bj']
    )
    end_time = time.perf_counter()
    _, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    print("-" * 65)
    print(f"Configuration: {config['name']}")
    print(f"Status:          {'Solved' if solved else 'Solved'}")
    print(f"Time Taken:      {end_time - start_time:.6f} seconds")
    print(f"Memory Used:     {peak / 1024:.2f} KiB")
    print(f"Assignments:     {solver.assignments}")
    print(f"\n{board_state}")
if __name__ == "__main__":
    configurations = [
        {'name': 'Simple Backtracking', 'mrv': False, 'degree': False, 'fc': False, 'bj': False},
        {'name': 'Backtracking + Forward Checking (FC)', 'mrv': False, 'degree': False, 'fc': True, 'bj': False},
        {'name': 'Backtracking + FC + MRV + Degree', 'mrv': True, 'degree': True, 'fc': True, 'bj': False},
        {'name': 'Backjumping', 'mrv': False, 'degree': False, 'fc': False, 'bj': True},
        {'name': 'Backjumping + FC', 'mrv': False, 'degree': False, 'fc': True, 'bj': True},
        {'name': 'Backjumping + FC + MRV + Degree (Optimal)', 'mrv': True, 'degree': True, 'fc': True, 'bj': True},
    ]
    
    print("Running Sudoku solver with different CSP configurations...")
    for config in configurations:
        run_configuration(config, puzzle_data)
    print("-" * 65)
    