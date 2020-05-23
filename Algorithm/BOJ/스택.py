import sys

n = int(input())
queue = []
for _ in range(n):
    command = sys.stdin.readline().strip()
    if 'push' in command:
        stack.append(command.split(' ')[1])
    elif command == 'pop':
        if stack:
            print(stack.pop())
        else:
            print(-1)
    elif command == 'size':
        print(len(stack))
    elif command == 'empty':
        if stack:
            print(0)
        else:
            print(1)
    elif command == 'top':
        if stack:
            print(stack[-1])
        else:
            print(-1)