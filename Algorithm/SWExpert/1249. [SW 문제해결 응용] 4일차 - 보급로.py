def solve():
    dp[0][0] = 0
    queue = [[0, 0]]
    while queue:
        x, y = queue[0][0], queue[0][1]
        del queue[0]
        for dx, dy in [[0, 1], [0, -1], [1, 0], [-1, 0]]:
            next_x, next_y = x+dx, y+dy
            if next_x >= 0 and next_x < n and next_y >= 0 and next_y < n:
                if dp[y][x] + li[next_y][next_x] < dp[next_y][next_x]:
                    dp[next_y][next_x] = dp[y][x] + li[next_y][next_x]
                    queue.append([next_x, next_y])

for t in range(int(input())):
    n = int(input())
    dp = [[987654321]*n for _ in range(n)]
    li = []
    for _ in range(n):
        li.append(list(map(int, input())))
    solve()
    print('#' + str(t+1), str(dp[n-1][n-1]))

'''
def solve(x, y, time):
    global answer
    if time >= answer:
        return
    if x == n-1 and y == n-1:
        answer = min(answer, time)
        return
    if x-1 >= 0 and time + li[y][x-1] < dp[y][x-1]:
        dp[y][x-1] = time + li[y][x-1]
        solve(x-1, y, time + li[y][x-1])
    if x+1 < n and time + li[y][x+1] < dp[y][x+1]:
        dp[y][x+1] = time + li[y][x+1]
        solve(x+1, y, time + li[y][x+1])
    if y-1 >= 0 and time + li[y-1][x] < dp[y-1][x]:
        dp[y-1][x] = time + li[y-1][x]
        solve(x, y-1, time + li[y-1][x])
    if y+1 < n and time + li[y+1][x] < dp[y+1][x]:
        dp[y+1][x] = time + li[y+1][x]
        solve(x, y+1, time+li[y+1][x])

for t in range(int(input())):
    n = int(input())
    answer = 987654321
    dp = [[987654321]*n for _ in range(n)]
    li = []
    for _ in range(n):
        li.append(list(map(int, input())))
    solve(0, 0, 0)
    print('#' + str(t+1), str(answer))
'''