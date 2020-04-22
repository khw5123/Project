count = int(input(''))
for _ in range(count):
    width, height, num = map(int, input().split())
    save = []
    for _ in range(num):
        x, y = map(int, input().split())
        save.append([x, y])
    result = 0
    index = 0
    saveIndex = set()
    while True:
        # print(save)
        # print(index)
        # print(save[index])
        for i in range(len(save)):
            if (save[index][0] == save[i][0] and abs(save[index][1] - save[i][1]) == 1) or (save[index][1] == save[i][1] and abs(save[index][0] - save[i][0]) == 1):
                saveIndex.add((save[i][0], save[i][1]))
        # print(saveIndex)
        del save[index]
        try:
            indexVar = saveIndex.pop()
            for i in range(len(save)):
                if save[i][0] == indexVar[0] and save[i][1] == indexVar[1]:
                    index = i
                    break
        except:
            index = 0
            result += 1
        if len(save) == 0:
            break
    print(result)