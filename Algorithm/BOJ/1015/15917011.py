size = int(input())
array = list(map(int , input().split()))
compare = []
for i in range(0,len(array)):
    compare.append(array[i])
compare.sort()
for v in array:
    print(compare.index(v), end=' ')
    compare[compare.index(v)] = -1