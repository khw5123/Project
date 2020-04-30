for t in range(int(input())):
    n = list(map(int, input().split()))
    n.sort()
    if n.count(n[0]) == 3 or n.count(n[0]) == 1:
        print('#' + str(t+1), str(n[0]))
    else:
        print('#' + str(t+1), str(n[-1]))