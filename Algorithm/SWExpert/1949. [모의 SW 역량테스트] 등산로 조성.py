def solve(path, i, j):
    global answer
    confirm = True
    if i-1 >= 0 and li[i][j] > li[i-1][j]:
        solve(path+[[i-1, j]], i-1, j)
        confirm = False
    if i+1 < n and li[i][j] > li[i+1][j]:
        solve(path+[[i+1, j]], i+1, j)
        confirm = False
    if j-1 >= 0 and li[i][j] > li[i][j-1]:
        solve(path+[[i, j-1]], i, j-1)
        confirm = False
    if j+1 < n and li[i][j] > li[i][j+1]:
        solve(path+[[i, j+1]], i, j+1)
        confirm = False
    if confirm:
        answer = max(answer, len(path))

for t in range(int(input())):
    n, k = map(int, input().split())
    li = [list(map(int, input().split())) for _ in range(n)]
    top, top_pos = 0, []
    for i in range(n):
        top = max(top, max(li[i]))
    for i in range(n):
        for j in range(n):
            if li[i][j] == top:
                top_pos.append([i, j])
    answer = 0
    for dig in range(k+1):
        for i in range(n):
            for j in range(n):
                li[i][j] -= dig
                for a in range(n):
                    for b in range(n):
                        if [a, b] in top_pos:
                            solve([[a, b]], a, b)
                li[i][j] += dig
    print('#' + str(t+1), str(answer))