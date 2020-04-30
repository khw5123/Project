for t in range(int(input())):
    n = int(input())
    score = list(map(int, input().split()))
    answer = [0]*10001
    answer[0] = 1
    sum_ = 0
    for i in range(n):
        sum_ += score[i]
        for j in range(sum_, -1, -1):
            if answer[j] == 1:
                answer[j + score[i]] = 1
    print('#' + str(t+1), str(sum(answer)))