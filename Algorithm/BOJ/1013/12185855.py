count = int(input(''))
for _ in range(count):
    tmp = input('')
    num = []
    confirm, sectionOne = True, False
    for i in range(len(tmp)):
        num.append(int(tmp[i]))
    save = num[:]
    remove = 0
    if len(num) == 1:
        print('NO')
        continue
    for i in range(len(num)):
        try:
            if num[i] == 0 and num[i - 1] == 0 and num[i - 2] == 1:
                sectionOne = True
                continue
            if sectionOne == True and num[i] == 0:
                del save[i - remove]
                remove += 1
            elif sectionOne == True and num[i] == 1:
                try:
                    if len(num) - 1 == i:
                        break
                    if (num[i + 1] == 0 and num[i + 2] == 1) or (num[i + 1] == 1 and num[i + 2] == 0 and num[i + 3] == 0):
                        sectionOne = False
                    else:
                        del save[i - remove]
                        remove += 1
                except:
                    del save[i - remove]
                    remove += 1
        except:
            continue
    if len(save) % 2 == 1:
        print('NO')
        continue
    jump = 0
    for i in range(len(save)):
        if jump == i:
            try:
                if save[i] == 0 and save[i + 1] == 1:
                    jump = i + 2
                elif save[i] == 1 and save[i + 1] == 0 and save[i + 2] == 0 and save[i + 3] == 1:
                    jump = i + 4
                else:
                    confirm = False
                    break
            except:
                confirm = False
                break
    if confirm == False:
        print('NO')
    elif confirm == True:
        print('YES')