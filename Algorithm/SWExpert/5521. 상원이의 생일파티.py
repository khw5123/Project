for t in range(int(input())):
    n, m = map(int, input().split())
    li = [[0]*(n+1) for _ in range(n+1)]
    answer, queue = [], []
    for _ in range(m):
        a, b = map(int, input().split())
        li[a][b], li[b][a] = 1, 1
    for i in range(n+1):
        if li[1][i] == 1:
            queue.append(i)
            answer.append(i)
    for i in queue:
        for j in range(n+1):
            if li[i][j] == 1 and j != 1 and j not in answer:
                answer.append(j)
    print('#' + str(t+1), len(answer))