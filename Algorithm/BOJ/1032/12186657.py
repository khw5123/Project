count = int(input(''))
save, result = [], []
for _ in range(count):
    file = input('')
    save.append(file)
for i in range(len(save[0])):
    result.append('')
for j in range(len(save[0])):
    for i in range(count - 1):
        if save[i][j] != save[i + 1][j]:
            result[j] = '?'
            break
    if result[j] == '':
        result[j] = save[0][j]
for c in result:
    print(c, end='')