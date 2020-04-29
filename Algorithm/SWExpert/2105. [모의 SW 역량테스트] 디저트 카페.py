for t in range(int(input())):
    n = int(input())
    li = [list(map(int, input().split())) for _ in range(n)]
    answer = -1
    for i in range(n-2):
        for j in range(1, n-1):
            for a in range(1, 19):
                for b in range(1, 19):
                    path = []
                    confirm, half = True, False
                    a_count, b_count = 0, 0
                    pos_i, pos_j = i, j
                    while not half or a_count+b_count != a+b:
                        if a_count < a:
                            if not half: 
                                pos_i, pos_j = pos_i+1, pos_j-1
                                if pos_j >= 0 and pos_i < n:
                                    path.append(li[pos_i][pos_j])
                                else:
                                    confirm = False
                                    break
                            else:
                                pos_i, pos_j = pos_i-1, pos_j+1
                                if pos_j < n and pos_i >= 0:
                                    path.append(li[pos_i][pos_j])
                                else:
                                    confirm = False
                                    break
                            a_count += 1
                        else:
                            if b_count < b:
                                if not half:
                                    pos_i, pos_j = pos_i+1, pos_j+1
                                    if pos_j < n and pos_i < n:
                                        path.append(li[pos_i][pos_j])
                                    else:
                                        confirm = False
                                        break
                                else:
                                    pos_i, pos_j = pos_i-1, pos_j-1
                                    if pos_j >= 0 and pos_i >= 0:
                                        path.append(li[pos_i][pos_j])
                                    else:
                                        confirm = False
                                        break
                                b_count += 1
                            else:
                                half = True
                                a_count, b_count = 0, 0
                    if confirm:
                        if len(path) == len(set(path)):
                            answer = max(answer, len(path))
    print('#' + str(t+1), str(answer))