def fakultät(n):
    if n == 0:
        return 1
    produkt = 1
    for i in range(1, n + 1):
        produkt *= i
    return produkt

def gauss_summe(n):
    summe = 0
    for i in range(1, n + 1):
        summe += i
    return summe
