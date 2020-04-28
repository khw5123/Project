def solution(x):
    answer = True
    tmp = 0
    for n in str(x):
        tmp += int(n)
    if x % tmp != 0:
        answer = False
    return answer