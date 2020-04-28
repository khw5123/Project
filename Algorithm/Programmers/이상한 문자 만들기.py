def solution(s):
    answer = ''
    for string in s.split(' '):
        for i in range(len(string)):
            if i % 2 == 0:
                answer += string[i].upper()
            else:
                answer += string[i].lower()
        answer += ' '
    return answer[:len(answer)-1]