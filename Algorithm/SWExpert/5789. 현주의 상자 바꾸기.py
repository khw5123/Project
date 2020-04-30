for t in range(int(input())):
    n, q = map(int, input().split())
    answer = [0]*n
    for i in range(1, q+1):
        l, r = map(int, input().split())
        answer[l-1:r] = [i]*(r-l+1)
    print('#' + str(t+1), end=' ')
    for v in answer:
        print(v, end=' ')
    print()