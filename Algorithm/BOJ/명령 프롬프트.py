n = int(input())
answer = ''
files = []
for _ in range(n):
    files.append(input())
for i in range(len(files[0])):
    c = set()
    for j in range(len(files)):
        c.add(files[j][i])
    if len(c) == 1:
        answer += files[0][i]
    else:
        answer += '?'
print(answer)