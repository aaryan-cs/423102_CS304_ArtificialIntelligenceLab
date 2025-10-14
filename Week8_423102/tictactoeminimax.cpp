#include <iostream>
#include <vector>
#include <algorithm>
#include <limits>
#include <chrono>
#include <iomanip>
using namespace std;
using namespace std::chrono;

vector<string> board = {"-","-","-","-","-","-","-","-","-"};

void printBoard(){
    cout << board[0] << " | " << board[1] << " | " << board[2] << endl;
    cout << board[3] << " | " << board[4] << " | " << board[5] << endl;
    cout << board[6] << " | " << board[7] << " | " << board[8] << endl;
}

bool isValidPosition(int position){
    if(position < 0 || position > 8 || board[position] == "X" || board[position] == "O") return false;
    return true;
}

void takeTurn(string player){
    cout<< player << "'s turn." << endl;
    cout << "Enter a postion from 1-9:" << endl;
    int position;
    cin >> position;
    position--;
    while(!isValidPosition(position)){
        cout << "Position " << position + 1 << " is invalid.\nEnter a valid position between 1-9: ";
        cin >> position;
        position--;
    }
    board[position] = player;
    printBoard();
}

string gameState(){
    // win state
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
    else if(count(board.begin(),board.end(),"-") == 0) return "tie";

    else return "play";
}

string checkWinner(){
    vector<vector <int>> winPatterns = {
        {0,1,2}, {3,4,5}, {6,7,8},{0,3,6}, {1,4,7}, {2,5,8},{0,4,8},{2,4,6}
    };
    for(auto pattern : winPatterns){
        if(board[pattern[0]] != "-" && board[pattern[0]] == board[pattern[1]] && board[pattern[1]] == board[pattern[2]]){
            return board[pattern[0]];
        }
    }
    return "-";
}

bool isMovesLeft(){
    return count(board.begin(),board.end(),"-") > 0;
}

int evaluationFunction(){
    string winner = checkWinner();
    if(winner == "X"){
        return -1;
    }
    else if(winner == "O") return 1;

    else return 0;
}
int minimax(bool isMaximizing) {
    int score = evaluationFunction();
    if (score == 1 || score == -1) return score;
    if (!isMovesLeft()) return 0;

    if (isMaximizing) {
        int best = -numeric_limits<int>::max();
        for (int i = 0; i < 9; i++) {
            if (board[i] == "-") {
                board[i] = "O";
                int val = minimax(false);
                board[i] = "-";
                best = max(best, val);
            }
        }
        return best;
    } else {
        int best = numeric_limits<int>::max();
        for (int i = 0; i < 9; i++) {
            if (board[i] == "-") {
                board[i] = "X";
                int val = minimax(true);
                board[i] = "-";
                best = min(best, val);
            }
        }
        return best;
    }
}

int minimaxWithAlphaBeta(bool isMaximizing, int alpha, int beta){
    int score = evaluationFunction();
    if(score == 1 || score == -1) return score;
    if(!isMovesLeft()) return 0;

    if(isMaximizing){
        int best = -numeric_limits<int>::max();
        for(int i = 0; i < 9; i++){
            if(board[i] == "-"){
                board[i] = "O";
                int val = minimaxWithAlphaBeta(false, alpha, beta);
                board[i] = "-";
                best = max(best, val);
                alpha = max(alpha, best);
                if(beta <= alpha) break;
            }
        }
        return best;
    }
    else{
        int best = numeric_limits<int>::max();
        for(int i = 0; i < 9; i++){
            if(board[i] == "-"){
                board[i] = "X";
                int val = minimaxWithAlphaBeta(true,alpha,beta);
                board[i] = "-";
                best = min(best, val);
                beta = min(beta,best);
                if(beta<=alpha) break;
            }
        }
        return best;
    }
}    

int pickBestMove(){
    int bestVal = numeric_limits<int>::max();;
    int bestMove = -1;
    for(int i =0 ;i<9; i++){
        if(board[i] == "-"){
            board[i] = "X";
            int moveVal = minimaxWithAlphaBeta(true,-numeric_limits<int>::max(), numeric_limits<int>::max());
            board[i] = "-";
            if(moveVal < bestVal){
                bestMove = i;
                bestVal = moveVal;
            }
        }
    }
    return bestMove;
}    

void compareMinimaxSpeeds() {
    board = {"X", "O", "X", "-", "O", "-", "-", "-", "-"};

    cout << "\n--- Comparing Minimax vs Alpha-Beta Pruning ---\n";

    auto start1 = high_resolution_clock::now();
    for (int i = 0; i < 200; i++)
        minimax(true);  // minimax
    auto end1 = high_resolution_clock::now();
    auto duration1 = duration_cast<milliseconds>(end1 - start1).count();

    auto start2 = high_resolution_clock::now();
    for (int i = 0; i < 200; i++)
        minimaxWithAlphaBeta(true, -1e9, 1e9);  // alpha-beta
    auto end2 = high_resolution_clock::now();
    auto duration2 = duration_cast<milliseconds>(end2 - start2).count();

    cout << "\nExecution Time Comparison:\n";
    cout << "+-------------------------+------------------+\n";
    cout << "| Algorithm               |     Time (ms)    |\n";
    cout << "+-------------------------+------------------+\n";
    cout << "| Minimax (no pruning)    | " << setw(16) << duration1 << " |\n";
    cout << "| Alpha-Beta Pruning      | " << setw(16) << duration2 << " |\n";
    cout << "+-------------------------+------------------+\n";

    
}


int main() {
    printBoard();
    string currentPlayer = "X";
    bool gameOver = false;
    while (!gameOver) {
        if (currentPlayer == "X") {
            cout << "Bot is making a move..." << endl;
            int aiMove = pickBestMove();
            board[aiMove] = "X";
            printBoard();
        } else {
            takeTurn(currentPlayer);
        }
        string gameResult = gameState();
        if (gameResult == "win") {
            cout << currentPlayer << " wins!" << endl;
            gameOver = true;
        } else if (gameResult == "tie") {
            cout << "It's a tie!" << endl;
            gameOver = true;
        } else {
            currentPlayer = currentPlayer == "X" ? "O" : "X";
        }
    }
    compareMinimaxSpeeds();
    return 0;
}
