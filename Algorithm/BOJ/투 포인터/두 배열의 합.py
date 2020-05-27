def get_case(arr):
    di = {}
    for i in range(len(arr)):
        _sum = 0
        for j in range(i, len(arr)):
            _sum += arr[j]
            if _sum not in di:
                di[_sum] = 1
            else:
                di[_sum] += 1
    return di

t = int(input())
input();a = list(map(int, input().split()))
input();b = list(map(int, input().split()))
case_a, case_b = get_case(a), get_case(b)
answer = 0
for k, v in case_a.items():
    if t-k in case_b:
        answer += (v*case_b[t-k])
print(answer)