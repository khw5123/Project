def solve(path, cost, direction):
    global answer
    if path[1] == n-1:
        if li[path[1]][path[0]] == 2:
            answer = True
        return
    if direction == 'r':
        if li[path[1]+1][path[0]] == 1:
            direction = 'd'
            solve([path[0], path[1]+1], cost+li[path[1]+1][path[0]], direction)
        else:
            solve([path[0]+1, path[1]], cost+li[path[1]][path[0]+1], direction)
    elif direction == 'l':
        if li[path[1]+1][path[0]] == 1:
            direction = 'd'
            solve([path[0], path[1]+1], cost+li[path[1]+1][path[0]], direction)
        else:
            solve([path[0]-1, path[1]], cost+li[path[1]][path[0]-1], direction)
    elif path[0]+1 >= 0 and path[0]+1 < n and li[path[1]][path[0]+1] == 1 and direction == 'd':
        direction = 'r'
        solve([path[0]+1, path[1]], cost+li[path[1]][path[0]+1], direction)
    elif path[0]-1 >= 0 and path[0]-1 < n and li[path[1]][path[0]-1] == 1 and direction == 'd':
        direction = 'l'
        solve([path[0]-1, path[1]], cost+li[path[1]][path[0]-1], direction)
    else:
        solve([path[0], path[1]+1], cost+li[path[1]+1][path[0]], direction)

for _ in range(10):
    t = int(input())
    answer = False
    n = 100
    li = [list(map(int, input().split())) for _ in range(n)]
    for i in range(n):
        if li[0][i] == 1:
            solve([i, 0], li[0][i], 'd')
            if answer:
                answer = i
                break
    print('#' + str(t), str(answer))