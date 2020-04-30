for t in range(int(input())):
    n, a, b = map(int, input().split())
    answer = 987654321
    for r in range(1, n+1):
        for c in range(r, n+1):
            if n-(r*c) >= 0:
                formula = a*abs(r-c) + b*(n-(r*c))
                answer = min(answer, formula)
            else:
                break
    print('#' + str(t+1), str(answer))