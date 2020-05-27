def solution(formula):
    answer, li = 0, []
    tmp = ''
    for c in formula:
        if c in '+-*':
            li.append(tmp)
            tmp = ''
            li.append(c)
        else:
            tmp += c
    li.append(tmp)
    check = False
    while len(li) != 1:
        if not check:
            prev = len(li)
            confirm = False
            for i in range(len(li)):
                if li[i] == '-':
                    confirm = True
                elif confirm and li[i] == '+':
                    n = int(li[i-1]) + int(li[i+1])
                    for _ in range(3):
                        del li[i-1]
                    li.insert(i-1, n)
                    break
            if prev == len(li):
                check = True
        else:
            if li[1] == '+':
                n = int(li[0]) + int(li[2])
            else:
                n = int(li[0]) - int(li[2])
            for _ in range(3):
                del li[0]
            li.insert(0, n)
    answer = li[0]
    return answer

formula = input()
print(solution(formula))