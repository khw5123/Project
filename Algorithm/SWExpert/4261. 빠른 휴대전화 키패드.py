keypad = ['','','abc','def','ghi','jkl','mno','pqrs','tuv','wxyz']

for t in range(int(input())):
    s, n = map(str, input().split())
    word = list(map(str, input().split()))
    answer = 0
    for w in word:
        if len(w) == len(s):
            confirm = True
            for i in range(len(w)):
                if w[i] not in keypad[int(s[i])]:
                    confirm = False
                    break
            if confirm:
                answer += 1
    print('#' + str(t+1), str(answer))