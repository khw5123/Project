def tenary_to_decimal(t):
    result = 0
    for i in range(len(t)):
        result += int(t[-(i+1)])*pow(3, i)
    return result

for a in range(int(input())):
    binary = input()
    tenary = input()
    li_b = []
    li_t = []
    answer = 0
    for i in range(len(binary)):
        if binary[i] == '0':
            li_b.append(binary[:i] + '1' + binary[i+1:])
        else:
            li_b.append(binary[:i] + '0' + binary[i+1:])
    for i in range(len(tenary)):
        if tenary[i] == '0':
            li_t.append(tenary[:i] + '1' + tenary[i+1:])
            li_t.append(tenary[:i] + '2' + tenary[i+1:])
        elif tenary[i] == '1':
            li_t.append(tenary[:i] + '0' + tenary[i+1:])
            li_t.append(tenary[:i] + '2' + tenary[i+1:])
        else:
            li_t.append(tenary[:i] + '0' + tenary[i+1:])
            li_t.append(tenary[:i] + '1' + tenary[i+1:])
    for b in li_b:
        exit_ = False
        for t in li_t:
            if int(b, 2) == tenary_to_decimal(t):
                answer = int(b, 2)
                exit_ = True
                break
        if exit_:
            break
    print('#' + str(a+1), str(answer))