def check():
    if len(str(target)) > m:
        return False
    for i in range(len(str(target))):
        if int(str(target)[i]) not in num:
            return False
    return True

def solve():
    result = -1
    queue = [save[i] for i in range(len(save))]
    dp = [len(str(i)) if i in save else 987654321 for i in range(1000)]
    while queue:
        number = queue.pop()
        for i in range(len(save)):
            for j in range(len(op)):
                count = dp[number] + dp[save[i]] + 1
                if count >= m:
                    continue
                if op[j] == 1:
                    if 0 <= number+save[i] and number+save[i] < 1000 and dp[number+save[i]] > count:
                        queue.append(number+save[i])
                        dp[number+save[i]] = count
                elif op[j] == 2:
                    if 0 <= number-save[i] and number-save[i] < 1000 and dp[number-save[i]] > count:
                        queue.append(number-save[i])
                        dp[number-save[i]] = count
                elif op[j] == 3:
                    if 0 <= number*save[i] and number*save[i] < 1000 and dp[number*save[i]] > count:
                        queue.append(number*save[i])
                        dp[number*save[i]] = count
                else:
                    if save[i] != 0 and 0 <= number//save[i] and number//save[i] < 1000 and dp[number//save[i]] > count:
                        queue.append(number//save[i])
                        dp[number//save[i]] = count
    if dp[target] != 987654321 and dp[target] <= m:
        result = dp[target] + 1
    return result

for t in range(int(input())):
    n, o, m = map(int, input().split())
    num = list(map(int, input().split()))
    op = list(map(int, input().split()))
    target = int(input())
    answer = -1
    if check():
        answer = len(str(target))
    else:
        save = []
        for n1 in num:
            for n2 in num:
                for n3 in num:
                    if n1 not in save:
                        save.append(n1)
                    if n1*10 + n2 not in save:
                        save.append(n1*10 + n2)
                    if (n1*10 + n2)*10 + n3 not in save:
                        save.append((n1*10 + n2)*10 + n3)
        answer = solve()
    print('#' + str(t+1), answer)