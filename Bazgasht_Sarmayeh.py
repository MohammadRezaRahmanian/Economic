import os
import sympy as syms
from function import Calucate_ROR, Calucate_ROR_Match , Calucate_ROR_Diffrent_Year

os.system("cls")
i_star=syms.symbols('i_star')

############################################################################################################
#            Example 8-11
# Present_Value= 150e3 , 210e3, 60e3
# Auto_Payment = -82e3 , -70e3 , 12e3
# L = 7.5e3 , 10e3 , 3e3
# Year = 25
# for i in range(3):
#     ROR = Calucate_ROR(Present_Value[i],Year,Auto_Payment[i],L[i],Method_ROR="A")
#     print(ROR * 100)
#############################################################################################################
#             Example 8-12
# P = 13e3 , 8e3
# A = 1.6e3 , 3.5e3
# L = 2e3 , 0
# Year = 5 , 10
# Data=Calucate_ROR_Diffrent_Year(P,Year,A,L,0.15)
# print(Data)

############################################################################################################
# #            Example 8-10
# Present_Value= 4e3 , 2e3 , 6e3 , 1e3 , 9e3
# Auto_Payment = 639 , 410 , 761 , 117 , 785
# L =  [ 0 for i in range(len(Present_Value))]
# Year = 20
# list_Name=Calucate_ROR_Match(Present_Value,Year,Auto_Payment,L,0.06)
# print(list_Name)
############################################################################################################
#            Example 8-11
# Present_Value= 150e3 , 210e3
# Auto_Payment = -82e3 , -70e3 
# L =  [ 7500 , 10.5e3 ]
# Year = 25
# list_Name=Calucate_ROR_Match(Present_Value,Year,Auto_Payment,L,0.15)
# print(list_Name)
############################################################################################################
#            Example 8-11
# Present_Value= 150e3 , 210e3
# Auto_Payment = -82e3 , -70e3 
# L =  [ 7500 , 10.5e3 ]
# Year = 25
# list_Name=Calucate_ROR_Match(Present_Value,Year,Auto_Payment,L,0.15,Method_ROR="A")
############################################################################################################
#            Example 8-8
# Present_Value= 2e3 , 4e3 , 5e3
# Auto_Payment = 410 , 639 , 700  
# L =  [ 0 for i in range(len(Present_Value)) ]
# Year = 20
# list_Name=Calucate_ROR_Match(Present_Value,Year,Auto_Payment,L,0.06)
############################################################################################################
# #            Example 8-9
# Present_Value= [2e3 , 4e3 , 5e3]
# Auto_Payment = [410 , 639 , 700 ]
# L =  [ 0 for i in range(len(Present_Value)) ]
# Year = 20
# MARR=0.06

# for i in range(len(Present_Value)):
#     ROR=Calucate_ROR(Present_Value[i],20,Auto_Payment[i],L[i])
#     print(ROR)
#     if ROR<MARR:
#         Present_Value.pop(i)
#         Auto_Payment.pop(i)
#         L.pop(i)
# list_Name=Calucate_ROR_Match(Present_Value,Year,Auto_Payment,L,MARR)
# print(list_Name)
############################################################################################################
#            Example Jozveh
# Present_Value= 130 , 70 , 11
# Auto_Payment = 107 , 201 , 35 
# L =  [ 55 , 30 , 0]
# Year = 20
# list_Name=Calucate_ROR_Match(Present_Value,Year,Auto_Payment,L,0.06)
# print(list_Name)


###             Example 8-16
P = 8e3 , 5e3 , 7e3 , 6e3 ,4e3
A = 920 , 510 , 820 , 640 , 400
L = [ 0 for i in range(len(P)) ]
N=50

for i in range(len(P)):
    print(Calucate_ROR(P[i],N,A[i],L[i]))

print(Calucate_ROR_Match(P,N,A,L,0))

for i in range(len(P)):
    for j in range(i+1,len(P)):
        print( i, j)
        Present_Value = P[i] , P[j]
        Auto_Payment = A[i],A[j]
        L = 0 , 0  
        print(Calucate_ROR_Match(Present_Value,N,Auto_Payment,L,0))