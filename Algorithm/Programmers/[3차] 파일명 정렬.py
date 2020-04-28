def solution(files):
    answer = []
    save = list()
    for i in range(len(files)):
        save.append([])
        idx = 0
        lock = False
        for j in range(len(files[i])):
            if not lock and files[i][j].isdigit():
                save[-1].append(files[i][:j])
                idx = j
                lock = True
            if lock and not files[i][j].isdigit():
                save[-1].append(files[i][idx:j])
                idx = j
                save[-1].append(files[i][idx:])
                lock = False
                break
        if lock:
            save[-1].append(files[i][idx:])
    save.sort(key=lambda x: (x[0].lower(), int(x[1])))
    for s in save:
        answer.append(''.join(s))
    return answer