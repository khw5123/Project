s, bomb = input(), 'PPAP'
answer = []
for i in range(len(s)):
    answer.append(s[i])
    if ''.join(answer[-len(bomb):]) == bomb:
        for _ in range(len(bomb)):
            answer.pop()
        answer.append('P')
if ''.join(answer) == 'P':
    print(bomb)
else:
    print('NP')