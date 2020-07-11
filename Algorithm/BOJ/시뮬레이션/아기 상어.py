n = int(input())
li = [list(map(int, input().split())) for _ in range(n)]
shark, answer = [-1, -1, 2, 0], 0
for i in range(n):
    for j in range(n):
        if li[i][j] == 9:
            shark[0], shark[1], li[i][j] = i, j, 0
while True:
    target = [-1, -1, 401]
    queue, visit = [[shark[0], shark[1], 0]], [[0]*n for _ in range(n)]
    while queue:
        y, x, time = queue[0][0], queue[0][1], queue[0][2]
        del queue[0]
        if li[y][x] != 0 and li[y][x] < shark[2]:
            if time < target[2]:
                target = [y, x, time]
            elif time == target[2]:
                if y < target[0]:
                    target = [y, x, time]
                elif y == target[0]:
                    if x < target[1]:
                        target = [y, x, time]
        if not visit[y][x]:
            visit[y][x] = 1
            for ny, nx in [[y+1, x], [y-1, x], [y, x+1], [y, x-1]]:
                if 0 <= ny < n and 0 <= nx < n:
                    if li[ny][nx] <= shark[2]:
                        queue.append([ny, nx, time+1])
    if target[0] == -1:
        break
    li[target[0]][target[1]] = 0
    shark[0], shark[1], shark[3] = target[0], target[1], shark[3]+1
    if shark[2] == shark[3]:
        shark[2], shark[3] = shark[2]+1, 0
    answer += target[2]
print(answer)