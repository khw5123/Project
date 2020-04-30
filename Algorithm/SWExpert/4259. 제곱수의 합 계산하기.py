for t in range(int(input())):
    n = int(input())
    num = list(map(str, input().split()))
    answer = 0
    for i in range(len(num)):
        answer += pow(int(num[i][:len(num[i])-1]), int(num[i][-1]))
    print('#' + str(t+1), str(answer))