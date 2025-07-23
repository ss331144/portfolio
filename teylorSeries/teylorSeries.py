# -*- coding: utf-8 -*-
"""
Created on Tue Apr 16 12:19:07 2024

@author: Sahar
"""

import math 
import numpy 
from sympy import Subs , diff , solve , sin , cos , tan , exp , symbols , pi ,log , Eq , sympify , atan
from sympy import acot , asin , acos ,sec , integrate , cosh , sinh 


x=symbols('x')

def getDiffN(curDiff , function):

    f = function
    for i in range (curDiff):
        f = diff(f)
    f = f.subs(x , 0)
    
    
    return f
def calcVal(teylorSeries,val):

    teylorSeries = sympify( teylorSeries )
    teylorSeries = teylorSeries.subs(x,val)
    return teylorSeries


def showTheSeries(string):
    copyString = string
    #string = string.split("^")
    st_x = ""
    st_without_space=""
    for i in range (len(string)):
        myIndex = string[i]
        st_x += myIndex
        '''if (myIndex[0]=="-"):
            st_x += myIndex
        else:
            st_x += "+"+myIndex'''
        st_x+="\n"
    #print(f'st_without_space :\n{st_without_space}\n')
    for i in range (len(string)) :
        copyString[i] = str(copyString[i]).replace("x**","power(x,")
        copyString[i] = str(copyString[i]).replace(")+","))+")
        st_without_space += str (copyString[i])
        
        
    #print(st_without_space)
    return st_x
            
def main(limit,function , calcValue ):
    string = ""
    cons_ = []
    for i in range (limit):
        a = getDiffN(i, function)
        cons_.append( eval(str(a/math.factorial(i)))      )
        if(a!=0):
            string += "+ (("+str(a)+")"+ "/" + str(math.factorial(i)) + ")*(x**"+str(i)+")+0^"
    
    string = string[:-1]
    #string = string.strip("^")
    m=0
    string = string.split("^")
    for i in string:
        m += calcVal(i, calcValue)
    value = m
    
    print(f'value = {value}')
    print(f'value = {round(value,50)}')
    
    str_res =  showTheSeries(string)
    print(f'taylor series of {function} until limit={limit-1} =\n{str_res}')
    v= getIntegralWithBond(0 , pi, str_res)
    print(f'your value of bonds : {v}\n')
    print(f'my cons function list :\n{cons_}\n\n')
    print()
    return 
def getIntegralWithBond(a,b , function):
    integral = integrate(function)
    valA = integral.subs(x,a)
    valB = integral.subs(x,b)
    return f'integral bodes {a}-{b} = {round(valB-valA,10)}'
myFun = 1+x**2*sin(x)
val = 1
main(20, myFun , val)
real_v = myFun.subs(x,val)
print(f'real value :{real_v}')
print(f'real value :{round(real_v,50)}')

        

