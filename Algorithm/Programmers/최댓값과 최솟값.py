def solution(s):
    answer = ''
    save = [int(n) for n in s.split(' ')]
    answer = str(min(save)) + ' ' + str(max(save))
    return answer