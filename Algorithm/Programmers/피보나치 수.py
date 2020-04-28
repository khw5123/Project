def matmul(a, b, mod):
    result = [[0, 0], [0, 0]]
    for i in range(2):
        for j in range(2):
            for k in range(2):
                result[i][j] = (result[i][j] + a[i][k] * b[k][j]) % mod
    return result

def fibonacci_matrix(n, mod):
    arr, constant = [[1, 0], [0, 1]], [[1, 1], [1, 0]]
    while n > 0:
        if n % 2 == 1:
            arr = matmul(arr, constant, mod)
        constant = matmul(constant, constant, mod)
        n = n // 2
    return arr[0][0]

def solution(n):
    answer = fibonacci_matrix(n-1, 1234567)
    return answer