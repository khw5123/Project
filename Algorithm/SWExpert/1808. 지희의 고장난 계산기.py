def solve(num, count):
    global answer
    if num >= target:
        if num == target:
            answer = min(answer, count+1)
        return
    if dp[num] < count:
        return
    dp[num] = count
    for i in range(len(li)):
        solve(num*li[i], count+len(str(li[i]))+1)

def make(num):
    if len(num) >= len(str(target)):
        return
    for i in range(len(n)):
        num += str(n[i])
        if num[0] != '0':
            if target >= int(num) and target % int(num) == 0:
                if int(num) not in li:
                    li.append(int(num))
            make(num)
        num = num[:len(num)-1]

for t in range(int(input())):
    tmp = list(map(int, input().split()))
    target = int(input())
    answer = 987654321
    dp = [987654321]*(target+1)
    n, li = [], []
    for i in range(len(tmp)):
        if tmp[i]:
            n.append(i)
    make('')
    for num in li:
        solve(num, len(str(num)))
    if answer == 987654321:
        answer = -1
    print('#' + str(t+1), str(answer))