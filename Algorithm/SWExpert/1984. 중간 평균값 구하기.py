for t in range(int(input())):
    n = list(map(int, input().split()))
    n.sort()
    print('#' + str(t+1) + ' ' + str(round(sum(n[1:len(n)-1]) / (len(n)-2))))