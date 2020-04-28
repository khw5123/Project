def solution(N, stages):
    answer = []
    save = dict()
    for i in range(1, N+1):
        enter, fail = 0, 0
        for j in range(len(stages)):
            if stages[j] >= i:
                enter += 1
                if stages[j] == i:
                    fail += 1
        save[i] = 0 if enter == 0 else fail / enter
    answer = [u[0] for u in sorted(save.items(), key=lambda kv: (-kv[1], kv[0]))]
    return answer