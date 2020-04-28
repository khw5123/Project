def solution(n):
    answer = 0
    save = list()
    for c in str(n):
        save.append(c)
    save.sort(reverse=True)
    answer = int(''.join(save))
    return answer