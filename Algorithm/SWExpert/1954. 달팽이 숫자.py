for t in range(int(input())):
    n = int(input())
    arr = [[0]*n for _ in range(n)]
    direction, count = 0, 0
    x, y = 0, 0
    while True:
        if direction % 4 == 0:
            for i in range(x, n):
                if arr[y][i] != 0:
                    break
                count += 1
                x = i
                arr[y][x] = count
            y += 1
        elif direction % 4 == 1:
            for i in range(y, n):
                if arr[i][x] != 0:
                    break
                count += 1
                y = i
                arr[y][x] = count
            x -= 1
        elif direction % 4 == 2:
            for i in range(x, -1, -1):
                if arr[y][i] != 0:
                    break
                count += 1
                x = i
                arr[y][x] = count
            y -= 1
        else:
            for i in range(y, -1, -1):
                if arr[i][x] != 0:
                    break
                count += 1
                y = i
                arr[y][x] = count
            x += 1
        direction += 1
        confirm = True
        for i in range(n):
            for j in range(n):
                if arr[i][j] == 0:
                    confirm = False
        if confirm:
            break
    print('#' + str(t+1))
    for i in range(n):
        for j in range(n):
            print(arr[i][j], end=' ')
        print()