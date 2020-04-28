def solution(n):
    answer = 0
    origin = n
    while True:
        n += 1
        if str(bin(origin)).count('1') == str(bin(n)).count('1'):
            answer = n
            break
    return answer