from function import AG, fp
import os
import pandas as pd
import numpy as np
from Replacement_Function import Number_Year_Economic

os.system("cls")

#          Example 13-1
Market_Value = 50000
N_Start=5
Number_Year=16
ROR=0.1
L = [ 40e3 , 35e3 , 30e3 , 25e3 , 20e3 , 20e3 , 20e3 , 20e3 , 20e3 , 20e3 , 20e3 ]
Auto_Payment_input = [ 1e3*i for i in range(Number_Year-N_Start)]
Auto_Payment=[]
for i in range(Number_Year-N_Start+1):
    if i != 0:
        x=AG(ROR,i,G=1000)
        Auto_Payment.append(x)
Table=Number_Year_Economic(Market_Value,Number_Year,ROR,Auto_Payment,N_Start,L=L)
Writer=pd.ExcelWriter("text.xlsx")
Table.to_excel(Writer)
Writer.save()
print(Table)

###             Exmple 13 - 2
# Market_Value = 13e3
# N_Start = 3
# Number_Year = 8
# ROR = 0.1
# L = [ 9000 , 8000 , 6000 , 2000 , 0 ]
# Auto_Payment_input = np.array([ 2500 , 2700 , 3000 , 3500 , 4500])
# Auto_Payment=[]
# for i in range(1,Number_Year-N_Start+1):
#     x=fp(ROR,i,f=Auto_Payment_input[i-1],Method="p/f")
#     if i != 1:
#         Auto_Payment.append(x+Auto_Payment[-1])
#     else:
#         Auto_Payment.append(x)
# Table=Number_Year_Economic(Market_Value,Number_Year,ROR,Auto_Payment,N_Start,L=L)
# Writer=pd.ExcelWriter("text.xlsx")
# Table.to_excel(Writer)
# print(Table)
# Writer.save() 