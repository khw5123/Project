def solution(N):
    answer = 0
    save = [1, 1]
    for i in range(1, N):
        save.append(save[-1] + save[-2])
    answer = save[-1]*2 + save[-2]*2
    return answer