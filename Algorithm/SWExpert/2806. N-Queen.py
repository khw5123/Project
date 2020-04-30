def promising(col, row):
    for i in range(col):
        if row[col] == row[i] or abs(row[col] - row[i]) == col - i:
            return False
    return True

def solve(col, n, row):
    answer = 0
    if col == n:
        return 1
    else:
        for i in range(n):
            row[col] = i
            if promising(col, row):
                answer += solve(col + 1, n, row)
    return answer

for t in range(int(input())):
    n = int(input())
    answer = solve(0, n, [0]*n)
    print('#' + str(t+1), str(answer))