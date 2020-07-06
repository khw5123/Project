def solve(path, cost, board, dp, answer):
    if [path[-1][0], path[-1][1]] == [len(board[0])-1, len(board)-1]:
        answer[0] = min(answer[0], cost)
        return
    if cost >= answer[0]:
        return
    if dp[path[-1][1]][path[-1][0]] < cost:
        return
    dp[path[-1][1]][path[-1][0]] = cost
    if not (path[-1][0]+1 < 0 or path[-1][0]+1 >= len(board[0]) or path[-1][1] < 0 or path[-1][1] >= len(board)):
        if board[path[-1][1]][path[-1][0]+1] == 0 and [path[-1][0]+1, path[-1][1]] not in path:
            tmp_cost = 100
            if len(path) > 1:
                prev_x, prev_y = path[-2][0], path[-2][1]
                current_x, current_y = path[-1][0], path[-1][1]
                next_x, next_y = path[-1][0]+1, path[-1][1]
                if (prev_x == current_x and current_y == next_y) or (prev_y == current_y and current_x == next_x):
                    tmp_cost += 500
            solve(path+[[path[-1][0]+1, path[-1][1]]], cost+tmp_cost, board, dp, answer)
    if not (path[-1][0]-1 < 0 or path[-1][0]-1 >= len(board[0]) or path[-1][1] < 0 or path[-1][1] >= len(board)):
        if board[path[-1][1]][path[-1][0]-1] == 0 and [path[-1][0]-1, path[-1][1]] not in path:
            tmp_cost = 100
            if len(path) > 1:
                prev_x, prev_y = path[-2][0], path[-2][1]
                current_x, current_y = path[-1][0], path[-1][1]
                next_x, next_y = path[-1][0]-1, path[-1][1]
                if (prev_x == current_x and current_y == next_y) or (prev_y == current_y and current_x == next_x):
                    tmp_cost += 500
            solve(path+[[path[-1][0]-1, path[-1][1]]], cost+tmp_cost, board, dp, answer)
    if not (path[-1][0] < 0 or path[-1][0] >= len(board[0]) or path[-1][1]+1 < 0 or path[-1][1]+1 >= len(board)):
        if board[path[-1][1]+1][path[-1][0]] == 0 and [path[-1][0], path[-1][1]+1] not in path:
            tmp_cost = 100
            if len(path) > 1:
                prev_x, prev_y = path[-2][0], path[-2][1]
                current_x, current_y = path[-1][0], path[-1][1]
                next_x, next_y = path[-1][0], path[-1][1]+1
                if (prev_x == current_x and current_y == next_y) or (prev_y == current_y and current_x == next_x):
                    tmp_cost += 500
            solve(path+[[path[-1][0], path[-1][1]+1]], cost+tmp_cost, board, dp, answer)
    if not (path[-1][0] < 0 or path[-1][0] >= len(board[0]) or path[-1][1]-1 < 0 or path[-1][1]-1 >= len(board)):
        if board[path[-1][1]-1][path[-1][0]] == 0 and [path[-1][0], path[-1][1]-1] not in path:
            tmp_cost = 100
            if len(path) > 1:
                prev_x, prev_y = path[-2][0], path[-2][1]
                current_x, current_y = path[-1][0], path[-1][1]
                next_x, next_y = path[-1][0], path[-1][1]-1
                if (prev_x == current_x and current_y == next_y) or (prev_y == current_y and current_x == next_x):
                    tmp_cost += 500
            solve(path+[[path[-1][0], path[-1][1]-1]], cost+tmp_cost, board, dp, answer)

def solution(board):
    answer = [987654321]
    dp = [[987654321]*len(board[0]) for _ in range(len(board))]
    solve([[0, 0]], 0, board, dp, answer)
    return answer[0]