for t in range(int(input())):
    d, a, b, f = map(int, input().split())
    answer = f * (d / (a + b))
    print('#' + str(t+1), str(answer))