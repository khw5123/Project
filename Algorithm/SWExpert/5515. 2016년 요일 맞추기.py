for t in range(int(input())):
    m, d = map(int, input().split())
    last = [0, 31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    total = sum(last[:m]) + d
    answer = (total % 7) - 4 if (total % 7) > 3 else (total % 7) + 3
    print('#' + str(t+1), str(answer))