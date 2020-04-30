for t in range(int(input())):
    s = input()
    h = int(input())
    pos = list(map(int, input().split()))
    for i in range(h):
        s = s[:pos[i]] + '-' + s[pos[i]:]
        for j in range(i+1, h):
            if pos[i] <= pos[j]:
                pos[j] += 1
    print('#' + str(t+1), s)