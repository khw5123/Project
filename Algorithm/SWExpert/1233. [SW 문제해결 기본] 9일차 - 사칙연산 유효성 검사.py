for t in range(10):
    n = int(input())
    answer = 1
    li = [1]
    while li[-1] < n:
        li.append(li[-1]*2)
    li.pop()
    leaf = (li[-1] - (sum(li) - n)) + ((sum(li) - n) // 2)
    for i in range(n):
        tmp = list(map(str, input().split()))
        if i < n-leaf:
            if len(tmp) != 4 or tmp[1] not in '+-*/':
                answer = 0
        else:
            if len(tmp) != 2 or tmp[1] in '+-*/':
                answer = 0
    print('#' + str(t+1), str(answer))