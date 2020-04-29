for t in range(int(input())):
    n, x = map(int, input().split())
    li = [list(map(int, input().split())) for _ in range(n)]
    answer = 0
    case = []
    for i in range(n):
        case.append(li[i])
    for i in range(n):
        tmp = []
        for j in range(n):
            tmp.append(li[j][i])
        case.append(tmp)
    for road in case:
        confirm = True
        for i in range(len(road)-1):
            if abs(road[i] - road[i+1]) > 1:
                confirm = False
                break
        if confirm:
            possibility = True
            prev = road[0]
            extra = 0
            down = False
            first = True
            if road[0] == max(road):
                count = 20
            else:
                count = 1
            for i in range(1, len(road)):
                if prev == road[i]:
                    count += 1
                    if count > x:
                        extra = count - x
                elif prev < road[i]:
                    if down:
                        if extra < x:
                            possibility = False
                            break
                    else:
                        if count < x:
                            possibility = False
                            break
                    if road[i] == max(road):
                        count = 20
                    else:
                        count = 1
                    first = False
                    down = False
                    extra = 0
                else:
                    if not first:
                        if count < x:
                            possibility = False
                            break
                    if road[i] == max(road):
                        count = 20
                        extra = 20
                    else:
                        count = 1
                    first = False
                    down = True
                    extra = 0
                prev = road[i]
            if down and count < x:
                possibility = False
            if possibility:
                answer += 1
    print('#' + str(t+1), str(answer))