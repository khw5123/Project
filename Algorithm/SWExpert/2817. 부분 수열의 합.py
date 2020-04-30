def solve(idx, sum_, n, k, li, answer):
    if idx == n:
        if sum_ == k:
            answer[0] += 1
        return
    if sum_ > k:
        return
    solve(idx+1, sum_+li[idx], n, k, li, answer)
    solve(idx+1, sum_, n, k, li, answer)

for t in range(int(input())):
    n, k = map(int, input().split())
    li = list(map(int, input().split()))
    answer = [0]
    solve(0, 0, n, k ,li, answer)
    print('#' + str(t+1), str(answer[0]))