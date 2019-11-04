height, width = map(int, input().split())
arr = []
result = 2500
for i in range(height):
    arr.append([])
    color = input()
    for j in range(width):
        arr[i].append(color[j])
for i in range(height - 7):
    for j in range(width - 7):
        typeW, typeB = 0, 0
        for a in range(8):
            for b in range(8):
                if (a % 2 == 0 and b % 2 == 0) or (a % 2 == 1 and b % 2 == 1):
                    if arr[i + a][j + b] == 'B':
                        typeW += 1
                    elif arr[i + a][j + b] == 'W':
                        typeB += 1
                if (a % 2 == 0 and b % 2 == 1) or (a % 2 == 1 and b % 2 == 0):
                    if arr[i + a][j + b] == 'B':
                        typeB += 1
                    elif arr[i + a][j + b] == 'W':
                        typeW += 1
        tmp = typeW if typeW < typeB else typeB
        result = result if result < tmp else tmp
print(result)