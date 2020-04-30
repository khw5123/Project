rule = {'0001101':0, '0011001':1, '0010011':2, '0111101':3, '0100011':4, '0110001':5, '0101111':6, '0111011':7, '0110111':8, '0001011':9}

for t in range(int(input())):
    n, m = map(int, input().split())
    code = []
    answer = 0
    for _ in range(n):
        tmp = list(map(str, input()))
        if sum(list(map(int, tmp))) != 0:
            tmp.reverse()
            save = []
            for i in range(tmp.index('1'), len(tmp), 7):
                tmp2 = tmp[i:i+7]
                tmp2.reverse()
                if ''.join(tmp2) in rule:
                    save.insert(0, rule[''.join(tmp2)])
            if len(save) != 0:
                code.append(save)
    confirm = True
    if len(code) >= 5:
        for i in range(1, len(code)):
            if code[i-1] != code[i] or len(code[i]) != 8:
                confirm = False
                break
    else:
        confirm = False
    if confirm:
        if ((code[0][0] + code[0][2] + code[0][4] + code[0][6])*3 + (code[0][1] + code[0][3] + code[0][5]) + code[0][7]) % 10 == 0:
            answer = sum(code[0])
    print('#' + str(t+1), str(answer))