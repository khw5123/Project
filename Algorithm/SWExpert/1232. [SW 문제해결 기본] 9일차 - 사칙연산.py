for t in range(10):
    n = int(input())
    li = ['']*(n+1)
    tmp = [[]]
    for _ in range(n):
        tmp.append(list(map(str, input().split())))
    for i in range(n, 0, -1):
        if tmp[i][1] in '+-*/':
            if tmp[i][1] == '+':
                li[i] = str(float(li[int(tmp[i][2])]) + float(li[int(tmp[i][3])]))
            elif tmp[i][1] == '-':
                li[i] = str(float(li[int(tmp[i][2])]) - float(li[int(tmp[i][3])]))
            elif tmp[i][1] == '*':
                li[i] = str(float(li[int(tmp[i][2])]) * float(li[int(tmp[i][3])]))
            elif tmp[i][1] == '/':
                li[i] = str(float(li[int(tmp[i][2])]) / float(li[int(tmp[i][3])]))
        else:
            li[i] = tmp[i][1]
    print('#' + str(t+1), li[1].split('.')[0])