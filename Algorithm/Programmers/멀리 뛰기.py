def solution(n):
    jump = [1, 2]
    save = [0] * (n+1)
    save[0] = 1
    for i in range(1, n+1):
        for j in range(len(jump)):
            if i - jump[j] >= 0:
                save[i] = (save[i] + save[i - jump[j]]) % 1234567
    return save[n]