import numpy as np
import sympy as syms
import os 
import pandas as pd
from datetime import datetime

start=datetime.now()
os.system("cls")

t=syms.symbols("t")


def Calucate_GI_OC(GI,OC,N,P):
    Gi=[]
    Oc=[]
    for i in range(N+1):
        if i ==0 :
            Gi.append(0)
            Oc.append(P)
        else:
            Gi.append(GI.subs(t,i))
            Oc.append(OC.subs(t,i))
    return Gi,Oc

def Calucate_CFBT(GI,OC,N):
    return [ GI[i]-OC[i] for i in range(N+1) ]

def Calucate_D(P,N,L,Method="Solid"):
    if Method == "Solid":
        D=[]
        for i in range(N+1):
            if i==0:
                D.append(0)
            else:
                D.append((P-L)/N)
    return D
def Calucate_IT(CFBT,D):
    IT=[]
    for i in range(len(D)):
        if i==0:
            IT.append(0)
        else:
            IT.append(CFBT[i]-D[i])
    return IT

def Calucate_TX(N,TI,TR):
    return [max(TI[i]*TR,0) for i in range(N+1)]

def Calucate_CFAT(CFBT,TX,N):
    return [CFBT[i]-TX[i] for i in range(N+1)]





N=5
P=5e+4
L=0
GI=28e+3-1e+3*t
OC=9500+500*t
TR=0.4



GI,OC=Calucate_GI_OC(GI,OC,N,P)
CFBT=Calucate_CFBT(GI,OC,N)
D=Calucate_D(P=P,N=N,L=0)
TI=Calucate_IT(CFBT,D)
TX=Calucate_TX(N,TI,TR)
CFAT=Calucate_CFAT(CFBT,TX,N)
print("CFAT",CFAT)
print(datetime.now()-start)
print("D",D)
print("TI",TI)
print("TX",TX)
print("CFBT",CFBT)