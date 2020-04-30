import copy

for t in range(int(input())):
    n = int(input())
    li = list(map(int, input().split()))
    answer = copy.deepcopy(li)
    for i in range(1, n):
        if li[i] < 0:
            if answer[i-1] + li[i] > 0:
                answer[i] = answer[i-1] + li[i]
            else:
                answer[i] = 0
        else:
            answer[i] = answer[i-1] + li[i]
    if max(answer) == 0:
        print('#' + str(t+1), str(max(li)))
    else:
        print('#' + str(t+1), str(max(answer)))