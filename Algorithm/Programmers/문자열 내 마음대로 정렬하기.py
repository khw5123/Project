def solution(strings, n):
    answer = []
    save = list()
    for s in strings:
        save.append([s[n], s])
    save.sort()
    for s in save:
        answer.append(s[1])
    return answer