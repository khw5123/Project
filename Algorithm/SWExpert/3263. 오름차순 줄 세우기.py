for t in range(int(input())):
    n = int(input())
    save = [0]*(n+1)
    li = list(map(int, input().split()))
    for i in range(len(li)):
        save[li[i]] = save[li[i]-1]+1
    answer = n-max(save)
    print('#' + str(t+1), str(answer))