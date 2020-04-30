for t in range(int(input())):
    s = input()
    answer = True
    for i in range(len(s) // 2):
        if s[i] == '?' or s[-i-1] == '?':
            continue
        else:
            if s[i] != s[-i-1]:
                answer = False
                break
    if answer:
        print('#' + str(t+1) + ' Exist')
    else:
        print('#' + str(t+1) + ' Not exist')