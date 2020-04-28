def solution(msg):
    answer = []
    index = dict()
    for i in range(1, 27):
        index[i] = chr(64+i)
    idx = 0
    while idx < len(msg):
        tmp = 1
        while True:
            if idx + tmp > len(msg):
                break
            if msg[idx:idx+tmp] in index.values():
                tmp += 1
            else:
                tmp -= 1
                break
        if msg[idx:idx+tmp+1] not in index.values():
            index[len(index)+1] = msg[idx:idx+tmp+1]
        for k, v in index.items():
            if v == msg[idx:idx+tmp]:
                answer.append(k)
                break
        idx += tmp
    return answer