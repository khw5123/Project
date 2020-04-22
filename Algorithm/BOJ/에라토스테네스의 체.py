def solve(n, arr):
    ret = list()
    for i in range(len(arr)):
        if arr[i] != -1:
            for j in range(i, len(arr), arr[i]):
                if arr[j] != -1 and arr[j] not in ret:
                    ret.append(arr[j])
                arr[j] = -1
    return ret

n, k = map(int, input().split())
arr = [i for i in range(2, n + 1)]
print(solve(n, arr)[k - 1])