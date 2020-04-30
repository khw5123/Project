for c in input():
    if ord(c) > 96 and ord(c) < 123:
        print(chr(ord(c) - 32), end='')
    else:
        print(c, end='')
print()