for t in range(int(input())):
    l, u, x = map(int, input().split())
    answer = 0
    if x >= l and x <= u:
        answer = 0
    elif x > u:
        answer = -1
    else:
        answer = l - x
    print('#' + str(t+1), str(answer))