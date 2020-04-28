import math

def solution(n, stations, w):
    answer = 0
    for i in range(len(stations)-1):
        answer += math.ceil((stations[i+1]-stations[i]-w*2-1)/(w*2+1))
    answer += math.ceil((stations[0]-w-1)/(w*2+1))
    answer += math.ceil((n-stations[-1]-w)/(w*2+1))
    return answer