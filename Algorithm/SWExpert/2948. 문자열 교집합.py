for t in range(int(input())):
    n, m = map(int, input().split())
    a = set(map(str, input().split()))
    b = set(map(str, input().split()))
    print('#' + str(t+1), str(len(a & b)))