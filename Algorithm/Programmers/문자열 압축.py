def solution(s):
    answer = 0
    save = list()
    for i in range(1, len(s)):
        prev = s[:i]
        save.append([])
        for j in range(i, len(s)+1, i):
            save[-1].append(prev)
            prev = s[j:j+i]
        if s[sum([len(a) for a in save[-1]]):] != '':
            save[-1].append(s[sum([len(a) for a in save[-1]]):])
    result = list()
    for i in range(len(save)):
        string = [save[i][0]]
        first = True
        count = 2
        pos = 0
        for j in range(len(save[i])-1):
            if len(save[i][j]) != len(save[i][j+1]):
                string += [save[i][j+1]]
            else:
                if save[i][j] == save[i][j+1]:
                    if first:
                        string.pop()
                        
                        pos = len(string)
                        string += [str(count)]
                        string += [save[i][j]]
                        first = False
                    else:
                        count += 1
                        string[pos] = str(count)
                else:
                    count = 2
                    pos = 0
                    first = True
                    string += [save[i][j+1]]
        length = lambda ss: len(ss)
        result.append(length(''.join(string)))
    if len(result) == 0:
        answer = len(s)
    else:
        answer = min(result)
    return answer