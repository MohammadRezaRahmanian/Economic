from function import Calucate_Benfit_Cost_Match,Ap
import os

os.system("cls")

###### Example 9-1
P=1e6
Annual_Incom=150e3+100e3
Annual_Loss=30e3
Annual_fee=50e3
Marr=0.1
Year=20
print(Benefit_Cost_Parametr(P,Marr,Year,Annual_Incom,Annual_Loss,Annual_fee))

###### Example 9-2

# P=100e3,105e3
# ROR=0.07
# Year=5
# Annual_Incom=30e3,40e3-AG(ROR,Year,G=5000)
# print(Calucate_Benfit_Cost_Match(P,ROR,Year,Annual_Incom=Annual_Incom,Method="P"))

# # Example 9-4
# P=200e3,700e3
# Annual_Incom=95e3,120e3
# L=50e3,150e3
# Year=6,12
# ROR=0.1
# print(Calucate_Benfit_Cost_Match(P,ROR,Year,L=L,Annual_Incom=Annual_Incom,Method="A"))

## Example 9-5
P=4e3,2e3,6e3,1e3,9e3,10e3
Annual_Incom=639,410,761,117,785,Ap(0.06,20,p=9.5e3)
Year=20
ROR=0.06
x=Calucate_Benfit_Cost_Match(P,ROR,Year,Annual_Income=Annual_Incom,Method="P")
print(x)



