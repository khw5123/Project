def solve(idx):
    global answer
    if idx > n:
        return
    solve(idx*2)
    answer += li[idx]
    solve(idx*2+1)

for t in range(10):
    n = int(input())
    answer = ''
    li = ['']*(n+1)
    for i in range(1, n+1):
        tmp = list(map(str, input().split()))
        li[i] = tmp[1]
    solve(1)
    print('#' + str(t+1), answer)