#!/usr/bin/env python
import numpy as np

N = 1
NS = 720
L = 115

# N = float(input("The Number of Turns : "))
# NS = int(input("The No. of sample points per Rotation : "))
# L = float(input("The length of Lead in mm : "))

x = np.linspace(0, L, 720)
c = np.linspace(0, 450, 720)

with open('5axisDrill.GCD','w') as file:
    file.write("G90\n")
    file.write("G01\n")
    for _ in range(N * NS):
        file.write("G01 ")
        file.write("X")
        file.write(format(x[_],".4f"))  
        file.write(" C")
        file.write(format(c[_],".4f"))
        file.write("\n")