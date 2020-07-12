import copy
from itertools import combinations

n, m = map(int, input().split())
li = [list(map(int, input().split())) for _ in range(n)]
virus, space = {}, []
answer = 0
for i in range(n):
    for j in range(m):
        if li[i][j] == 0:
            space.append([i, j])
        elif li[i][j] == 2:
            virus[(i, j)] = 1
for wall in combinations(space, 3):
    save = copy.deepcopy(li)
    for i, j in wall:
        li[i][j] = 1
    for k, v in virus.items():
        queue, visit = [[k[0], k[1]]], [[0]*m for _ in range(n)]
        while queue:
            y, x = queue[0][0], queue[0][1]
            del queue[0]
            li[y][x] = 2
            if not visit[y][x]:
                visit[y][x] = 1
                for ny, nx in [[y+1, x], [y-1, x], [y, x+1], [y, x-1]]:
                    if 0 <= ny < n and 0 <= nx < m:
                        if li[ny][nx] != 1:
                            queue.append([ny, nx])
    count = 0
    for i in range(n):
        for j in range(m):
            if li[i][j] == 0:
                count += 1
    answer = max(answer, count)
    li = save
print(answer)