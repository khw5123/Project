def solve(node):
    global answer
    if answer:
        return
    if node == 99:
        answer = 1
        return
    for i in range(len(li[node])):
        if li[node][i] == 1:
            solve(i)

for _ in range(10):
    t, n = map(int, input().split())
    tmp = list(map(int, input().split()))
    answer = 0
    li = [[0]*(100) for _ in range(100)]
    for i in range(0, len(tmp), 2):
        li[tmp[i]][tmp[i+1]] = 1
    solve(0)
    print('#' + str(t), str(answer))