def solution(s):
    answer = ''
    save = [c for c in s]
    save.sort(reverse=True)
    answer = ''.join(save)
    return answer