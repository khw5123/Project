def solve(idx, probability):
    global li, visit, answer
    if probability <= answer:
        return
    if idx == len(li):
        answer = probability
        return
    for i in range(len(li[idx])):
        if visit[i] == False:
            visit[i] = True
            solve(idx+1, probability*li[idx][i])
            visit[i] = False

for t in range(int(input())):
    n = int(input())
    answer = 0.
    visit = [False]*n
    li = []
    for _ in range(n):
        li.append([])
        for v in list(map(int, input().split())):
            if v != 0:
                li[-1].append(v/100)
            else:
                li[-1].append(0.)
    solve(0, 1.)
    print('#%d %0.6f' % (t+1, round(answer*100, 6)))