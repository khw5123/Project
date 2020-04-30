li = [1]
for i in range(1, 12):
    li.append(pow(10, i) + ((9-1) * sum(li[:i])))

def solve(n):
    global li
    result = 0
    for i in range(len(n)):
        num = n[i:]
        if len(num) == 1 and int(num) >= 4:
            result += 1
        else:
            if int(num[0]) < 4:
                result += (int(num[0]) * sum(li[:len(num)-1]))
            elif int(num[0]) > 4:
                result += (pow(10, len(num)-1) + ((int(num[0])-1) * sum(li[:len(num)-1])))
    return result

for t in range(int(input())):
    a, b = map(int, input().split())
    if a < 0 and b > 0:
        answer = (abs(a) + abs(b) - 1) - (solve(str(abs(a))) + solve(str(abs(b))))
    else:
        answer = (abs(abs(a) - abs(b))) - (abs(solve(str(abs(a))) - solve(str(abs(b)))))
    print('#' + str(t+1), str(answer))