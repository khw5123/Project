def solution(m, n, puddles):
    save = [[0]*m for _ in range(n)]
    save[0][0] = 1
    for i in range(n):
        for j in range(m):
            if [j+1, i+1] in puddles or (i == 0 and j == 0):
                continue
            if i == 0:
                save[i][j] = save[i][j-1]
            elif j == 0:
                save[i][j] = save[i-1][j]
            else:
                save[i][j] = (save[i-1][j] + save[i][j-1]) % 1000000007
    return save[n-1][m-1]