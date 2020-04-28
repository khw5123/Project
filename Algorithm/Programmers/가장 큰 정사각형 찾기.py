def solution(board):
    answer = 1 if any(sum(board[h]) for h in range(len(board))) else 0
    for h in range(1, len(board)):
        for w in range(1, len(board[0])):
            if board[h][w] == 1:
                board[h][w] = min(board[h-1][w-1], min(board[h][w-1], board[h-1][w])) + 1
                answer = max(answer, board[h][w])
    return answer * answer