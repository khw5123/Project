s, bomb = input(), input()
answer = []
for i in range(len(s)):
    answer.append(s[i])
    if ''.join(answer[-len(bomb):]) == bomb:
        for _ in range(len(bomb)):
            answer.pop()
if answer:
    answer = ''.join(answer)
else:
    answer = 'FRULA'
print(answer)