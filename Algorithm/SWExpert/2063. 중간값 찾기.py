n = int(input())
num = sorted(list(map(int, input().split())))
print(num[len(num) // 2])