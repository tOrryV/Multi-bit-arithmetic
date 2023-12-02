import math


def parcer(obj, n):
    args = [iter(obj)] * n
    return zip(*args)


def convert_to_hex(num):
    if num is None:
        return '0'
    if num == [0]:
        return '0'
    i = len(num) - 1
    while num[i] == 0:
        i -= 1
        if i == -1:
            return '0'
    num.reverse()
    hex_num = ''
    for i in range(len(num)):
        hex_el = hex(num[i])[2:]
        if len(hex_el) != 8:
            zeros = (8 - len(hex_el)) * '0'
            hex_str = zeros + hex_el
            hex_num += hex_str
        else:
            hex_num += hex_el
        hex_num = hex_num.lstrip('0')
    num.reverse()
    return hex_num.swapcase()


def convert_from_hex(hex_num):
    n = math.ceil(len(hex_num) / 8)
    hexs = []
    decs = []
    if len(hex_num) % 8 == 0:
        hexs = [''.join(i) for i in parcer(hex_num, 8)]
    else:
        zeros = 8 * n - len(hex_num)
        str_zeros = zeros * '0'
        final_hex = str_zeros + hex_num
        hexs = [''.join(i) for i in parcer(final_hex, 8)]
    for i in range(len(hexs)):
        decs.append(int(hexs[i], 16))
    decs.reverse()
    return decs


num_1_A = str(input('Enter the first number: '))
num_2_B = str(input('Enter the second number: '))
# num_3_C = str(input('Enter the third number: '))
num_Module = str(input('Enter the module: '))

A = convert_from_hex(num_1_A)
B = convert_from_hex(num_2_B)
# C = convert_from_hex(num_3_C)
Module = convert_from_hex(num_Module)


'''Основні функції'''


def LongAddition(a, b):
    max_len = max(len(a), len(b))
    carry = 0
    sum = []
    for i in range(max_len):
        temp_A = int(a[i]) if i < len(a) else 0
        temp_B = int(b[i]) if i < len(b) else 0
        temp = temp_A + temp_B + carry
        sum.append(temp & (2 ** 32 - 1))
        carry = temp >> 32
    if carry > 0:
        sum.append(carry)
    return sum


def LongSubstration(a, b):
    '''if LongCompare(a, b) == -1:
        result = LongSubstration(b, a)
        result.insert(0, 1)
        return result
'''
    borrow = 0
    sub = []
    max_len = max(len(a), len(b))
    for i in range(max_len):
        temp_A = int(a[i]) if i < len(a) else 0
        temp_B = int(b[i]) if i < len(b) else 0
        temp = temp_A - temp_B - borrow
        if temp >= 0:
            sub.append(temp)
            borrow = 0
        else:
            sub.append((2 ** 32 + temp))
            borrow = 1
    if borrow != 0:
        return None
    else:
        while len(sub) > 1 and sub[-1] == 0:
            sub.pop()
        return sub


def LongMultiply(a, b):
    if LongCompare(a, b) == -1:
        return LongMultiply(b, a)

    mul = [0] * (len(a) + len(b))

    for i in range(len(b)):
        carry = 0
        for j in range(len(a)):
            temp = mul[i + j] + a[j] * b[i] + carry
            mul[i + j] = temp & (2 ** 32 - 1)
            carry = temp >> 32

        if carry > 0:
            mul[i + len(a)] += carry

    while len(mul) > 1 and mul[-1] == 0:
        mul.pop()

    return mul


def LongDivideModule(a, b):
    if a == b:
        return ([1], [0])
    k = BitLength(b)
    remainder = a.copy()
    quotient = [0]
    while LongCompare(remainder, b) != -1:
        t = BitLength(remainder)
        c = LongShiftBitsToHigh(b, t - k)
        if LongCompare(remainder, c) < 0:
            t -= 1
            length = t - k
            c = LongShiftBitsToHigh(b, length)
        remainder = LongSubstration(remainder, c)
        temp = LongShiftBitsToHigh([1], t - k)
        quotient = LongAddition(quotient, temp)
    return (quotient, remainder)


def LongSquare(a):
    result = LongMultiply(a, a)
    return result


def LongPower(a, b):
    pow = [1]
    for i in range(BitLength(b)):
        if BitCheck(b, i) == 1:
            pow = LongMultiply(pow, a)
        a = LongMultiply(a, a)
        while len(a) < len(pow):
            a.append(0)
    return pow


'''Додаткові функції'''


def LongCompare(a, b):
    if a != [0]:
        while a[len(a) - 1] == 0:
            del a[len(a) - 1]
    if b != [0]:
        while b[len(b) - 1] == 0:
            del b[len(b) - 1]
    if len(a) == len(b):
        i = max(len(a), len(b)) - 1
        while a[i] == b[i]:
            i -= 1
            if i == -1:
                return 0
        else:
            if a[i] > b[i]:
                return 1
            else:
                return -1
    elif len(a) > len(b):
        return 1
    else:
        return -1


def LongShiftDigitsToHigh(n, l):
    for i in range(l):
        n.insert(0, 0)
    return n


def LongShiftDigitsToLow(n, amount):
    if len(n) - amount <= 0:
        return [0]
    i = amount - 1
    while i > -1:
        del n[i]
        i -= 1
    return n


def LongShiftBitsToHigh(number, width_shift):
    if width_shift <= 0 or number == [0]:
        return number.copy()
    remainder = width_shift % 32
    width_shift //= 32
    result = LongShiftDigitsToHigh(number.copy(), width_shift)
    if remainder > 0:
        for i in range(remainder):
            last_bit = (result[-1] >> 31) & 1
            for j in range(len(result) - 1, 0, -1):
                result[j] = ((result[j] << 1) ^ ((result[j - 1] >> 31) & 1)) & 0xFFFFFFFF
            result[0] = (result[0] << 1) & 0xFFFFFFFF
            if last_bit != 0:
                result.append(last_bit)
    while len(result) > 1 and result[-1] == 0:
        result.pop()
    return result


def LongShiftBitsToLow(n, amount):
    if amount // 32 >= len(n):
        return convert_from_hex('0')
    if amount % 32 == 0:
        return LongShiftDigitsToLow(n, amount // 32)
    b = 32 - amount % 32
    k = 0 if n[len(n) - 1] >> 32 - b != 0 else 1
    result = [0] * (len(n) - k - amount // 32)
    if k == 0:
        result[len(n) - 1] = n[len(n) - 1] >> 32 - b
        i = len(result) - 2
    else:
        i = len(result) - 1
    for j in reversed(range(amount // 32 + 1, len(n))):
        result[i] = (n[j] << b) & (2 ** 32 - 1) | n[j - 1] >> 32 - b
        i -= 1
    return result


def BitCheck(a, i):
    c = i % 32
    j = i // 32
    return (a[j] >> c) & 1


def BitLength(a):
    result = (len(a) - 1) * 32 + a[len(a) - 1].bit_length()
    return result


'''Lab--2'''


def GCD(a, b):
    divisor = [1]
    compare = 0
    col_vo_sub = 0
    while a[0] % 2 == 0 and b[0] % 2 == 0:
        a = LongShiftBitsToLow(a, 1)
        b = LongShiftBitsToLow(b, 1)
        divisor = LongShiftBitsToHigh(divisor, 1)
    while a[0] % 2 == 0:
        a = LongShiftBitsToLow(a, 1)
    while LongCompare(b, convert_from_hex('0')) != 0:
        compare += 1
        while b[0] % 2 == 0:
            b = LongShiftBitsToLow(b, 1)
        compare_of_number = LongCompare(a, b)
        compare += 1
        if compare_of_number == 1:
            min_ab = b
            sub = LongSubstration(a, b)
            col_vo_sub += 1
        elif compare_of_number == -1:
            min_ab = a
            sub = LongSubstration(b, a)
            col_vo_sub += 1
        else:
            min_ab = b
            sub = [0]
        a = min_ab
        b = sub
    divisor = LongMultiply(divisor, a)
    return divisor, compare, col_vo_sub

# print('НСД(A, B) = ' + convert_to_hex(GCD(A, B)[0]) + '; кількість порівнянь = ' + str(GCD(A, B)[1]) + '; кількість віднімань = ' + str(GCD(A, B)[2]))


def EvklidGCD(a, b):
    compare = 0
    div = 0
    while LongCompare(a, [0]) != 0 and LongCompare(b, [0]) != 0:
        compare_of_number = LongCompare(a, b)
        compare += 3
        if compare_of_number == 1:
            a = LongDivideModule(a, b)[1]
            div += 1
        elif compare_of_number == -1:
            b = LongDivideModule(b, a)[1]
            div += 1
        else:
            b = [0]
    res = LongAddition(a, b)
    return res, compare, div


# EvklidGCD(A, B)
# print('НСД(A, B) за алгоритмом Евкліда = ' + convert_to_hex(EvklidGCD(A, B)[0]) + '; кількість порівнянь = ' + str(EvklidGCD(A, B)[1]) + '; кількість ділень = ' + str(EvklidGCD(A, B)[2]))



def LCM(a, b):
    gcd = GCD(a, b)[0]
    multiply = LongMultiply(a, b)
    result = LongDivideModule(multiply, gcd)[0]
    return result


def BarrettReduction(a, mod, µ):
    if LongCompare(mod, a) == 1:
        return a
    k = len(mod)
    if len(a) <= len(mod):
        return a
    q = LongDivideModule(a, LongShiftBitsToHigh([1], k-1))[0]
    q = LongMultiply(q, µ)
    q = LongShiftBitsToLow(q, k + 1)
    r = LongSubstration(a, LongMultiply(q, mod))
    while LongCompare(r, mod) != -1:
        r = LongSubstration(r, mod)
    return r


def LongAdititonModule(a, b, mod):
    sum = LongAddition(a, b)
    result = LongDivideModule(sum, mod)[1]
    return result


def LongSubstractionModule(a, b, mod):
    if LongCompare(a, b) == -1:
        print("The second number is bigger! The result is B-A mod M")
        sub = LongSubstration(b, a)
    else:
        sub = LongSubstration(a, b)
    result = LongDivideModule(sub, mod)[1]
    return result


def LongMultiplyModule(a, b, mod):
    mul = LongMultiply(a, b)
    mul_mod = LongDivideModule(mul, mod)[1]
    return mul_mod


def LongSquareMod(a, mod):
    sq = LongMultiplyModule(a, a, mod)
    return sq


def LongModulePower(a, b, mod):
    pow = [1]
    k = len(mod)
    ß = LongShiftDigitsToHigh([1], 2 * k)
    µ = LongDivideModule(ß, mod)[0]
    for i in range(BitLength(b)):
        if BitCheck(b, i) == 1:
            pow = BarrettReduction(LongMultiply(pow, a), mod, µ)
        a = BarrettReduction(LongMultiply(a, a), mod, µ)
    return pow


# sum = convert_to_hex(LongAddition(A, B))
# sub = convert_to_hex(LongSubstration(A, B))
# mul = convert_to_hex(LongMultiply(A, B))

# divide = LongDivideModule(A, B)
# div = convert_to_hex(divide[0]) if divide[0] != [] else '0'
# div_mod = convert_to_hex(divide[1])

# square = convert_to_hex(LongSquare(A))
#pow = convert_to_hex(LongPower(A, B))

# print('The result of addition: ' + sum)
# print('The result of substraction: ' + sub)
# print('The result of multiplication: ' + mul)
# print('The result of dividing: ' + div)
# print('The result of reminder of dividing: ' + div_mod)
# print('The result of elevation to the square: ' + square)
#print('The result of elevation: ' + pow)

gcd = convert_to_hex(GCD(A, B)[0])
print('The result of finding gcd: ' + gcd)

lcm = convert_to_hex(LCM(A, B))
print('The result of finding lcm: ' + lcm)

mod_sum = convert_to_hex(LongAdititonModule(A, B, Module))
print('The result of (A+B)modModule: ' + mod_sum)

mod_sub = convert_to_hex(LongSubstractionModule(A, B, Module))
print('The result of (A-B)modModule: ' + mod_sub)

mod_mul__ = convert_to_hex(LongMultiplyModule(A, B, Module))
print('The result of (A*B)modModule: ' + mod_mul__)

mod_sq = convert_to_hex(LongSquareMod(A, Module))
print('The result of (A^2)modModule: ' + mod_sq)

# mod_pow = convert_to_hex(LongModulePower(A, B, Module))
# print('The result of (A^B)modModule: ' + mod_pow)

# print(LongCompare(LongMultiply(A, B), Module))


# divide = LongDivideModule(A, B)
# div = convert_to_hex(divide[0]) if divide[0] != [] else '0'
# div_mod = convert_to_hex(divide[1])
# print('The result of dividing: ' + div)
# print('The result of reminder of dividing: ' + div_mod)

# sub = convert_to_hex(LongSubstration(A, B))
# print('The result of substraction: ' + sub)