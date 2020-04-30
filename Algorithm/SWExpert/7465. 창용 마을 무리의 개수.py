def solve(n, cluster, li, answer):
    target = cluster[-1]
    for i in range(1, n+1):
        if li[target][i] == 1 and i not in cluster:
            cluster.append(i)
            solve(n, cluster, li, answer)
    return cluster

for t in range(int(input())):
    save, answer = [], 0
    n, m = map(int, input().split())
    li = [[0]*(n+1) for _ in range(n+1)]
    for _ in range(m):
        a, b = map(int, input().split())
        li[a][b], li[b][a] = 1, 1
    while len(save) != n:
        if len(save) == 0:
            save += solve(n, [1], li, save)
        else:
            save.sort()
            for i in range(1, n+1):
                if i not in save:
                    save += solve(n, [i], li, save)
                    break
        answer += 1
    print('#' + str(t+1), str(answer))