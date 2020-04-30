for t in range(int(input())):
    n = int(input())
    answer = 0.
    for _ in range(n):
        p, x = map(float, input().split())
        answer += p*x
    print('#' + str(t+1) + ' ' + str(answer))