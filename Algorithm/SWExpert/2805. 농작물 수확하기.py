for t in range(int(input())):
    n = int(input())
    li = []
    answer = 0
    for i in range(n):
        li.append(list(map(int, input())))
    for i in range(n//2):
        answer += sum(li[i][(n//2)-i:((n//2)-i)+((i*2)+1)])
        answer += sum(li[n-i-1][(n//2)-i:((n//2)-i)+((i*2)+1)])
    answer += sum(li[n//2][:])
    print('#' + str(t+1), str(answer))