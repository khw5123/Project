for t in range(int(input())):
    arr = []
    length = 0
    for _ in range(5):
        arr.append(list(input().split()))
        length = max(length, len(arr[-1][0]))
    print('#' + str(t+1), end=' ')
    for i in range(length):
        for j in range(5):
            try:
                print(arr[j][0][i], end='')
            except:
                pass
    print()