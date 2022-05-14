import random

Human = -1
Computer = 1

def wins(board, player):
    win_boards = [
        [board[0][0], board[0][1], board[0][2]],
        [board[1][0], board[1][1], board[1][2]],
        [board[2][0], board[2][1], board[2][2]],
        [board[0][0], board[1][0], board[2][0]],
        [board[0][1], board[1][1], board[2][1]],
        [board[0][2], board[1][2], board[2][2]],
        [board[0][0], board[1][1], board[2][2]],
        [board[2][0], board[1][1], board[0][2]],
    ]
    return [player, player, player] in win_boards

def finished(board):
    return wins(board, "O") or wins(board, "X")

def emptyCell(board):
    ec = []
    for i, row in enumerate(board):
        for j, col in enumerate(row):
            if col is None:
                ec.append([i, j])
    return ec

def evalute(board):
    if wins(board, "X"):
        return -10
    if wins(board, "O"):
        return 10
    else:
        return 0
        
def minimax(srcBoard, depth, player, alpha, beta):
    board = srcBoard[:]
    
    if depth == 0 or finished(board):
        return [evalute(board), -1, -1]

    best = [-99999, -1, -1] if player == Computer else [99999, -1 -1]
    for c in emptyCell(board):
        i, j = c[0], c[1]
        board[i][j] = "O" if player == Computer else "X"
        score = minimax(board, depth-1, -player, alpha, beta)
        board[i][j] = None
        score[1], score[2] = i, j

        if player == Computer:
            if score[0] > best[0]:
                best = score
                alpha = max(best[0], alpha)
        else:
            if score[0] < best[0]:
                best = score
                beta = min(best[0], beta)

        if beta <= alpha:
            return best

    return best

def CMove(srcBoard):
    for c in emptyCell(srcBoard):
        i, j = c[0], c[1]

        if i == 0:
            if j == 0:
                if srcBoard[1][1] == 'X' and srcBoard[2][2] == 'X':
                    return [i, j]
            if j == 2:
                if srcBoard[1][1] == 'X' and srcBoard[2][0] == 'X':
                    return [i, j]
            if srcBoard[i + 1][j] == 'X' and srcBoard[i + 2][j] == 'X':
                return [i, j]
        if i == 2:
            if j == 0:
                if srcBoard[1][1] == 'X' and srcBoard[0][2] == 'X':
                    return [i, j]
            if j == 2:
                if srcBoard[1][1] == 'X' and srcBoard[0][0] == 'X':
                    return [i, j]
            if srcBoard[i - 1][j] == 'X' and srcBoard[i - 2][j] == 'X':
                return [i, j]
        if j == 0:
            if srcBoard[i][j + 1] == 'X' and srcBoard[i][j + 2] == 'X':
                return [i, j]
        if j == 2:
            if srcBoard[i][j - 1] == 'X' and srcBoard[i][j - 2] == 'X':
                return [i, j]
    if len(emptyCell(srcBoard)) > 0:
        return random.choice(emptyCell(srcBoard))