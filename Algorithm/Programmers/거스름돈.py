def solution(n, money):
    save = [0] * (n+1)
    save[0] = 1
    for i in range(len(money)):
        for j in range(1, n+1):
            if j - money[i] >= 0:
                save[j] += (save[j - money[i]] % 1000000007)
    return save[n]