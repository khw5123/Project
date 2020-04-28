def solution(s):
    answer = True
    if s.lower().count('p') != s.lower().count('y'):
        answer = False
    return answer