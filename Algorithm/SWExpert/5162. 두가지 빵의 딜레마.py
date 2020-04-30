for t in range(int(input())):
    a, b, c = map(int, input().split())
    a, b = (b, a) if a > b else (a, b)
    m, answer = 0, 0
    while True:
        if m + a <= c:
            m += a
            answer += 1
        else:
            break
    print('#' + str(t+1), str(answer))