def solve(idx, count, num, answer):
    if count == 0 or idx == len(num)-1:
        if answer[0] < int(''.join(num)):
            answer[0], answer[1] = int(''.join(num)), count
        elif answer[0] == int(''.join(num)):
            if answer[1] % 2 == 1 and count % 2 == 0:
                answer[0], answer[1] = int(''.join(num)), count
        return
    if num[idx] < max(num[idx+1:]):
        change = idx+1 + num[idx+1:].index(max(num[idx+1:]))
        for i in range(num[idx+1:].count(max(num[idx+1:]))):
            num[idx], num[change] = num[change], num[idx]
            solve(idx+1, count-1, num, answer)
            num[idx], num[change] = num[change], num[idx]
            if i != num[idx+1:].count(max(num[idx+1:]))-1:
                change += num[change+1:].index(max(num[idx+1:])) + 1
            else:
                break
    else:
        solve(idx+1, count, num, answer)

for t in range(int(input())):
    num, count = map(int, input().split())
    num = list(map(str, str(num)))
    answer = [0, 0]
    solve(0, count, num, answer)
    if answer[1] % 2 == 1:
        confirm = False
        for i in range(1, len(str(answer[0]))):
            if str(answer[0])[i-1] == str(answer[0])[i]:
                confirm = True
                break
        if not confirm:
            answer[0] = int(str(answer[0])[:len(str(answer[0]))-2] + str(answer[0])[-1] + str(answer[0])[-2])
    print('#' + str(t+1), str(answer[0]))