def solve(arr):
    if len(arr) == 0:
        return
    mid = len(arr)//2
    tree[len(arr)].append(arr[mid])
    solve(arr[:mid])
    solve(arr[mid+1:])

k = int(input())
li = list(map(int, input().split()))
tree = [[] for _ in range(sum([pow(2, i) for i in range(k)])+2)]
solve(li)
for i in range(len(tree)-1, -1, -1):
    if tree[i]:
        for num in tree[i]:
            print(num, end=' ')
        print()