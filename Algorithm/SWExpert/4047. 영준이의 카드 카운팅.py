for t in range(int(input())):
    card = [[], [], [], []]
    s = input()
    error = False
    for i in range(0, len(s), 3):
        if s[i] == 'S':
            if s[i+1:i+3] not in card[0]:
                card[0].append(s[i+1:i+3])
            else:
                error = True
                break
        elif s[i] == 'D':
            if s[i+1:i+3] not in card[1]:
                card[1].append(s[i+1:i+3])
            else:
                error = True
                break
        elif s[i] == 'H':
            if s[i+1:i+3] not in card[2]:
                card[2].append(s[i+1:i+3])
            else:
                error = True
                break
        else:
            if s[i+1:i+3] not in card[3]:
                card[3].append(s[i+1:i+3])
            else:
                error = True
                break
    print('#' + str(t+1), end=' ')
    if error:
        print('ERROR')
    else:
        for li in card:
            print(str(13 - len(li)), end=' ')
        print()