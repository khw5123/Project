def solve(y, x, time):
    if time == l:
        answer.add((y, x))
        return
    if time in dp[y][x]:
        return
    dp[y][x].append(time)
    if li[y][x] == 1:
        if y-1 >= 0 and (li[y-1][x] == 1 or li[y-1][x] == 2 or li[y-1][x] == 5 or li[y-1][x] == 6):
            solve(y-1, x, time+1)
        if y+1 < n and (li[y+1][x] == 1 or li[y+1][x] == 2 or li[y+1][x] == 4 or li[y+1][x] == 7):
            solve(y+1, x, time+1)
        if x-1 >= 0 and (li[y][x-1] == 1 or li[y][x-1] == 3 or li[y][x-1] == 4 or li[y][x-1] == 5):
            solve(y, x-1, time+1)
        if x+1 < m and (li[y][x+1] == 1 or li[y][x+1] == 3 or li[y][x+1] == 6 or li[y][x+1] == 7):
            solve(y, x+1, time+1)
    elif li[y][x] == 2:
        if y-1 >= 0 and (li[y-1][x] == 1 or li[y-1][x] == 2 or li[y-1][x] == 5 or li[y-1][x] == 6):
            solve(y-1, x, time+1)
        if y+1 < n and (li[y+1][x] == 1 or li[y+1][x] == 2 or li[y+1][x] == 4 or li[y+1][x] == 7):
            solve(y+1, x, time+1)
    elif li[y][x] == 3:
        if x-1 >= 0 and (li[y][x-1] == 1 or li[y][x-1] == 3 or li[y][x-1] == 4 or li[y][x-1] == 5):
            solve(y, x-1, time+1)
        if x+1 < m and (li[y][x+1] == 1 or li[y][x+1] == 3 or li[y][x+1] == 6 or li[y][x+1] == 7):
            solve(y, x+1, time+1)
    elif li[y][x] == 4:
        if y-1 >= 0 and (li[y-1][x] == 1 or li[y-1][x] == 2 or li[y-1][x] == 5 or li[y-1][x] == 6):
            solve(y-1, x, time+1)
        if x+1 < m and (li[y][x+1] == 1 or li[y][x+1] == 3 or li[y][x+1] == 6 or li[y][x+1] == 7):
            solve(y, x+1, time+1)
    elif li[y][x] == 5:
        if y+1 < n and (li[y+1][x] == 1 or li[y+1][x] == 2 or li[y+1][x] == 4 or li[y+1][x] == 7):
            solve(y+1, x, time+1)
        if x+1 < m and (li[y][x+1] == 1 or li[y][x+1] == 3 or li[y][x+1] == 6 or li[y][x+1] == 7):
            solve(y, x+1, time+1)
    elif li[y][x] == 6:
        if y+1 < n and (li[y+1][x] == 1 or li[y+1][x] == 2 or li[y+1][x] == 4 or li[y+1][x] == 7):
            solve(y+1, x, time+1)
        if x-1 >= 0 and (li[y][x-1] == 1 or li[y][x-1] == 3 or li[y][x-1] == 4 or li[y][x-1] == 5):
            solve(y, x-1, time+1)
    elif li[y][x] == 7:
        if y-1 >= 0 and (li[y-1][x] == 1 or li[y-1][x] == 2 or li[y-1][x] == 5 or li[y-1][x] == 6):
            solve(y-1, x, time+1)
        if x-1 >= 0 and (li[y][x-1] == 1 or li[y][x-1] == 3 or li[y][x-1] == 4 or li[y][x-1] == 5):
            solve(y, x-1, time+1)
    solve(y, x, time+1)

for t in range(int(input())):
    n, m, r, c, l = map(int, input().split())
    li = [list(map(int, input().split())) for _ in range(n)]
    dp = [[[] for _ in range(m)] for _ in range(n)]
    answer = set()
    solve(r, c, 1)
    print('#' + str(t+1), str(len(answer)))