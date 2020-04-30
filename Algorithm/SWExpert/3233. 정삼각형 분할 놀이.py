for t in range(int(input())):
    a, b = map(int, input().split())
    answer = 0
    for i in range(a//b):
        answer += (i*2 + 1)
    print('#' + str(t+1), str(answer))