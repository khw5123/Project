def solve(prev_x, prev_y, x, y, count):
    global answer, end_x, end_y
    if x == end_x and y == end_y:
        answer = min(answer, count)
        return
    if x < 0 or x >= n or y < 0 or y >= n:
        return
    if visit[y][x] == 1:
        return
    visit[y][x] = 1
    if prev_x == x and prev_y == y-1:
        if count < depth[y][x][0]:
            depth[y][x][0] = count
            if li[y][x] == 1 or li[y][x] == 2:
                solve(x, y, x, y+1, count+1)
            elif li[y][x] == 3 or li[y][x] == 4 or li[y][x] == 5 or li[y][x] == 6:
                solve(x, y, x-1, y, count+1)
                solve(x, y, x+1, y, count+1)
    elif prev_x == x and prev_y == y+1:
        if count < depth[y][x][1]:
            depth[y][x][1] = count
            if li[y][x] == 1 or li[y][x] == 2:
                solve(x, y, x, y-1, count+1)
            elif li[y][x] == 3 or li[y][x] == 4 or li[y][x] == 5 or li[y][x] == 6:
                solve(x, y, x+1, y, count+1)
                solve(x, y, x-1, y, count+1)
    elif prev_x == x-1 and prev_y == y:
        if count < depth[y][x][2]:
            depth[y][x][2] = count
            if li[y][x] == 1 or li[y][x] == 2:
                solve(x, y, x+1, y, count+1)
            elif li[y][x] == 3 or li[y][x] == 4 or li[y][x] == 5 or li[y][x] == 6:
                solve(x, y, x, y+1, count+1)
                solve(x, y, x, y-1, count+1)
    elif prev_x == x+1 and prev_y == y:
        if count < depth[y][x][3]:
            depth[y][x][3] = count
            if li[y][x] == 1 or li[y][x] == 2:
                solve(x, y, x-1, y, count+1)
            elif li[y][x] == 3 or li[y][x] == 4 or li[y][x] == 5 or li[y][x] == 6:
                solve(x, y, x, y+1, count+1)
                solve(x, y, x, y-1, count+1)
    visit[y][x] = 0

for t in range(int(input())):
    n = int(input())
    li = [list(map(int, input().split())) for _ in range(n)]
    answer = n*n
    for i in range(2):
        depth = [[[n*n]*4 for _ in range(n)] for _ in range(n)]
        visit = [[0]*n for _ in range(n)]
        if i == 0:
            end_x, end_y = n, n-1
            solve(-1, 0, 0, 0, 0)
        else:
            end_x, end_y = -1, 0
            solve(n, n-1, n-1, n-1, 0)
    print('#' + str(t+1), str(answer))