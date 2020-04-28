def solution(n, arr1, arr2):
    answer = []
    tmp = []
    for i in range(n):
        tmp.append(arr1[i] | arr2[i])
    for i in range(n):
        tmp[i] = bin(tmp[i])[2:]
    for i in range(n):
        s = ''
        for c in tmp[i]:
            if c == '1':
                s += '#'
            else:
                s += ' '
        answer.append(s)
    for i in range(n):
        if len(answer[i]) != n:
            answer[i] = answer[i].rjust(n)
    return answer