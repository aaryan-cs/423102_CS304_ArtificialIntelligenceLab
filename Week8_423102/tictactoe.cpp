#include <iostream>
#include <vector>
#include <algorithm>

using namespace std;

// Game board is 1d array
vector<string> board = {"-", "-", "-", "-", "-", "-", "-", "-", "-"};

// printing the board
void printBoard() {
    cout << board[0] << " | " << board[1] << " | " << board[2] << endl;
    cout << board[3] << " | " << board[4] << " | " << board[5] << endl;
    cout << board[6] << " | " << board[7] << " | " << board[8] << endl;
}

//function to handle a player's turn
void takeTurn(string player) {
    cout << player << "'s turn." << endl;
    cout << "Choose a position from 1-9: ";
    int position;
    cin >> position;
    position -= 1;
    while (position < 0 || position > 8 || board[position] != "-") {
        cout << "Invalid input or position already taken. Choose a different position: ";
        cin >> position;
        position -= 1;
    }
    board[position] = player;
    printBoard();
}

// function to check if the game is over
string checkGameOver() {
    // win
    if ((board[0] == board[1] && board[1] == board[2] && board[0] != "-") ||
        (board[3] == board[4] && board[4] == board[5] && board[3] != "-") ||
        (board[6] == board[7] && board[7] == board[8] && board[6] != "-") ||
        (board[0] == board[3] && board[3] == board[6] && board[0] != "-") ||
        (board[1] == board[4] && board[4] == board[7] && board[1] != "-") ||
        (board[2] == board[5] && board[5] == board[8] && board[2] != "-") ||
        (board[0] == board[4] && board[4] == board[8] && board[0] != "-") ||
        (board[2] == board[4] && board[4] == board[6] && board[2] != "-")) {
        return "win";
    }
    // tie
    else if (count(board.begin(), board.end(), "-") == 0) {
        return "tie";
    }
    // Game is not over
    else {
        return "play";
    }
}
// Function to check for winner (returns 'X', 'O', or '-')
string checkWinner() {
    vector<vector<int>> winPatterns = {
        {0,1,2}, {3,4,5}, {6,7,8}, // rows
        {0,3,6}, {1,4,7}, {2,5,8}, // cols
        {0,4,8}, {2,4,6}           // diagonals
    };
    for (auto pattern : winPatterns) {
        if (board[pattern[0]] != "-" &&
            board[pattern[0]] == board[pattern[1]] &&
            board[pattern[1]] == board[pattern[2]]) {
            return board[pattern[0]];
        }
    }
    return "-";
}

bool isMovesLeft() {
    return count(board.begin(), board.end(), "-") > 0;
}

// Evaluate board: +10 for X win, -10 for O win, 0 for tie
int evaluate() {
    string winner = checkWinner();
    if (winner == "X") return +10;
    else if (winner == "O") return -10;
    return 0;
}
int minimax(bool isMaximizing) {
    int score = evaluate();
    if (score == 10 || score == -10) return score;
    if (!isMovesLeft()) return 0;

    if (isMaximizing) {
        int best = -1000;
        for (int i = 0; i < 9; i++) {
            if (board[i] == "-") {
                board[i] = "X";
                best = max(best, minimax(false));
                board[i] = "-";
            }
        }
        return best;
    } else {
        int best = 1000;
        for (int i = 0; i < 9; i++) {
            if (board[i] == "-") {
                board[i] = "O";
                best = min(best, minimax(true));
                board[i] = "-";
            }
        }
        return best;
    }
}

// Define the main game loop
int main() {
    printBoard();
    string currentPlayer = "X";
    bool gameOver = false;
    while (!gameOver) {
        takeTurn(currentPlayer);
        string gameResult = checkGameOver();
        if (gameResult == "win") {
            cout << currentPlayer << " wins!" << endl;
            gameOver = true;
        } else if (gameResult == "tie") {
            cout << "It's a tie!" << endl;
            gameOver = true;
        } else {
            // Switch to the other player
            currentPlayer = currentPlayer == "X" ? "O" : "X";
        }
    }
    return 0;
}