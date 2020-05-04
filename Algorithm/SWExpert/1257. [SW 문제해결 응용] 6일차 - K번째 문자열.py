for t in range(int(input())):
    k = int(input())
    s = input()
    li = set()
    answer = 'none'
    for i in range(len(s)+1):
        for j in range(i+1, len(s)+1):
            li.add(s[i:j])
    if k <= len(li):
        answer = sorted(list(li))[k-1]
    print('#' + str(t+1), answer)