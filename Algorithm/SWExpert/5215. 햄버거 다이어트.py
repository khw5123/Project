def solve(idx, score, kcal, answer, l, li):
    if kcal > l:
        return
    if idx == len(li):
        answer[0] = max(answer[0], score)
        return
    solve(idx+1, score+li[idx][0], kcal+li[idx][1], answer, l , li)
    solve(idx+1, score, kcal, answer, l, li)

for t in range(int(input())):
    n, l = map(int, input().split())
    li, answer = [], [0]
    for _ in range(n):
        li.append(list(map(int, input().split())))
    solve(0, 0, 0, answer, l, li)
    print('#' + str(t+1), str(answer[0]))