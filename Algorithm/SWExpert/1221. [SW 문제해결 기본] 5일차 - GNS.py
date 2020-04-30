di = {'ZRO':0, 'ONE':1, 'TWO':2, 'THR':3, 'FOR':4, 'FIV':5, 'SIX':6, 'SVN':7, 'EGT':8, 'NIN':9}

for t in range(int(input())):
    input()
    answer = []
    for n in list(map(str, input().split())):
        answer.append([di[n], n])
    answer.sort()
    print('#' + str(t+1))
    for n in answer:
        print(n[1], end=' ')
    print()