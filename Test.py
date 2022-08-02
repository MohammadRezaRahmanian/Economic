import numpy as np
import sympy as syms
from function import fp,Ap
from sympy.abc import i

list_Data = [ 0.01 , 0.02 , 0.03 , 0.04 , 0.05 , 0.06 , 0.07]
problem = -5000 + Ap(i,10,A=100,Method="p/A") + fp(i,10,f=7000,Method="p/f")

result_Data=[]
for Data in list_Data:
    
    result_Data.append(problem.subs({i:Data}))
    
    if len(result_Data)!=1:
        if result_Data[-1] < 0 and result_Data[-2] > 0:
            break


length = len(result_Data)
result_Data[-2] / (result_Data[-2]-result_Data[-1]) * (list_Data[length-1]-list_Data[length-2])