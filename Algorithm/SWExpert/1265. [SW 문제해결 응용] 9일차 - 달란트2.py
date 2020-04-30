for t in range(int(input())):
    n, p = map(int, input().split())
    li = [0]*p
    answer = 1
    idx = 0
    while sum(li) != n:
        li[idx] += 1
        idx += 1
        if idx == len(li):
            idx = 0
    for v in li:
        answer *= v
    print('#' + str(t+1), answer)