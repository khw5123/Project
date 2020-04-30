for t in range(int(input())):
    answer = 0
    n = int(input())
    num = ''
    while len(num) != n:
        num += ''.join(list(map(str, input().split())))
    while str(answer) in num:
        answer += 1
    print('#' + str(t+1), str(answer))

'''
for t in range(int(input())):
    n = int(input())
    save = []
    num = ''
    while len(num) != n:
        num += ''.join(list(map(str, input().split())))
    for i in range(1, (5 if n > 4 else n+1)): # 1 -> 1000 <10>, 2 -> 999 <90>, 3 -> 998 <900>, 4 -> 997 <9000>
        for j in range(0, len(num)-i+1):
            if int(num[j:j+i]) not in save:
                save.append(int(num[j:j+i]))
    save.sort()
    for i in range(len(save)):
        if i != save[i]:
            print('#' + str(t+1), str(i))
            break
'''