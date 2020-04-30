for t in range(int(input())):
    n, m = map(int, input().split())
    a = list(map(int, input().split()))
    b = list(map(int, input().split()))
    save, answer = [], [0, 0]
    for i in range(len(b)):
        for j in range(len(a)):
            if b[i] >= a[j]:
                save.append(j+1)
                break
    for i in range(len(save)):
        if answer[1] < save.count(save[i]):
            answer[0], answer[1] = save[i], save.count(save[i])
    print('#' + str(t+1), str(answer[0]))