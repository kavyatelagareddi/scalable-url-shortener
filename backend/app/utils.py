BASE62 = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"

def encode_base62(num):

    if num == 0:

        return BASE62[0]

    result = ""

    while num > 0:

        result = BASE62[num % 62] + result

        num //= 62

    return result