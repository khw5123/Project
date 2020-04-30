import time
from datetime import datetime

for t in range(int(input())):
    d, h, m = map(int, input().split())
    start = time.mktime(datetime(2011, 11, 11, 11, 11, 0).timetuple())
    end = time.mktime(datetime(2011, 11, d, h, m, 0).timetuple())
    diff = int(end - start) // 60
    if diff < 0:
        print('#' + str(t+1) + ' -1')
    else:
        print('#' + str(t+1), str(diff))