def promising(col, row):
    for i in range(col):
        if row[col] == row[i] or abs(row[col]-row[i]) == col-i:
            return False
    return True

def solution(n, col, row):
    if col == n:
        return 1
    ret = 0
    for i in range(n):
        row[col] = i
        if promising(col, row):
            ret += solution(n, col+1, row)
    return ret

n = int(input())
answer = solution(n, 0, [0]*n)
print(answer)