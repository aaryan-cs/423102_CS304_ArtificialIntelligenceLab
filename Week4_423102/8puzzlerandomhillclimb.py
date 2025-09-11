import random

def check_solvability(state):
    inv_count = 0
    for i in range(8):
        for j in range(i + 1, 9):
            if state[i] != 0 and state[j] != 0 and state[i] > state[j]:
                inv_count += 1
    return inv_count % 2 == 0

def print_states(state):
    for i in range(0,9,3):
        print(state[i:i+3])
    print()


def init_random_initial_state():
    while True:
        state = list(range(9))
        random.shuffle(state)
        if check_solvability(state):
            return state


def manhattan(state):
    goal = {i: (i // 3, i % 3) for i in range(9)}  # goal = [0,1,2,3,4,5,6,7,8]
    return sum(abs(i // 3 - goal[val][0]) + abs(i % 3 - goal[val][1])
               for i, val in enumerate(state) if val != 0)


def get_neighbors(state):
    neighbors = []
    idx = state.index(0)
    row, col = divmod(idx, 3)
    moves = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    for dr, dc in moves:
        r, c = row + dr, col + dc
        if 0 <= r < 3 and 0 <= c < 3:
            new_idx = r * 3 + c
            new_state = list(state)
            new_state[idx], new_state[new_idx] = new_state[new_idx], new_state[idx]
            neighbors.append(new_state)
    return neighbors

# normal hill climb
def hill_climb_8puzzle(start, max_iters=500):
    current = start
    current_h = manhattan(current)

    for _ in range(max_iters):
        neighbors = get_neighbors(current)
        better = [n for n in neighbors if manhattan(n) < current_h]
        if not better:  # stuck in local min
            break
        current = random.choice(better)
        current_h = manhattan(current)
        if current_h == 0:  # solved
            return current, True
    return current, False

# random restart
def puzzle_random_restart(restarts=20, max_iters=1000):
    best_state, solved_any = None, False
    for _ in range(restarts):
        start = init_random_initial_state()  # new random solvable start each restart
        state, solved = hill_climb_8puzzle(start, max_iters)
        if solved:
            return state, True
        if best_state is None or manhattan(state) < manhattan(best_state):
            best_state = state
    return best_state, False

if __name__ == "__main__":
    solution, solved = puzzle_random_restart(restarts=20, max_iters=1000)
    print("Final board: ", solution, "Solved?:", solved)
