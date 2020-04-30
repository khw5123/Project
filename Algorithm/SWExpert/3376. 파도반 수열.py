for t in range(int(input())):
    n = int(input())
    li = [1,1,1,2]
    if n > len(li):
        for i in range(n-len(li)):
            li.append(li[-2] + li[-3])
    print('#' + str(t+1), str(li[n-1]))