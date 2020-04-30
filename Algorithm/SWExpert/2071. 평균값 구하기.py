for i in range(int(input())):
    n = list(map(int, input().split()))
    avg = round(sum(n) / len(n))
    print('#' + str(i+1) + ' ' + str(avg))