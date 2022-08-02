import pandas as pd
import sympy as syms
import numpy as np
from sympy.abc import i

def fp(i_star,n,f=1,p=1,Method="f/p"):
    Constant=(1+i_star)**n
    if Method == "f/p":
        Out_Put=p*Constant
    elif Method =="p/f":
        Out_Put=f/Constant
    return Out_Put

def AG(i_star,Year,A=1,G=1,Method="A/G"):
    Parameter=1/i_star - Year/((1+i_star)**Year-1)
    if Method == "A/G":
        Out_Put=G*Parameter
    elif Method == "G/A":
        Out_Put=A/Parameter
    return Out_Put
    
def Ap(i_star,n,A=1,p=1,Method="A/p"):
    Constant=(i_star*(1+i_star)**n)/((1+i_star)**n-1)
    if Method == "A/p":
        Out_Put=p*Constant
    elif Method =="p/A":
        Out_Put=A/Constant
    return Out_Put

def fA(i_star,n,f=1,A=1,Method="A/f"):
    Constant=i_star/((1+i_star)**n-1)
    if Method == "A/f":
        Out_Put=f*Constant
    elif Method =="f/A":
        Out_Put=A/Constant
    return Out_Put

def PG(i_star,n,P=1,G=1,Method="P/G"):
    if Method == "P/G":
        A=AG(i_star,n,G=G)
        Out_Put= Ap(i_star,n,A=A,Method="p/A")
    elif Method == "G/P":
        A=Ap(i_star,n,p=G)
        Out_Put= AG(i_star,n,A=A,Method="G/A")
    return Out_Put

def Calculate_CFBT(**kwarg):
    if "Oc" in kwarg and "Gi" in kwarg:
        OC=kwarg["Oc"]
        GI=kwarg["Gi"]
        Out_Put=[]
        for i in range(len(GI)):
            Out_Put.append(GI[i]-OC[i])
    elif "CFAT" in kwarg:
        CFAT=kwarg["CFAT"]
        if "TX" in kwarg:
            TX=kwarg["TX"]
            Out_Put=CFAT-TX
        elif "TR" in kwarg and "D" in kwarg:
            TR=kwarg["TR"]
            D=kwarg["D"]
            Out_Put=(CFAT-D*TR)/(1-TR)
        else:
            print("You'r input is not enoufh")
            return None
    elif "IT" in kwarg and "D" in kwarg:
        D=kwarg["D"]
        IT=kwarg["IT"]
        Out_Put=IT+D
    else:
        print("You'r input is not enoufh")
    return np.matrix(Out_Put)

def Calucate_D(P,N,L,Method="Solid",**kwarg):
    Book_Value=np.matrix(np.zeros((1,N+1)))
    Depreciation=np.matrix(np.zeros((1,N+1)))
    Book_Value[0,0]=P
    Column=["D","BV"]
    if Method=="Solid":
        for i in range(1,N+1):
            Depreciation[0,i]=(P-L)/N
            Book_Value[0,i]=P-np.sum(Depreciation[0,:i+1])
    elif Method=="SOYD":
        SYD=N*(N+1)/2
        for M in range(1,N+1):
            Depreciation[0,M]=((N+1-M)/SYD)*(P-L)
            Book_Value[0,M]=P-np.sum(Depreciation[0,:M+1])
    elif Method=="DB" or Method == "DDB":
        if Method == "DB":
            d=1-(L/P)**(1/N)
        elif Method =="DDB":
            d=2/N
        for M in range(N+1):
            Book_Value[0,M]=P*(1-d)**M
            if M!=0:
                Depreciation[0,M]=d*Book_Value[0,M-1]
    elif Method == "SF":
        Rate_Of_Return=kwarg["Rate_Of_Return"]
        f=fA(Rate_Of_Return,N,f=P-L)
        for M in range(1,N+1):
            Depreciation[0,M]=fp(Rate_Of_Return,M-1,p=f)
            Book_Value[0,M]=P-Depreciation[0,M]
    if Book_Value[0,-1] < L:
        index=Book_Value<L
        Last_Book_Value=Book_Value.copy()
        Last_Depreciation=Depreciation.copy()
        Book_Value[index]=L
        index=np.argwhere(index==True)[0][1]
        Depreciation[0,index]=Book_Value[0,index-1]-L
        if index < N+1:
            Depreciation[0,index+1:]=0
        Column.extend(["Last D","Last BV"])
    elif Book_Value[0,N] > L:
        SL=np.matrix(np.zeros((1,N)))
        for j in range(0,N):
            SL[0,j]=(Book_Value[0,j]-L)/(N-j)
        index=np.argwhere(SL>Depreciation[0,1:])[:,1]
        for i in index:
            New_Book_Value=Book_Value.copy()
            New_Depreciation=Depreciation.copy()
            New_Depreciation[0,i+1:]=SL[0,i]
            for j in range(i+1,N+1):
                New_Book_Value[0,j]=P-np.sum(New_Depreciation[0,:j+1])
            if New_Book_Value[0,-1] == L:
                break
        Book_Value,Last_Book_Value=New_Book_Value,Book_Value
        Depreciation,Last_Depreciation=New_Depreciation,Depreciation
        Column.extend(["SL","Last D","Last BV"])
    Table=pd.DataFrame([],index=range(N+1),columns=Column)
    for i in range(N+1):
        Row=[]
        Row.append(Depreciation[0,i])
        Row.append(Book_Value[0,i])
        if i==0 and "SL" in Column:
            Row.append(0)
        elif "SL" in Column:
            Row.append(SL[0,i-1])
        if "Last D" in Column:
            Row.append(Last_Depreciation[0,i])
        if "Last BV" in Column:
            Row.append(Last_Book_Value[0,i])
        Table.loc[i,:]=Row
    return Table

def Calucate_GI(N,GI):
    Gross_Income=[]
    if type(GI) in (list,tuple):
        Gross_Income=GI
    elif type(GI)==float or type(GI)==int:
        Gross_Income=[GI for i in range(N+1)]
        Gross_Income[0]=0
    else:
        for i in range(N+1):
            if i==0:
                Gross_Income.append(0)
            else:
                Gross_Income.append(GI.subs({"t":i}))
    return np.array(Gross_Income,dtype=float).tolist()

def Calucate_OC(N,P,OC):
    Operating_Costs=[]
    if type(OC)== list:
        Operating_Costs=OC
    elif type(OC)==int or type(OC)==float:
        Operating_Costs=[OC for i in range(N+1)]
        Operating_Costs[0]=P
    else:
        for i in range(N+1):
            if i==0:
                Operating_Costs.append(P)
            else:
                Operating_Costs.append(OC.subs({"t":i}))
        Operating_Costs=np.array(Operating_Costs,dtype=float).tolist()
    return Operating_Costs

def Calucate_Loan(Present_Loan,Loan_rate,Year,Method="Simple",Start_Loan=0):
    I=np.matrix(np.zeros((1,Year+1)))
    PR=np.matrix(np.zeros((1,Year+1)))
    if Method == "Simple":
        I[0,Start_Loan+1:]=Loan_rate*Present_Loan
        PR[0,Start_Loan+1:]=Present_Loan/(Year-Start_Loan)
    elif Method == "Compound":
        Loan_installment=Ap(Loan_rate,Year-Start_Loan,p=Present_Loan)
        for i in range(Start_Loan+1,Year+1):
            I[0,i]=Loan_rate*(Present_Loan-np.sum(PR[0,Start_Loan+1:i]))
            PR[0,i]=Loan_installment-I[0,i]
    return I,PR

def Calucate_PW(Input,Number_Of_Year,L,Rate_Of_Return):
    Input=np.matrix(Input)
    PW=[]
    for i in range(Number_Of_Year+1):
        if i==0:
            PW.append(Input[0,i])
        else:
            PW.append(fp(Rate_Of_Return,i,f=Input[0,i],Method="p/f"))
        if i== Number_Of_Year:
            PW[i]+fp(Rate_Of_Return,i,f=L,Method="p/f")
    return PW

def Main_CFAT(P,L,N,Tax_Rate,**kwarg):
    """
    How To Use Main_CFAT:
        *arg Parameters:
            P : Present Value (float Or int Number)
            L : L (float Or int Number)
            N : Number Of Year (int Number)
            Tax_Rate : Tax Rate (float Number Between 0 to 1)
        **kwarg Parameters:
            Method_D : Choose Between ['Solid','SOYD','DB','DDB','SF'] If you do not enter, the program itself selects the method 'sloid'
            Method_Loan : "Simple","Compound" If you do not enter, the program itself selects the method 'Simple'
            Loan_Rate : Loan Rate(float Number Between 0 to 1)
            Present_Loan : Loan amount per year is zero (int or float Number)
            GI : Gross Income (List Or int Or float Or Sympy Module)
            OC : Operating Costs (List Or int Or float Or Sympy Module)
            Start_Loan : The Year That You Get Loan (int Number) 
    For Calucate Loan You Must Enter The Loan_Rate
                @ Created By : Mohammad Reza Rahmanian
    """
    if "OC" in kwarg and "GI" in kwarg:
        Columns=["GI","EX","CFBT","D","BV","TI","TX","CFAT"]
        Operating_Costs=kwarg["OC"]
        Gross_Income=kwarg["GI"]
        Operating_Costs=Calucate_OC(N,P,Operating_Costs)
        Gross_Income=Calucate_GI(N,Gross_Income)
        Cash_Flow_Before_Tax=Calculate_CFBT(Gi=Gross_Income,Oc=Operating_Costs)
        if "Method_D" in kwarg:
            Method_D=kwarg["Method_D"]
        else:
            Method_D="Solid"
        Table_Depreciation=Calucate_D(Method=Method_D,P=P,L=L,N=N)
        Loan=0
        if "Loan_Rate" in kwarg:
            if "Method_Loan" in kwarg:
                Method_Loan=kwarg["Method_Loan"]
            else:
                Method_Loan="Simple"
            if "Start_Loan" in kwarg:
                Start_Loan=kwarg["Start_Loan"]
            else:
                Start_Loan=0
            Present_Loan=kwarg["Present_Loan"]
            Loan_Rate=kwarg["Loan_Rate"]
            I,PR=Calucate_Loan(Present_Loan,Loan_Rate,N,Method=Method_Loan,Start_Loan=Start_Loan)
            Loan=I+PR
            Columns.insert(5,"I")
            Columns.insert(6,"PR")
            Cash_Flow_Before_Tax[0,Start_Loan]+=Present_Loan
            Gross_Income[Start_Loan]+=Present_Loan
        Taxable_Income=Cash_Flow_Before_Tax-Table_Depreciation.loc[:,"D"].to_numpy()
        if "Loan_Rate" in kwarg:
            Taxable_Income-=I
        Taxable_Income[0,0]=0
        Tax=Taxable_Income*Tax_Rate
        Tax=np.maximum(Tax,0)
        if "SL" in Table_Depreciation.columns:
            Columns.insert(6,"SL")
        list_not_in=[]
        for i in Table_Depreciation.columns:
            if i not in Columns:
                list_not_in.append(i)
                Columns.append(i)
        Cash_Flow_After_Tax=Cash_Flow_Before_Tax-Tax-Loan
        Table=pd.DataFrame([],index=range(N+1),columns=Columns)
        for year in range(N+1):
            Row=[]
            Row.append(Gross_Income[year])
            Row.append(Operating_Costs[year])
            Row.append(Cash_Flow_Before_Tax[0,year])
            Row.append(Table_Depreciation.loc[year,"D"])
            Row.append(Table_Depreciation.loc[year,"BV"])
            if "Loan_Rate" in kwarg:
                Row.append(I[0,year])
                Row.append(PR[0,year])
            Row.append(Taxable_Income[0,year])
            if "SL" in Table_Depreciation.columns:
                Row.append(Table_Depreciation.loc[year,"SL"])
            Row.append(Tax[0,year])
            Row.append(Cash_Flow_After_Tax[0,year])
            for i in list_not_in:
                Row.append(Table_Depreciation.loc[year,i])
            Table.loc[year,:]=Row
    return Table

def Calucate_ROR(Present_Value,Number_Of_Year,A,L,Method_ROR="P"):
    """
    Present_Value : Present Value (float Or int Number)
    L : L (float Or int Number)
    Number_Of_Year : Number Of Year (int Number)
    A : Auto Payment (int or float Number)
    Method_ROR : Choose Between (P,A)
    """
    if Method_ROR == "P":
        problem = -Present_Value + Ap(i,Number_Of_Year,A=A,Method="p/A") + fp(i,Number_Of_Year,f=L,Method="p/f")
    elif Method_ROR == "A" :
        problem = -Ap(i,Number_Of_Year,p=Present_Value) + A + fA(i,Number_Of_Year,f=L)
    return Calucate_Find_ROR(problem)

def Calucate_Find_ROR(Input):
    """
    Find ROR From Equation
    Like Example : -P * f(A/P,i*,n) + A + F * f(A/F,i*,n) --> Find i*
    """
    list_Data = [ 0.01 , 0.02 , 0.03 , 0.04 , 0.05 , 0.06 , 0.07 , 0.08 , 0.09 , 0.1 , 0.12,
                0.15 , 0.18 , 0.2 , 0.25 , 0.3 , 0.35 , 0.4 , 0.5 ]
    result_Data=[]
    for Data in list_Data:
        result_Data.append(Input.subs({i:Data}))
        if len(result_Data)!=1:
            if ( result_Data[-1] < 0 and result_Data[-2] > 0 ) or ( result_Data[-1] > 0 and result_Data[-2] < 0 ):
                break
    length = len(result_Data)
    x=result_Data[-2] / (result_Data[-2]-result_Data[-1]) * (list_Data[length-1]-list_Data[length-2])
    Out_Put = list_Data[length-2] + x
    return Out_Put

def Calucate_ROR_Diffrent_Year(Present_Value,Number_Of_Year,Auto_Payment,L,MARR,Method_ROR="A"):
    Index=np.argsort(Present_Value)
    list_Name=Index.tolist()
    dict_data={"Tartib":list_Name}
    if Method_ROR == "A":
        for h in Index:
            counter=Index.tolist().index(h)
            for j in Index[counter+1:]:
                EUAC_1 = Ap(i,Number_Of_Year[h],p=-Present_Value[h]) - Auto_Payment[h] + fA(i,Number_Of_Year[h],f=L[h])
                EUAC_2 = Ap(i,Number_Of_Year[j],p=-Present_Value[j]) - Auto_Payment[j] + fA(i,Number_Of_Year[j],f=L[j])
                EUAC = Calucate_Find_ROR(EUAC_2-EUAC_1)
                dict_data.__setitem__(f"{h}_{j}",EUAC)
                if EUAC>MARR:
                    list_Name.remove(h)
                    break
                else:
                    list_Name.remove(j)
                if len(list_Name)==1:
                    break
            if len(list_Name) == 1:
                break
    return dict_data

def Calucate_ROR_Match(Present_Value,Number_Of_Year,Auto_Payment,L,MARR,Method_ROR="P"):
    """
    Match Between 2 Or Higher Project
    Present_Value : Present Value ( list )
    L : L ( list )
    Number_Of_Year : Number Of Year (int)
    A : Auto Payment ( list )
    Method_ROR : Choose Between (P,A)
    """
    Index = np.argsort(Present_Value)
    list_Name=Index.tolist()
    dict_data={"Tartib":Index.tolist()}
    for i in Index:
        counter=Index.tolist().index(i)
        for j in Index[counter+1:]:
            P = Present_Value[j] - Present_Value[i]
            SV = L[j] - L[i]
            A = Auto_Payment[j] - Auto_Payment[i]
            ROR=Calucate_ROR(P,Number_Of_Year,A,SV,Method_ROR=Method_ROR)
            dict_data.__setitem__(f"{i}_{j}",
                                {"P":P,"L":SV,"A":A,"ROR":ROR})
            if ROR >= MARR:
                list_Name.remove(i)
                break
            else:
                list_Name.remove(j)
        if len(list_Name) == 1:
            dict_data.__setitem__("Winner:",list_Name[0])
            break
    return dict_data

def Benefit_Cost_Parameters(Present_value,ROR,Number_Year,Annual_Income=0,Annual_Loss=0,Annual_fee=0,Method="A"):
    if Method == "A":
        Out_Put=(Annual_Income-Annual_Loss)/(Ap(ROR,Number_Year,p=Present_value)+Annual_fee)
    elif Method == "P":
        Out_Put=(Annual_Income-Annual_Loss)/(Ap(ROR,Number_Year,p=Present_value)+Annual_fee)
    return Out_Put

def Benefit_Cost(Benefit,Cost,Disbenefit):
    return (Benefit-Disbenefit)/Cost

def Calucate_Benfit_Cost_Match(Present_value,ROR,Number_Year,L=0,Annual_Income=0,Annual_Loss=0,Annual_fee=0,Method="A"):
    """
    Present_Value : Present Value ( list )
    L : L ( list )
    Number_Of_Year : Number Of Year (int)
    A : Auto Payment ( list )
    Method_ROR : Choose Between (P,A)
    """
    Index = np.argsort(Present_value)
    list_Name=Index.tolist()
    dict_data={"Tartib":Index.tolist()}
    if Annual_fee == 0:
        Annual_fee = [0 for i in range(len(list_Name))]
    if Annual_Loss == 0:
        Annual_Loss = [0 for i in range(len(list_Name))]
    if Annual_Income == 0:
        Annual_Income = [0 for i in range(len(list_Name))]
    if L == 0:
        L = [0 for i in range(len(list_Name))]
    if type(Number_Year) == int:
        Number_Year = [Number_Year for i in range(len(list_Name))]
    for i in Index:
        counter=Index.tolist().index(i)
        for j in Index[counter+1:]:
            if Method == "A":
                Delta_B_1=Annual_Income[i] - Annual_fee[i]
                Delta_B_2=Annual_Income[j] - Annual_fee[j]
                Delta_B=Delta_B_2-Delta_B_1
                Delta_C_1=Ap(ROR,Number_Year[i],p=Present_value[i])-fA(ROR,Number_Year[i],f=L[i]) + Annual_Loss[i]
                Delta_C_2=Ap(ROR,Number_Year[j],p=Present_value[j])-fA(ROR,Number_Year[i],f=L[i]) + Annual_Loss[j]
                Delta_C = Delta_C_2 - Delta_C_1
            elif Method == "P":
                Delta_B_1=Ap(ROR,Number_Year[i],Annual_Income[i] - Annual_fee[i],Method="p/A")
                Delta_B_2=Ap(ROR,Number_Year[j],Annual_Income[j] - Annual_fee[j],Method="p/A")
                Delta_B=Delta_B_2-Delta_B_1
                Delta_C_1=Ap(ROR,Number_Year[i],p=Annual_Loss[i]) + Present_value[i]-fp(ROR,Number_Year,L[i],Method="p/f")
                Delta_C_2=Ap(ROR,Number_Year[j],p=Annual_Loss[j]) + Present_value[j]-fp(ROR,Number_Year,L[j],Method="p/f")
                Delta_C = Delta_C_2 - Delta_C_1
            B_C = Delta_B / Delta_C
            dict_data.__setitem__(f"{i}_{j}",(Delta_B,Delta_C,B_C))
            if B_C > 1:
                list_Name.remove(i)
                break
            else:
                list_Name.remove(j)
        if len(list_Name) == 1:
            dict_data.__setitem__("Winner:",list_Name[0])
            break
    return dict_data
