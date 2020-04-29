for t in range(int(input())):
    n = int(input())
    atom = [list(map(int, input().split())) for _ in range(n)]
    answer = 0
    for _ in range(4000):
        meet = dict()
        for i in range(len(atom)):
            if atom[i][2] != -1:
                if atom[i][2] == 0:
                    atom[i][1] += 0.5
                elif atom[i][2] == 1:
                    atom[i][1] -= 0.5
                elif atom[i][2] == 2:
                    atom[i][0] -= 0.5
                else:
                    atom[i][0] += 0.5
                if (atom[i][0], atom[i][1]) in meet:
                    meet[(atom[i][0], atom[i][1])].append(i)
                else:
                    meet[(atom[i][0], atom[i][1])] = [i]
        for k, v in meet.items():
            if len(v) > 1:
                for idx in v:
                    answer += atom[idx][3]
                    atom[idx][2] = -1
    print('#' + str(t+1), str(answer))