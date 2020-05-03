import copy

rate = {'1123':0, '1222':1, '2212':2, '1141':3, '2311':4, '1321':5, '4111':6, '2131':7, '3121':8, '2113':9}

def hex_to_bin(num):
    if len(bin(int(num, 16))[2:]) == 4:
        return bin(int(num, 16))[2:]
    else:
        return '0'*(4-len(bin(int(num, 16))[2:])) + bin(int(num, 16))[2:]

def solve(s):
    code = []
    length, width = 56, 1
    while True:
        if len(s) >= length*width:
            for i in range(len(s)-length*width+1):
                target = s[i:i+length*width]
                result, arr = [], []
                for j in range(0, len(target), width*7):
                    arr.append(target[j:j+width*7])
                for num in arr:
                    if num[0] != '1':
                        break
                    sub, confirm = [], True
                    for j in range(0, len(num), width):
                        n = num[j:j+width]
                        if width > 1:
                            for k in range(len(n)-1):
                                if n[k] != n[k+1]:
                                    confirm = False
                                    break
                        if not confirm:
                            break
                        sub.append(n[0])
                    if len(sub) == 7:
                        r, one, zero = '', 0, 0
                        for j in range(len(sub)):
                            if sub[j] == '1':
                                if zero != 0:
                                    r += str(zero)
                                    zero = 0
                                one += 1
                            else:
                                if one != 0:
                                    r += str(one)
                                    one = 0
                                zero += 1
                        if zero == 0:
                            r += str(one)
                        elif one == 0:
                            r += str(zero)
                        if r in rate:
                            result.append(rate[r])
                        else:
                            break
                    else:
                        break
                if len(result) == 8:
                    code.append(copy.deepcopy(result))
        else:
            break
        width += 1
    return code

for t in range(int(input())):
    n, m = map(int, input().split())
    answer = 0
    check, prev = [], ''
    for _ in range(n):
        line = input()[:m]
        if line != prev:
            if len(set(list(line))) != 1:
                s = ''
                for v in line:
                    s += hex_to_bin(v)
                s = s[::-1]
                s = s[s.find('1'):]
                for code in solve(s):
                    code.reverse()
                    if code in check:
                        continue
                    check.append(code)
                    if ((code[0]+code[2]+code[4]+code[6])*3 + code[1] + code[3] + code[5] + code[7]) % 10 == 0:
                        answer += sum(code)
        prev = line
    print('#' + str(t+1), str(answer))