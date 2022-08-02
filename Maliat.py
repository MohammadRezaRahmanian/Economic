import matplotlib.pyplot as plt
import numpy as np
import os 
import pandas as pd
from function import Main_CFAT,Calucate_D,fA,fp
import sympy as syms

os.system("cls")

# t=syms.symbols("t")
# Table=Main_CFAT(50000,0,20,0.4,GI=28000-1000*t,OC=9500+500*t,Method_D="DDB")

# Table_Depreciation=Calucate_D(P=82e3,L=5e3,N=20,Method="DDB")
# Writer=pd.ExcelWriter("Test.xlsx")
# Table.to_excel(Writer)
# Writer.save()

# Present_Value=8e+4
# L=1e+4
# Number_Of_Year=10

# Depreciation=Calucate_D(P=Present_Value,N=Number_Of_Year,L=L,Method="DB")
# print(Book_Value)
# print(Depreciation)

# print(sum(Table["PW-CFAT"]))


# Table=Calucate_D(80e3,10,10e3,Method="SF",Rate_Of_Return=0.1)
# Table=Calucate_D(138e3,11,28e3,Method="DDB")
# Table=Calucate_D(80e3,10,10e+3,Method="DB")
# Table=Calucate_D(P,N,L,Method="SOYD")
# Table=Calucate_D(80e3,10,10e3)
# Table=Calucate_D(82e3,7,5e3,Method="DDB")
# print(Table)
# plt.plot(range(11),Table.loc[:,"Last BV"])
# plt.plot(range(11),[28e3 for i in range(11)],color="green",linestyle="--")
# plt.plot(range(11),Table.loc[:,"BV"],color="black")
# plt.legend(["Last BV","L","BV"])
# plt.grid()
# plt.show()



# P=100e3
# Loan_Rate=0.1
# TR=0.09
# L=10e3
# n=5
# Method_D="DDB"
# ROR=0.2
# from sympy.abc import t
# Gi=-10*t+50e3
# OC=15*t+10000
# print(Main_CFAT(P,L,n,TR,Method_D=Method_D,GI=Gi,OC=OC,Start_Loan=0,Loan_Rate=0.1,Present_Loan=0.3*P,Method_Loan="Compound"))
