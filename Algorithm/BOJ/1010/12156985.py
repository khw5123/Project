def combination(n, r):
    def factorial(n):
        if n == 1 or n == 0:
            return 1
        else:
            return n * factorial(n - 1)
    return factorial(n) // (factorial(n - r) * factorial(r))

count = int(input(''))
for _ in range(count):
    r, n = map(int, input().split())
    result = combination(n, r)
    print(result)