def solve(start, end):
    result = 0
    queue = [start]
    visit = []
    while queue:
        x, y = queue[0][0], queue[0][1]
        del queue[0]
        if [x, y] == end:
            result = 1
            break
        if [x, y] not in visit:
            visit.append([x, y])
            for dx, dy in [[0, 1], [0, -1], [1, 0], [-1, 0]]:
                next_x, next_y = x+dx, y+dy
                if next_x >= 0 and next_x < n and next_y >= 0 and next_y < n:
                    if li[next_y][next_x] != 1:
                        if [next_x, next_y] not in queue:
                            queue.append([next_x, next_y])
    return result

for _ in range(10):
    t = int(input())
    n = 16
    li = [list(map(int, input())) for _ in range(n)]
    start, end = [], []
    for i in range(n):
        for j in range(n):
            if li[i][j] == 2:
                start = [j, i]
            elif li[i][j] == 3:
                end = [j, i]
    answer = solve(start, end)
    print('#' + str(t), str(answer))