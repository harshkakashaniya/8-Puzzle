import argparse
import numpy as np
import os, sys
import math
import time

#------------------------------------------------------------------------------
#FUNCTIONS DEFINATION

# function to find zero in matrix
def findzero(matrix):
    for i in range(0,len(matrix)):
        for j in range(0,len(matrix)):
            if(matrix[i,j]==0):
                a=i
                b=j
    return a , b
# function to swipe element right with zero
def Swiperight(matrix_m):
    possible_R=0
    matrix=matrix_m.copy()
    #print(matrix,'m_right')
    zero_i,zero_j=findzero(matrix)
    if(zero_j<len(matrix)-1):
        matrix[zero_i,zero_j]=matrix[zero_i,zero_j+1]
        matrix[zero_i,zero_j+1]=0
        possible_R=1
        #print(matrix,'right')
    return matrix,matrix_m,possible_R
# function to swipe element left with zero
def Swipeleft(matrix_m):
    possible_L=0
    matrix=matrix_m.copy()
    zero_i,zero_j=findzero(matrix)
    if(zero_j>0):
        matrix[zero_i,zero_j]=matrix[zero_i,zero_j-1]
        matrix[zero_i,zero_j-1]=0
        possible_L=1
        #print(matrix,'left')
    return matrix,matrix_m,possible_L
# function to swipe element top with zero
def Swipetop(matrix_m):
    possible_T=0
    matrix=matrix_m.copy()
    zero_i,zero_j=findzero(matrix)
    if(zero_i>0):
        matrix[zero_i,zero_j]=matrix[zero_i-1,zero_j]
        matrix[zero_i-1,zero_j]=0
        possible_T=1
        #print(matrix,'top')
    return matrix,matrix_m,possible_T
# function to swipe element bottom with zero
def Swipebottom(matrix_m):
    possible_B=0
    matrix=matrix_m.copy()
    zero_i,zero_j=findzero(matrix)
    if(zero_i<len(matrix)-1):
        matrix[zero_i,zero_j]=matrix[zero_i+1,zero_j]
        matrix[zero_i+1,zero_j]=0
        possible_B=1
        #print(matrix,'bottom')
    return matrix,matrix_m,possible_B
# compare two mrtix
def search(A,B):
    for i in range(0,3):
        for j in range(0,3):
            if (A[i,j] != B[i,j]):
                return 0;
    return 1;
# function to find back tracking parents
def backtrack(Found,Nodeinfo):
    back_mat=[Found]
    while(Found!=0):
        Found=int(Nodeinfo[0,0,Found])
        #print(Found)
        back_mat=np.append([back_mat],[Found])
    return back_mat
# function returns matrix with final path
def backtrackmat(back_mat,Node):
    backtrackmat=np.zeros((3,3,len(back_mat)))
    for i in range(0,len(back_mat)):
        backtrackmat[:,:,i]=Node[:,:,back_mat[i]]
        #print(backtrackmat[:,:,i])
    return backtrackmat
# function returns instructions to follow to reach the output in numbers
def backtrackdirection(back_mat,Node):
    backtrackdirection=np.zeros((len(back_mat),1))
    for i in range(0,len(back_mat)):
        backtrackdirection[i,0]=Nodeinfo[0,3,back_mat[i]]
        #print(backtrackmat[:,:,i])
    return backtrackdirection
# function returns instructions to follow to reach the output in words
def directions(backtrackdirection):
    print('Steps to follow to reach desired position:')
    for i in range(0,len(backtrackdirection)):
        if (backtrackdirection[i,0]==2):
            print('Move DOWN')
        elif(backtrackdirection[i,0]==4):
            print('Move RIGHT')
        elif(backtrackdirection[i,0]==6):
            print('Move LEFT')
        elif(backtrackdirection[i,0]==8):
            print('Move UP')
        else:
            print('Reached')
# transform matrix for node printing
def matrixtransform9(Node):
    Iterations=Node.shape[2]
    Elements=Iterations
    for i in range(Iterations):
        if(Node[0,0,i]==0 and Node[1,0,i]==0):
            Elements=i
            break
    Print_Node=np.zeros((Elements,1,9))
    for i in range(0,Elements):
        c=0
        for x in range(0,3):
            for y in range(0,3):
                Print_Node[i,0,c]=Node[y,x,i].copy()
                c=c+1
    return Print_Node
# transform matrix for nodeinfo
def matrixtransform4(Nodeinfo):
    Iterations=Node.shape[2]
    Elements=Iterations
    for i in range(Iterations):
        if(Node[0,0,i]==0 and Node[1,0,i]==0):
            Elements=i-1
            break
    Print_Node_info=np.zeros((Elements,1,4))
    for i in range(Elements):
        c=0
        for y in range(0,4):
            Print_Node_info[i,0,c]=Nodeinfo[0,y,i].copy()
            #print(Print_Node_info[i,0,c])
            c=c+1
    return Print_Node_info
# removes matrix repeatation
def repeatation_avoidance(mat,mat_arr,value):
    repeat=0
    for i in range(value):
        search_para=mat_arr[:,:,i]
        #print(mat,'compairing mat')
        #print(search_para,'compairing head mat')
        if(search(mat,search_para)):
            repeat=1
            break
    return repeat
# search in straight array
def search9(A,B):
    result=0
    for i in range(A.shape[0]):
        A[i,0]!=B[i,0]
        result=1
    return result

#------------------------------------------------------------------------------
#INITIALIZATION

#user imput
print("Input unsolved puzzle matrix? in following manner [[A,B,C],[D,E,F],[G,H,I]]")
A=input('value of A \n')
B=input('value of B \n')
C=input('value of C \n')
D=input('value of D \n')
E=input('value of E \n')
F=input('value of F \n')
G=input('value of G \n')
H=input('value of H \n')
I=input('value of I \n')

try:
   a=int(A)
   b=int(B)
   c=int(C)
   d=int(D)
   e=int(E)
   f=int(F)
   g=int(G)
   h=int(H)
   i=int(I)
   Start=np.mat([[a,b,c],[d,e,f],[g,h,i]])
except ValueError:
     print('One or more inputs are not integers. So we take default matrix as:')
     Start=np.mat([[1,8,2],[0,4,3],[7,6,5]])

print(Start,'User Input matrix')
time.sleep(.5)
Goal=[[1,2,3],[4,5,6],[7,8,0]] # final goal matrix
Iterations=98144100 # 9!/2 are maximum ways to find all possible which is 181441
#Initialize node
Node=np.zeros((3,3,Iterations))
#Initialize nodeinfo
Nodeinfo=np.zeros((1,4,Iterations))
#First node will be zeroth which is goal node
Node[:,:,0]=Goal

Nodeinfo[:,:,0]=[0,0,0,0]
#child value
i=1
#Parent Value
j=0
#finding of node set to zero
success=0

while (i<Iterations-4 and success==0):
    #print(i,'th number of child')
    Current_parent=Node[:,:,j]
    Node[:,:,i],Current_parent,status_R=Swiperight(Current_parent)
    #Tentative_child=Node[:,:,i]
    #repeat=repeatation_avoidance(Node[:,:,i],Node,i)
    #print(repeat,'repeat')
    if (status_R==1):
        Nodeinfo[:,:,i]=[j,i,0,6]
        #print(Node[:,:,i])
        #print(Current_parent)
        if(search(Node[:,:,i],Start)):
            success=1
        i=i+1
    #print(i)
    Node[:,:,i],Current_parent,status_L=Swipeleft(Current_parent)
    #Tentative_child=Node[:,:,i]
    #repeat=repeatation_avoidance(Node[:,:,i],Node,i)
    #print(repeat,'repeat')
    if (status_L==1):
        Nodeinfo[:,:,i]=[j,i,0,4]
        #print(Node[:,:,i])
        #print(Current_parent)
        if(search(Node[:,:,i],Start)):
            success=1
        i=i+1
    #print(i)
    Node[:,:,i],Current_parent,status_T=Swipetop(Current_parent)
    #Tentative_child=Node[:,:,i]
    #repeat=repeatation_avoidance(Node[:,:,i],Node,i)
    #print(repeat,'repeat')
    if (status_T==1):
        Nodeinfo[:,:,i]=[j,i,0,2]
        #print(Node[:,:,i])
        #print(Current_parent)
        if(search(Node[:,:,i],Start)):
            success=1
        i=i+1
    #print(i)
    Node[:,:,i],Current_parent,status_B=Swipebottom(Current_parent)
    #Tentative_child=Node[:,:,i]
    #repeat=repeatation_avoidance(Node[:,:,i],Node,i)
    #print(repeat,'repeat')
    if (status_B==1):
        Nodeinfo[:,:,i]=[j,i,0,8]
        #print(Node[:,:,i])
        #print(Current_parent)
        if(search(Node[:,:,i],Start)):
            success=1
        i=i+1
    print(i)
    j=j+1

'''
length=Node.shape[2]
Node1=np.reshape(Node,[length,9,1])
Nodeinfo1=np.reshape(Nodeinfo,[length,4,1])
for i in range(length):
    Benchmark=Node1[i,:,:]
    for j in range (i,length):
        comp=Node1[j,:,:]
        if(search9(Benchmark,comp)):
            np.delete(Node,j)
            #print(Node)
            np.delete(Nodeinfo1,j)
print(Nodeinfo1)
'''
# search algorithm
for i in range (Iterations):
    if (search(Node[:,:,i],Start)):
        #print('Found at %d'%i)
        Found=i
        break
    else:
        Found=-1

# If we found the element
if(Found!=-1):
    Path=backtrack(Found,Nodeinfo)
    #print(Path)
    backtrackmat=backtrackmat(Path,Node)
    back_direction=backtrackdirection(Path,Node)
    directions(back_direction)


# If we are unable to found the element
else:
    backtrackmat=[]

#------------------------------------------------------------------------------
# Printing customized the text files
if (Found!=-1):
    # For node
    Print_Node=matrixtransform9(Node)
    with open('Nodes.txt', 'w') as file:

        for data_slice in Print_Node:

            np.savetxt(file, data_slice, fmt='%-2.0f')
    # For node info
    Print_Node_info=matrixtransform4(Nodeinfo)
    with open('NodeInfo.txt', 'w') as file:

        for data_slice in Print_Node_info:
            np.savetxt(file, data_slice, fmt='%-2.0f')
    # for node target
    Print_Target=matrixtransform9(backtrackmat)
    with open('nodePath.txt', 'w') as file:

        for data_slice in Print_Target:
            np.savetxt(file, data_slice, fmt='%-2.0f')
else:
    # if node not found blank
    # For node
    with open('Nodes.txt', 'w') as file:
        file.write('This configuration is not possible')
        X=[]
        np.savetxt(file,X,fmt='%-2.0f')
    # For node info
    with open('NodeInfo.txt', 'w') as file:
        file.write('This configuration is not possible')
        X=[]
        np.savetxt(file,X,fmt='%-2.0f')
    # for node target
    with open('nodePath.txt', 'w') as file:
        file.write('This configuration is not possible')
        X=[]
        np.savetxt(file,X,fmt='%-2.0f')


#------------------------------------------------------------------------------
