import datetime

def solution(n, t, m, timetable):
    timetable.sort()
    answer = datetime.datetime.strptime(timetable[0], '%H:%M') + datetime.timedelta(minutes=-1)
    now = datetime.datetime.strptime('09:00', '%H:%M')
    count = 0
    for nn in range(n):
        for mm in range(m):
            count += 1
            if len(timetable) != 0 and datetime.datetime.strptime(timetable[0], '%H:%M') <= now:
                if len(timetable) == 1:
                    if datetime.datetime.strptime(timetable[0], '%H:%M') == now:
                        if count != n*m:
                            return datetime.datetime.strptime(timetable[0], '%H:%M').strftime('%H:%M')
                        else:
                            return (datetime.datetime.strptime(timetable[0], '%H:%M') + datetime.timedelta(minutes=-1)).strftime('%H:%M')
                    else:
                        if count == n*m:
                            return (datetime.datetime.strptime(timetable[0], '%H:%M') + datetime.timedelta(minutes=-1)).strftime('%H:%M')
                if count == n*m:
                    answer = datetime.datetime.strptime(timetable[0], '%H:%M') + datetime.timedelta(minutes=-1)
                del timetable[0]
            else:
                answer = now
        now += datetime.timedelta(minutes=t)
    if len(timetable) != 0:
        if datetime.datetime.strptime(timetable[0], '%H:%M') < now:
            if count != n*m:
                answer = datetime.datetime.strptime(timetable[0], '%H:%M') + datetime.timedelta(minutes=-1)
    return answer.strftime('%H:%M')