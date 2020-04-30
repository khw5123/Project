for t in range(int(input())):
    n = int(input())
    m = [50000, 10000, 5000, 1000, 500, 100, 50, 10]
    answer = [0] * 8
    for i in range(len(m)):
        answer[i] = n // m[i]
        n -= (m[i] * answer[i])
    print('#' + str(t+1))
    for v in answer:
        print(v, end=' ')
    print()