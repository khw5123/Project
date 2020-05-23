import sys
from collections import deque

n = int(input())
deq = deque()
for _ in range(n):
    command = sys.stdin.readline().strip()
    if 'push_front' in command:
        deq.appendleft(command.split(' ')[1])
    elif 'push_back' in command:
        deq.append(command.split(' ')[1])
    elif command == 'pop_front':
        if deq:
            print(deq.popleft())
        else:
            print(-1)
    elif command == 'pop_back':
        if deq:
            print(deq.pop())
        else:
            print(-1)
    elif command == 'size':
        print(len(deq))
    elif command == 'empty':
        if deq:
            print(0)
        else:
            print(1)
    elif command == 'front':
        if deq:
            print(deq[0])
        else:
            print(-1)
    elif command == 'back':
        if deq:
            print(deq[-1])
        else:
            print(-1)