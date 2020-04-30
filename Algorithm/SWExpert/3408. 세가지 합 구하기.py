for t in range(int(input())):
    n = int(input())
    print('#' + str(t+1)+ ' ' + str((n*(1+n))//2) + ' ' + str((n*(1+n))//2*2-n) + ' ' + str((n*(1+n))//2*2))