def solution(record):
    answer = []
    uid = dict()
    for i in range(len(record)):
        if record[i].split(' ')[0] == 'Enter':
            if record[i].split(' ')[1] in uid:
                uid[record[i].split(' ')[1]] = record[i].split(' ')[2]
            else:
                uid[record[i].split(' ')[1]] = record[i].split(' ')[2]
            answer.append(record[i].split(' ')[1] + '님이 들어왔습니다.')
        elif record[i].split(' ')[0] == 'Leave':
            answer.append(record[i].split(' ')[1] + '님이 나갔습니다.')
        else:
            uid[record[i].split(' ')[1]] = record[i].split(' ')[2]
    for i in range(len(answer)):
        answer[i] = answer[i].replace(answer[i].split('님')[0], uid[answer[i].split('님')[0]])
    return answer