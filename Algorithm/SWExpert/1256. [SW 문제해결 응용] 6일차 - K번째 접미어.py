for t in range(int(input())):
    k = int(input())
    s = input()
    li = []
    answer = ''
    for i in range(len(s)):
        li.append(s[len(s)-i-2:])
    li.sort()
    if len(li) >= k:
        answer = li[k-1]
    else:
        answer = 'none'
    print('#' + str(t+1), answer)