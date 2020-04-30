def solve(s):
    result = True
    for i in range(len(s)//2):
        if s[i] != s[-(i+1)]:
            result = False
            break
    return result

for t in range(int(input())):
    s = sorted(list(input()))
    answer = 0
    for i in range(len(s)):
        for j in range(i+1, len(s)+1):
            if solve(s[i:j]):
                answer += 1
    print('#' + str(t+1), str(answer))