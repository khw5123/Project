import sys

def update(tree, index, diff):
    while index < len(tree):
        tree[index] += diff
        index += (index & (-index))

def _sum(tree, index):
    result = 0
    while index > 0:
        result += tree[index]
        index -= (index & (-index))
    return result

for line in sys.stdin:
    n, k = map(int, line.split())
    arr, tree = [0]+list(map(int, sys.stdin.readline().split())), [0]*(n+1)
    answer, INF = '', 9876543210
    for i in range(1, n+1):
        # 양수일 경우 암묵적으로 0 업데이트
        if arr[i] < 0: # 음수일 경우 1 업데이트
            update(tree, i, 1)
        elif arr[i] == 0: # 0일 경우 큰 수 업데이트
            update(tree, i, INF)
    for _ in range(k):
        command, i, j = map(str, sys.stdin.readline().split())
        i, j = int(i), int(j)
        if command == 'C':
            before, after = arr[i], j # 변경 전과 후
            if before > 0 and after < 0: # 양수에서 음수로 변경
                update(tree, i, 1)
            elif before > 0 and after == 0: # 양수에서 0으로 변경
                update(tree, i, INF)
            elif before < 0 and after > 0: # 음수에서 양수로 변경
                update(tree, i, -1)
            elif before < 0 and after == 0: # 음수에서 0으로 변경
                update(tree, i, INF-1)
            elif before == 0 and after > 0: # 0에서 양수로 변경
                update(tree, i, -INF)
            elif before == 0 and after < 0: # 0에서 음수로 변경
                update(tree, i, 1-INF)
            arr[i] = j # 수 변경
        else:
            # 모든 수가 음수(1)라고 해도 최대 라운드가 10^5 이므로 구간 합이 해당 수를 넘어가지 못함. 따라서 10^5 초과라면 0이 포함된 것임
            result = _sum(tree, j) - _sum(tree, i-1) # 추상화된 구간 곱
            if result > pow(10, 5): # 구간 곱이 0일 경우
                answer += '0'
            elif result % 2 == 0: # 구간 곱이 양수일 경우
                answer += '+'
            elif result % 2 == 1: # 구간 곱이 음수일 경우
                answer += '-'
    print(answer)