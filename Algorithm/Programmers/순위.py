def solution(n, results):
    answer = 0
    win = [[] for _ in range(n+1)]
    lose = [[] for _ in range(n+1)]
    for result in results:
        win[result[0]].append(result[1])
        lose[result[1]].append(result[0])
    for i in range(1, n+1):
        for j in win[i]:
            for k in lose[i]:
                if k not in lose[j]:
                    lose[j].append(k)
        for j in lose[i]:
            for k in win[i]:
                if k not in win[j]:
                    win[j].append(k)
    for i in range(1, n+1):
        if len(win[i]) + len(lose[i]) == n-1:
            answer += 1
    return answer