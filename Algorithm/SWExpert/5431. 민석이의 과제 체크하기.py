for t in range(int(input())):
    n, k = map(int, input().split())
    answer = list(map(int, input().split()))
    print('#' + str(t+1), end=' ')
    for i in range(1, n+1):
        if i not in answer:
            print(i, end=' ')
    print()