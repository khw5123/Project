for t in range(int(input())):
    score = list(map(int, input().split()))
    for i in range(len(score)):
        if score[i] < 40:
            score[i] = 40
    print('#' + str(t+1), str(int(sum(score)/len(score))))