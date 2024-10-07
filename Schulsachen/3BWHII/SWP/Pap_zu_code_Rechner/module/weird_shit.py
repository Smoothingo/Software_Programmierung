
def fakultät(n):
    i = 1 
    prod = 1
    print
    if n == 0:
        return prod
    elif n <= 0:
        print("keine negativen zahlen")
    while i <= n:
        prod = prod * i
        i+= 1
        return prod
        
  

def gauss_summe(n):
    summe = 0
    for i in range(1, n + 1):
        summe += i
    return summe
