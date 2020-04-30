for t in range(int(input())):
    string = input()
    answer = list()
    tmp = ''
    for i in range(len(string) // 2):
        tmp += string[i]
        if tmp == string[i+1:i+1+len(tmp)]:
            if len(answer) == 0 or (len(answer) != 0 and len(tmp) % len(answer[-1]) != 0):
                answer.append(tmp)
    if len(answer) != 0:
        print('#' + str(t+1) + ' ' + str(len(answer[-1])))
    else:
        print('#' + str(t+1) + ' 0')