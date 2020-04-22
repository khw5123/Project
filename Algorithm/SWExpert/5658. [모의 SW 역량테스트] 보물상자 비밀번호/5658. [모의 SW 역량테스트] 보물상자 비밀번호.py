for t in range(int(input())):
    n, k = map(int, input().split())
    pw = input()
    tmp, answer = [pw], []
    for i in range(1, len(pw)):
        tmp.append(pw[-i:] + pw[:len(pw)-i])
    for i in range(len(tmp)):
        for j in range(0, len(tmp[i]), len(tmp[i])//4):
            if tmp[i][j:j+(len(tmp[i])//4)] not in answer:
                answer.append(tmp[i][j:j+(len(tmp[i])//4)])
    answer.sort(reverse=True)
    print('#' + str(t+1), int(answer[k-1], 16))