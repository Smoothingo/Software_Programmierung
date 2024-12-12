from terminal_handler.in_out import * 
import numpy as np

n= 10
# int_input()

curr = 2
while curr <= n:
    is_p = True
    d = 2
    while d <= np.sqrt(curr):
        if curr % d == 0:
            is_p = False
            break
        d = d + 1
    
    if is_p:
        print(curr)

    curr += 1

print("Programmende")

    
