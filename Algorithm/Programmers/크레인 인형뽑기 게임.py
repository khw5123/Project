def solution(board, moves):
    answer = 0
    stack = []
    for n in moves:
        for i in range(len(board)):
            if board[i][n-1] != 0:
                stack.append(board[i][n-1])
                board[i][n-1] = 0
                break
        if len(stack) > 1:
            if stack[-1] == stack[-2]:
                stack.pop()
                stack.pop()
                answer += 2
    return answer