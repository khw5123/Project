def solve(start, n, m, edge, answer, case):
    if len(case) == 3:
        if edge[case[0]][case[2]] == 1:
            answer[0] += 1
        return
    for i in range(1, n+1):
        if edge[start][i] == 1 and i not in case:
            case.append(i)
            solve(i, n, m, edge, answer, case)
            case.pop()

for t in range(int(input())):
    n, m = map(int, input().split())
    edge = [[0]*(n+1) for _ in range(n+1)]
    answer = [0]
    for _ in range(m):
        x, y = map(int, input().split())
        edge[x][y], edge[y][x] = 1, 1
    for i in range(1, n+1):
        solve(i, n, m, edge, answer, [i])
    print('#' + str(t+1), str(answer[0]//6))