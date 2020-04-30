def solve(idx, height):
    global answer
    if height >= b:
        answer = min(answer, height)
    if idx == n:
        return
    solve(idx+1, height+h[idx])
    solve(idx+1, height)

for t in range(int(input())):
    n, b = map(int, input().split())
    h = list(map(int, input().split()))
    answer = sum(h)
    solve(0, 0)
    print('#' + str(t+1), str(answer-b))