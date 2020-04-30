for t in range(int(input())):
    n = int(input())
    arr = list(map(int, input().split()))
    print('#' + str(t+1), end=' ')
    for v in sorted(arr):
        print(v, end=' ')
    print()