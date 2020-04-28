def convert(n, num):
    result = list()
    while True:
        result.append(str(num % n))
        num //= n
        if num < n:
            if num != 0:
                result.append(str(num))
            break
    result.reverse()
    for i in range(len(result)):
        if n > 10 and int(result[i]) >= 10:
            result[i] = chr(int(result[i]) + 55)
    return ''.join(result)

def solution(n, t, m, p):
    answer = ''
    total = ''
    num = 0
    while True:
        if len(total) > m * t:
            break
        total += convert(n, num)
        num += 1
    for i in range(p-1, len(total), m):
        answer += total[i]
    return answer[:t]