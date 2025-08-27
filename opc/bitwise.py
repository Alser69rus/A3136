def get(value: int, n: int):
    if value is None: value = 0
    return (value >> n) & 1


def set(value: int, n: int):
    if value is None: value = 0
    return (1 << n) | value


def reset(value: int, n: int):
    if value is None: value = 0
    return (~(1 << n)) & value


def override(value: int, n: int, bit_value):
    if bit_value:
        return set(value, n)
    else:
        return reset(value, n)


def to_signed32(n):
    n = n & 0xffffffff
    return n | (-(n & 0x80000000))
