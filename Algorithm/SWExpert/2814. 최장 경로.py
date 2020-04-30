def solve(start, depth, visit, n, li, answer):
    if depth > n:
        return
    answer[0] = max(answer[0], depth)
    for i in range(1, n+1):
        if i not in visit and li[start][i] == 1:
            visit.append(i)
            solve(i, depth+1, visit, n, li, answer)
            visit.pop()

for t in range(int(input())):
    n, m = map(int, input().split())
    li = [[0]*(n+1) for _ in range(n+1)]
    answer = [0]
    for _ in range(m):
        a, b = map(int, input().split())
        li[a][b], li[b][a] = 1, 1
    for start in range(1, n+1):
        solve(start, 1, [start], n, li, answer)
    print('#' + str(t+1), str(answer[0]))