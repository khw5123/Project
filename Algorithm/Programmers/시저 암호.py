def solution(s, n):
    answer = ''
    for c in s:
        if c == ' ':
            answer += ' '
            continue
        if ord(c) > 64 and ord(c) < 91:
            if ord(c) + n > 90:
                answer += chr((ord(c) + n - 90 + 64))
            else:
                answer += chr(ord(c) + n)
        else:
            if ord(c) + n > 122:
                answer += chr(ord(c) + n - 122 + 96)
            else:
                answer += chr(ord(c) + n)
    return answer