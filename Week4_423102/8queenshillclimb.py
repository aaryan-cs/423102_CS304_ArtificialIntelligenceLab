import random
def attacking_pairs(board):
    n = len(board)
    attacks = 0
    for i in range(n):
        for j in range(i+1, n):
            if board[i] == board[j] or abs(board[i]-board[j]) == j-i:
                attacks += 1
    return attacks

def hill_climb_8queens(n=8, max_iters=1000):
    board = [random.randint(0, n-1) for _ in range(n)]
    current_h = attacking_pairs(board)

    for _ in range(max_iters):
        if current_h == 0:
            return board, True
        i = random.randint(0, n-1)
        best_move = board[i]
        best_h = current_h
        for row in range(n):
            if row != board[i]:
                new_board = board[:]
                new_board[i] = row
                h = attacking_pairs(new_board)
                if h < best_h:
                    best_h = h
                    best_move = row
        if best_h < current_h:
            board[i] = best_move
            current_h = best_h
    return board, (current_h == 0)

def queens_random_restart(n=8, restarts=50, max_iters=1000):
    best_board, best_h = None, float("inf")
    for _ in range(restarts):
        board, solved = hill_climb_8queens(n, max_iters)
        h = attacking_pairs(board)
        if solved:
            return board, True
        if h < best_h:
            best_board, best_h = board, h
    return best_board, False

if __name__ == "__main__":
    solution, solved = queens_random_restart()
    print("Board:", solution, "Solved:", solved)