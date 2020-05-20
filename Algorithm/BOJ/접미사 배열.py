def solution(s):
    answer = []
    for i in range(len(s)):
        answer.append(s[i:len(s)])
    answer.sort()
    return answer

s = input()
for v in solution(s):
    print(v)