def solution(m, musicinfos):
    answer = ''
    save = list()
    for i in range(len(musicinfos)):
        start, end, name, manuscript = musicinfos[i].split(',')[0], musicinfos[i].split(',')[1], musicinfos[i].split(',')[2], musicinfos[i].split(',')[3]
        tmp, idx = list(), 0
        while True:
            if idx+1 < len(manuscript):
                if manuscript[idx+1] != '#':
                    tmp.append(manuscript[idx])
                    idx += 1
                else:
                    tmp.append(manuscript[idx] + manuscript[idx+1])
                    idx += 2
            else:
                if idx != len(manuscript):
                    tmp.append(manuscript[idx])
                break
        sheet = list()
        time = (int(end.split(':')[0]) - int(start.split(':')[0])) * 60 + int(end.split(':')[1]) - int(start.split(':')[1])
        time2 = time
        if time < len(tmp):
            sheet = tmp[:time]
        else:
            while time > len(tmp):
                sheet += tmp
                time -= len(tmp)
            sheet += tmp[:time]
        music, idx = list(), 0
        while True:
            if idx+1 < len(m):
                if m[idx+1] != '#':
                    music.append(m[idx])
                    idx += 1
                else:
                    music.append(m[idx] + m[idx+1])
                    idx += 2
            else:
                if idx != len(m):
                    music.append(m[idx])
                break
        if time2 >= len(music):
            for j in range(len(sheet) - len(music) + 1):
                if music == sheet[j:j+len(music)]:
                    confirm = True
                    for k in range(j, j+len(music)):
                        if k != 0 and k % len(sheet) == 0:
                            confirm = False
                            break
                    if confirm:
                        save.append([time2, name])
                        break
    if len(save) != 0:
        save = sorted(save, key=lambda x: -x[0])
        answer = save[0][1]
    else:
        answer = '(None)'
    return answer