import os
import numpy as np
import pandas as pd
from function import Calucate_D, fA,fp,Ap,AG,Main_CFAT

os.system("cls")

def replacement(i_star,Year,L,OC,Start_Replacement,**kwarg):
    if "Present_Value" in kwarg:
        Present_Value=kwarg["Present_Value"]
    elif type(L)==list:
        Present_Value=L[0]
    if type(L)==list:
        Column_1=[Ap(i_star,n-Start_Replacement,p=Present_Value,Method="A/p")
                -fA(i_star,n-Start_Replacement,f=L[n-Start_Replacement],Method="A/f") 
                    for n in range(Start_Replacement+1,Year+1)]
    elif type(L)==int:
        Column_1=(Ap(i_star,Year-Start_Replacement,p=Present_Value,Method="A/p")
                -fA(i_star,Year-Start_Replacement,f=L,Method="A/f")) 
    if OC[2]-OC[1]==OC[3]-OC[2]:
        Column_2=[AG(i_star,n-Start_Replacement,G=OC[2]-OC[1]) for n in range(Start_Replacement+1,Year+1)]
    else:
        Column_2=[]
        Column_2.append(OC[1])
        for i in range(2,Year-Start_Replacement):
            constant=AG(i_star,i,G=OC[i])
            Column_2.append(constant)
    columns="P*f(A/P,i%,n)-L*f(A/f,i%,n)","Operating Costs","EUAC"
    Table=pd.DataFrame([],index=range(Year-Start_Replacement),columns=columns)
    Table
    Table.loc[:,"P*f(A/P,i%,n)-L*f(A/f,i%,n)"]=Column_1
    Table.loc[:,"Operating Costs"]=Column_2
    Table.loc[:,"EUAC"]=Table.loc[:,"Operating Costs"]+Table.loc[:,"P*f(A/P,i%,n)-L*f(A/f,i%,n)"]
    return Table

def Calucate_A(i_star,Year,Start_Replacement,OC):
    if type(OC)==list:
        Auto_Payment=[]
        for n in range(1,Year-Start_Replacement+1):
            if OC[1]-OC[2]==OC[2]-OC[3]:
                Auto_Payment.append(OC[0]+AG(i_star,n,G=OC[2]-OC[1]))
            else:
                Auto_Payment.append(0)
                for j in range(1,n+1):
                    Auto_Payment[-1]+=fp(i_star,j,f=OC[j],Method="p/f")
                Auto_Payment[-1]=Ap(i_star,n,p=Auto_Payment[-1])
    if type(OC) == int or type(OC)==float:
        Auto_Payment=OC 
    return Auto_Payment

def Replace(i_star,Year,L,OC,Start_Replacement,**kwarg):
    if "Present_Value" in kwarg:
        Present_Value=kwarg["Present_Value"]
    elif type(L)==list:
        Present_Value=L[0]
    Auto_Payment=Calucate_A(i_star,Year,Start_Replacement,OC)
    if type(OC) not in (list,tuple) and type(L) not in (list,tuple):
        Out_Put=(Ap(i_star,Year-Start_Replacement,p=Present_Value)+Auto_Payment-
                    fA(i_star,Year-Start_Replacement,f=L))
    elif type(OC) in (list,tuple) or type(L) in (list,tuple):
        columns="Value","A","EUAC"
        if type(L) not in (list,tuple):
            Value=[Ap(i_star,n-Start_Replacement,p=Present_Value,Method="A/p")
                -fA(i_star,n-Start_Replacement,f=L,Method="A/f") 
                    for n in range(Start_Replacement+1,Year+1)]
        else:
            Value=[Ap(i_star,n,p=Present_Value,Method="A/p")
                -fA(i_star,n,f=L[n],Method="A/f") for n in range(1,Year-Start_Replacement+1)]
        Table=pd.DataFrame([],index=range(Year-Start_Replacement),columns=columns)
        EUAC=np.array(Value)+np.array(Auto_Payment)
        Table.loc[:,"EUAC"]=EUAC
        Table.loc[:,"Value"]=Value
        Table.loc[:,"A"]=Auto_Payment
        Out_Put=Table
    return Out_Put

##############################################################################################
# i_star=0.12
# Present_Value=42000,0
# A=12000,25000
# L=8000,0
# Year=12
# Start_Replacement=2

# for i in range(2):
#     print(Replace(i_star,Year,L[i],A[i],Start_Replacement,Present_Value=Present_Value[i]))

###############################################################################################

# i_star=0.08
# Present_Value=1e5
# Start_Replacement=1
# Year=9
# L=0
# OC=[6000*n for n in range(Year-Start_Replacement)]
# Table=Replace(i_star,Year,L,OC,Start_Replacement,Present_Value=Present_Value)

# Writer=pd.ExcelWriter("Replacement.xlsx")
# Table.to_excel(Writer)
# Writer.save()

###############################################################################################

# Present_Value=2000,10500
# Method_D="Solid"
# OC=800,-1200
# L=0,2500
# Year=4
# i_star=0.1

# for i in range(2):
#     print(Replace(i_star,Year+1,L[i],OC[i],Start_Replacement=0,Present_Value=Present_Value[i]))

################################################################################################

# Present_Value=16000,10500
# P=16000,1200
# Method_D="Solid"
# OC=800,-1200
# L=0,2500
# Year=4,4
# i_star=0.08
# Tax_Rate=0.5
# Start_Replacement=2,0

# Type="Defender","Challenger"
# for i in range(2):
#     Table=Main_CFAT(Present_Value[i],L[i],Year[i],Tax_Rate,OC=OC[i],GI=0)
#     print(Table)

################################################################################################

#       Example 13-9

# Year=4
# L=[2500,1500,1000,500,0]
# OC=[8000+1000*n for n in range(Year+1)]
# i_star=0.12

# Table=Replace(i_star,Year,L,OC,0)
# print(Table)

# EUAC=Replace(i_star,7,1500,6000,0,Present_Value=16000)
# print("\n")
# print(EUAC)

################################################################################################

#            Jozveh

Year=10
L=0
Methdo_D="SOYD"
A=90e3,50e3
P_Prin=192500
Present_Value=37500,16500
Tax_Rate=0.4

Table_Defender=Main_CFAT(P_Prin,L,Year,Tax_Rate,Method_D=Methdo_D,GI=0,OC=A[0])
Table_Challanger=Main_CFAT(Present_Value[1],L,Year,Tax_Rate,Method_D=Methdo_D,GI=0,OC=A[1])
print(Table_Challanger)
