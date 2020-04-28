def solution(s):
    answer = ''
    for string in s.split(' '):
        if string != '':
            answer += string[0].upper() + string[1:].lower()
        answer += ' '
    return answer[:len(answer)-1]