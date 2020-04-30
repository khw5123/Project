for t in range(int(input())):
    li = list()
    for _ in range(int(input())):
        li.append(list(map(int, input().split())))
    p = int(input())
    answer = [0]*p
    for i in range(p):
        j = int(input())
        for l in li:
            if j >= l[0] and j <= l[1]:
                answer[i] += 1
    print('#' + str(t+1), end=' ')
    for v in answer:
        print(v, end=' ')
    print()