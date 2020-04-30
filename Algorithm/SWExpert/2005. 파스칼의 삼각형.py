for t in range(int(input())):
    n = int(input())
    li = [['1'], ['1', '1']]
    print('#' + str(t+1))
    for i in range(n):
        if len(li) <= i:
            li.append(['1'])
            for j in range(len(li[i-1])-1):
                li[-1].append(str(int(li[i-1][j]) + int(li[i-1][j+1])))
            li[-1].append('1')
        print(' '.join(li[i]))