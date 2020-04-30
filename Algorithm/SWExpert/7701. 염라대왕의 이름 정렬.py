for t in range(int(input())):
    n = int(input())
    li = []
    for i in range(n):
        li.append(input())
    li.sort(key=lambda x: (len(x), x))
    print('#' + str(t+1))
    for i in range(len(li)-1):
        if li[i] != li[i+1]:
            print(li[i])
    print(li[-1])