import os
import numpy as np
import pandas as pd
from function import fA,Ap

def Number_Year_Economic(Market_Vale,Number_Year,i_Star,Auto_Payment,N_Start=0,L=0):
    columns="P * f(A/P,i*,n) - L * f(A/F,i*,n)","A","EUAC"
    index=range(Number_Year-N_Start+1)
    Table=pd.DataFrame([],index=index,columns=columns)
    for i in range(1,Number_Year-N_Start+1):
        P = Ap(i_Star,i,p=Market_Vale)
        SV = fA(i_Star,i,f=L[i-1])
        Table.loc[i,"P * f(A/P,i*,n) - L * f(A/F,i*,n)"] = P - SV
        Table.loc[i,"A"]=Auto_Payment[i-1]
        Table.loc[i,"EUAC"]=Auto_Payment[i-1] + P - SV
    return Table

