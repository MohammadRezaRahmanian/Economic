import numpy as np
import pandas as pd
import os
import seaborn as sns
from function import fp,fA,Ap

os.system("cls")
cm = sns.light_palette("green", as_cmap=True)

Max_Year=100
i_star=0.035,0.1,0.08

for i in i_star:
    Table=pd.DataFrame([],index=range(1,Max_Year+1),columns=("F/P","P/F","A/F","F/A","A/P","P/A"))
    for n in range(1,Max_Year+1):
        Row=[]
        Row.append(fp(i,n,Method="f/p"))
        Row.append(fp(i,n,Method="p/f"))
        Row.append(fA(i,n,Method="A/f"))
        Row.append(fA(i,n,Method="f/A"))
        Row.append(Ap(i,n,Method="A/p"))
        Row.append(Ap(i,n,Method="p/A"))
        Row=np.round(Row,5)
        Table.loc[n,:]=Row
    Writer=pd.ExcelWriter(f"I={i}.xlsx")
    Table.to_excel(Writer)
    Writer.save()
