for t in range(int(input())):
    s = input()
    bar = list()
    count = 0
    answer = 0
    for c in s:
        if c == '(':
            if len(bar) != 0 and bar[-1][0] == '(' and bar[-1][1] == 'y':
                bar[-1][1] = 'n'
            count += 1
            bar.append([c, 'y', False])
        else:
            if bar[-1][0] == '(' and bar[-1][1] == 'y':
                count -= 1
                answer += count
                bar.pop()
            elif bar[-1][0] == '(' and bar[-1][1] == 'n':
                answer += 1
                count -= 1
                bar.pop()
    print('#' + str(t+1), str(answer))