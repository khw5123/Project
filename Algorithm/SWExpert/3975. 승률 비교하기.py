answer = []

for t in range(int(input())):
    a, b, c, d = map(float, input().split())
    if a / b > c / d:
        answer.append('ALICE')
    elif a / b < c / d:
        answer.append('BOB')
    else:
        answer.append('DRAW')

for i in range(len(answer)):
    print('#' + str(i+1), answer[i])