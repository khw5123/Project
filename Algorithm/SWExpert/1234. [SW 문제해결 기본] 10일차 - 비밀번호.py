for t in range(10):
    c, n = map(int, input().split())
    while True:
        prev = len(str(n))
        for i in range(1, len(str(n))):
            if str(n)[i-1] == str(n)[i]:
                if i == 1:
                    n = int(str(n)[i+1:])
                    break
                elif i == len(str(n))-1:
                    n = int(str(n)[:i-1])
                    break
                else:
                    n = int(str(n)[:i-1] + str(n)[i+1:])
                    break
        if prev == len(str(n)):
            break
    print('#' + str(t+1), str(n))