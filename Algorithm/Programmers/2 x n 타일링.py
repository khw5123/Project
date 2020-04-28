def solution(n):
    answer = 0
    save = list()
    save.append(1)
    save.append(2)
    for i in range(2, n):
        save.append((save[-1] + save[-2]) % 1000000007)
    answer = save[-1]
    return answer