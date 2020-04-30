for t in range(int(input())):
    n = int(input())
    string = input()
    answer = [0]*n
    idx = 0
    for word in string.split():
        end = False
        if '!' in word or '?' in word or '.' in word:
            word = word[:len(word)-1]
            end = True
        confirm = True
        for i in range(len(word)):
            if i == 0:
                if ord(word[i]) < 65 or ord(word[i]) > 90:
                    confirm = False
                    break
            else:
                if ord(word[i]) < 97 or ord(word[i]) > 122:
                    confirm = False
                    break
        if confirm:
            answer[idx] += 1
        if end:
            idx += 1
    print('#' + str(t+1), end=' ')
    for v in answer:
        print(v, end=' ')
    print()