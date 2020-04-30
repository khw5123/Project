for t in range(int(input())):
    s = input()
    answer = [[] for _ in range(5)]
    for i in range(len(s)):
        if i == 0:
            answer[0].append(['..#..'])
            answer[1].append(['.#.#.'])
            answer[2].append(['#.' + s[i] + '.#'])
            answer[3].append(['.#.#.'])
            answer[4].append(['..#..'])
        else:
            answer[0].append(['.#..'])
            answer[1].append(['#.#.'])
            answer[2].append(['.' + s[i] + '.#'])
            answer[3].append(['#.#.'])
            answer[4].append(['.#..'])
    for a in answer:
        tmp = ''
        for b in a:
            tmp += ''.join(b)
        print(tmp)