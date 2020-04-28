def calc(s, N, number):
    result = 0
    start = 0
    tmp = ''
    for i in range(len(s)):
        if s[i] != str(N):
            start = i
            result = int(tmp)
            break
        else:
            tmp += s[i]
    tmp = ''
    operator = []
    for i in range(start, len(s)):
        if s[i] == str(N):
            tmp += s[i]
            if i == len(s) - 1 and len(operator) != 0:
                if operator[0] == '+':
                    result += int(tmp)
                elif operator[0] == '-':
                    result -= int(tmp)
                elif operator[0] == '*':
                    result *= int(tmp)
                elif operator[0] == '/':
                    result //= int(tmp)
        else:
            if len(operator) == 1:
                if operator[0] == '+':
                    result += int(tmp)
                elif operator[0] == '-':
                    result -= int(tmp)
                elif operator[0] == '*':
                    result *= int(tmp)
                elif operator[0] == '/':
                    result //= int(tmp)
                tmp = ''
                operator.pop()
            operator.append(s[i])
    return result

def solve(s, N, number):
    answer = 9
    if s.count(str(N)) < 9:
        if s[-1] == str(N):
            if eval(''.join(s)) == number or calc(s, N, number) == number:
                answer = min(answer, s.count(str(N)))
        s.append(str(N))
        answer = min(answer, solve(s, N, number))
        s.pop()
        if s[-1] != '+' and s[-1] != '-' and s[-1] != '*' and s[-1] != '/':
            s.append('+')
            answer = min(answer, solve(s, N, number))
            s.pop()
            s.append('-')
            answer = min(answer, solve(s, N, number))
            s.pop()
            s.append('*')
            answer = min(answer, solve(s, N, number))
            s.pop()
            s.append('/')
            answer = min(answer, solve(s, N, number))
            s.pop()
        return answer
    return answer

def solution(N, number):
    answer = solve([str(N)], N, number)
    return -1 if answer == 9 else answer