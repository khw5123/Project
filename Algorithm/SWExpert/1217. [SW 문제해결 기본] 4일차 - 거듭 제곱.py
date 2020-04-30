for t in range(10):
    n = int(input())
    a, b = map(int, input().split())
    answer = pow(a, b)
    print('#' + str(n) + ' ' + str(answer))