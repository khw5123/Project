def solution(name):
    answer = 0
    test = ['A' for _ in range(len(name))]
    for i in range(len(test)):
        if test[i] == name[i]:
            test[i] = '0'
    idx = 0
    while len(set(test)) != 1 or list(set(test))[0] == 'A':
        right, left, move = 0, 0, 0
        tmp, tmp2 = test * 2, name * 2
        for i in range(idx, len(test) + idx):
            if tmp[i] != '0' and tmp[i] != tmp2[i]:
                break
            right += 1
        for i in range(len(test) + idx, idx, -1):
            if tmp[i] != '0' and tmp[i] != tmp2[i]:
                break
            left -= 1
        if abs(right) <= abs(left):
            move = right
        else:
            move = left
        answer += abs(move)
        if idx + move > len(test)-1:
            idx = (idx + move - (len(test)-1))
        elif idx + move < 0:
            idx = (idx + move + len(test))
        else:
            idx += move
        if abs(ord(test[idx]) - ord(name[idx])) < 26 - abs(ord(test[idx]) - ord(name[idx])):
            answer += abs(ord(test[idx]) - ord(name[idx]))
        else:
            answer += (26 - abs(ord(test[idx]) - ord(name[idx])))
        test[idx] = '0'
    return answer