
def gauss_summe(n):
    if n < 0:
        raise ValueError("n kein negativ Wert")
    summe = 0
    for i in range(1, n + 1):
        summe += i
    return summe

def fakultät(n):
    if n < 0:
        raise ValueError("n kein negativ Wert")
    result = 1
    for i in range(1, n + 1):
        result *= i
    return result 

#ay ay ay