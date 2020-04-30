for t in range(int(input())):
    n = int(input())
    li, answer = [], []
    for _ in range(n):
        li.append(int(input()))
    del li[0]
    while len(li) != 0:
        period = li[0]-1
        answer.append(period)
        for i in range(1, li[-1]+1, period):
            if i in li:
                del li[li.index(i)]
    print('#' + str(t+1), str(len(answer)))