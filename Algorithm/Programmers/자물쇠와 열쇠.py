import copy

def rotate_90(key):
    N = len(key)
    ret = [[0] * N for _ in range(N)]
    for r in range(N):
        for c in range(N):
            ret[c][N-1-r] = key[r][c]
    return ret

def rotate_180(key):
    N = len(key)
    ret = [[0] * N for _ in range(N)]
    for r in range(N):
        for c in range(N):
            ret[N-1-r][N-1-c] = key[r][c]
    return ret

def rotate_270(key):
    N = len(key)
    ret = [[0] * N for _ in range(N)]
    for r in range(N):
        for c in range(N):
            ret[N-1-c][r] = key[r][c]
    return ret

def solution(key, lock):
    save = copy.deepcopy(key)
    for r in range(0, 4):
        if r == 1:
            key = copy.deepcopy(rotate_90(key))
        elif r == 2:
            key = copy.deepcopy(rotate_180(key))
        elif r == 3:
            key = copy.deepcopy(rotate_270(key))
        for h in range(len(lock)):
            if h >= len(save):
                key.append([0] * len(lock))
            for w in range(len(lock)):
                if w >= len(save[0]):
                    key[h].append(0)
        for h in range(-len(key) + 1, len(key)):
            for w in range(-len(key) + 1, len(key)):
                tmp = copy.deepcopy(key)
                save2 = copy.deepcopy(list())
                for i in range(len(key)):
                    for j in range(len(key)):
                        try:
                            if h + i >= 0 and w + j >= 0:
                                tmp[h+i][w+j] = key[i][j]
                                save2.append([h + i, w + j])
                        except:
                            pass
                for i in range(len(key)):
                    for j in range(len(key)):
                        if [i, j] not in save2:
                            tmp[i][j] = 0
                confirm = 0
                for i in range(len(key)):
                    for j in range(len(key)):
                        if tmp[i][j] + lock[i][j] == 1:
                            confirm += 1
                if confirm == pow(len(key), 2):
                    return True
        key = copy.deepcopy(save)
    return False