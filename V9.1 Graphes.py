
# Tipe MP 2016 #
# Capdevila - Germa #
# Version 3-27.09.15#


from pylab import *
from tkinter import *
from random import *
from math import *

## Declatations

# Matrice
dimx=50
dimy=50
bords=4
#Types
Vide=0
Mur=1
Occupee=2
Sortie=3
tours=50
# # # # # # # # # # # # # Paniq mode #
PM=False
# # # # # # # # # # # # # 
sorties=[[1,25]] #Position des sorties
global nbsorties
nbsorties=0
mouvements=[
            [0,0],   #Ne pas bouger 0
            [0,1],   #Haut          1
            [1,0],   #Gauche        2
            [-1,0],  #Droite        3
            [0,-1],  #Bas           4
            ]

deplacements=[
            [0,0],   #Ne pas bouger 0
            [0,1],   #Haut          1
            [1,0],   #Gauche        2
            [-1,0],  #Droite        3
            [0,-1],  #Bas           4
            [0,2],   #courir haut          5
            [2,0],   #courir Gauche        6
            [-2,0],  #courir Droite        7
            [0,-2],  #courir Bas           8
            [1,1],   #Haut gauche          9
            [1,-1],  #Gauche bas           10
            [-1,1],  #Droite haut          11
            [-1,-1], #Droite bas           12
            ]


            

bords=3

def ArchiParam(n,i,j):
        
        if (i-bords<0 or i+bords>dimy or j-bords<0 or j+bords>dimx or (j<dimy/2 and abs(i-dimx)<3) or j<6) and i!=25 and i!=24 and i!=26 and n==0:
            return(Mur) # 3 par 2
        elif ((j-9)**2+(i-25)**2<boule):return(Mur) #boule
        else : return(Vide)


def placage(Cellules, densite):
    n=0
    densite_actuelle=0
    while densite_actuelle<densite:
        aleai=randint(bords,dimx-bords+1)
        aleaj=randint(bords,dimy-bords+1)
        if Cellules[0][aleai][aleaj]==Vide:
            Cellules[0][aleai][aleaj]=Occupee
            n+=1
            densite_actuelle=n/((dimx-bords)*(dimy-bords))
    return(True)
        
        
## Outils
def SC(cp1,cp2): # Sommes de couples
    return([cp1[0]+cp2[0],cp1[1]+cp2[1]])

## Mouvements
distance=[dimx,dimy]


##### Comportement ####
#### v29.01.16 ########
######### 1 ###########
##### 3 # 2 # 6 #######
# 4 # 5 #%%%###########


def Comportement(n,x,y):
    if not PM:
        distance=[dimx,dimy]
        for couple in sorties:
            if abs(distance[0])**2+abs(distance[1])**2>abs(x-couple[0])**2+abs(y-couple[1])**2 :
                distance[0]=x-couple[0]
                distance[1]=y-couple[1]
        #Ordre des mouvements                               ## a compacter. Place pour lisibilite
        if distance[0]>0 : # si vers la droite
            if abs(distance[0])>abs(distance[1]) : # -> Sortie est a droite et plus longue dist
                if distance[1]>=0 : ordre=[7,12,3,8,4,11,0,1,2] #Vers le bas ensuite
                else : ordre=[7,11,3,5,1,12,0,4,2]
            else :
                if distance[1]>=0 : ordre=[8,12,4,7,3,10,0,2,1]
                else : ordre=[5,11,1,7,3,9,0,2,4]
        else :
            if abs(distance[0])>abs(distance[1]) : # -> Sortie est a droite et plus longue dist
                if distance[1]>=0 : ordre=[6,10,2,8,4,9,0,1,3] #Vers le bas ensuite
                else : ordre=[6,9,2,5,1,10,0,4,3]
            else :
                if distance[1]>=0 : ordre=[8,10,4,6,2,12,0,3,1]
                else : ordre=[5,9,1,6,2,11,0,3,4]
         
      
    global nbsorties
    possibledeplacement=False
    k=0
    out=False
    while not possibledeplacement and k<len(ordre):
        if verif(n,x,y,deplacements[ordre[k]]) :
            possibledeplacement=True
            if Cellules[n+1][x+deplacements[ordre[k]][0]][y+deplacements[ordre[k]][1]]==Sortie:
                    out=True
                    nbsorties+=1
            else :
                Cellules[n+1][x][y]=Vide # On vide l'ancienne case
                Cellules[n+1][x+deplacements[ordre[k]][0]][y+deplacements[ordre[k]][1]]=Occupee # On occupe la nouvelle (qui peut etre identique)
        k+=1

def verif(n,x,y,traj):
    #traj=[[+-1,+-1]]
    verific=SC([x,y],traj)
    verific1=SC([x,y],[sign(traj[0]),sign(traj[1])])
    verific2=SC([x,y],[traj[0]+sign(traj[0]),traj[1]+sign(traj[1])]) # Si plus loin, il y a un mur, on y va pas. Si on cours,
    # alors on ne sera pas posse par ceux de derriere, alors on peut eviter l obstacle de plus loin
    if verific!=[x,y] and (Cellules[n+1][verific[0]][verific[1]]==Occupee or Cellules[n][verific[0]]
    [verific[1]]==Occupee or Cellules[n][x+traj[0]][y+traj[1]]==Mur or Cellules[n][verific1[0]][verific1[1]]==Mur or Cellules[n][verific2[0]][verific2[1]]==Mur) : return(False) # Si il y a quelque chose : C'est impossible
    return True
global ite
ite=0

global Cellules

def value(densite,boule):
    #init
    ite=0
    global Cellules
    global nbsorties
    nbsorties=0


        
    Cellules=[#n
                [#x
                    [ArchiParam(k,i,j) for i in range(dimy)]#y
                for j in range(dimx)]
            for k in range(tours+1)]
    for couple in sorties:
        for mouve in mouvements:
            Cellules[0][couple[0]+mouve[0]][couple[1]]=Sortie
            Cellules[0][couple[0]+mouve[0]][couple[1]+1]=Sortie
            Cellules[0][couple[0]+mouve[0]][couple[1]-1]=Sortie
    placage(Cellules, densite)
    
    




    for instance in range(tours): # On lance le calcul
        # Recherche de personne
        startx=randint(0,dimx) # Choix aleatoire a chaque tour le du debut de la recherche
        starty=randint(0,dimy)
        for x in range(dimx):
            for y in range(dimy):
                if Cellules[instance][(x+startx)%dimx][(y+starty)%dimy]==Occupee :
                    Comportement(instance,(x+startx)%dimx,(y+starty)%dimy)
                elif Cellules[instance][(x+startx)%dimx][(y+starty)%dimy]!=Occupee and Cellules[instance][((x+startx)%dimx)%dimx][(y+starty)%dimy]!=Vide :
                    Cellules[instance+1][(x+startx)%dimx][(y+starty)%dimy]=Cellules[instance][(x+startx)%dimx][(y+starty)%dimy]

    # ###########
    print('nbsorties=',nbsorties)
    return(nbsorties)
    global OK
    OK =1

import numpy as np
import matplotlib.pyplot as plt
nbtest=100
def moyenne(i,nbtest):
    sommemoy=0
    for k in range(nbtest):
        sommemoy+=value(i,boule)
    return(sommemoy/nbtest)
begin=0
finish=20
precision=160
x=[i/precision for i in range(begin,finish)]
y=[]
courb=[i for i in range(0,4)]
meilleur=0
for boule in courb:

    y=([moyenne(i/precision,nbtest) for i in range(begin,finish)])
    plt.plot(x,y)
    plt.legend(courb)
    som=0
    for add in y:som+=add
    if (meilleur<som):
        meilleur=som
        ymeilleur=max([coordy for coordy in y])
        i=0
        xmeilleur=0
        while xmeilleur==0:
            if y[i]==ymeilleur: xmeilleur=i/precision+begin/precision
            i+=1
        
plt.title("Courbes de tailles d obstacle")
ax = gca()


annotate(r'meilleur en moyenne',
         xy=(xmeilleur, ymeilleur), xycoords='data',
         xytext=(-260, -20), textcoords='offset points', fontsize=16,
         arrowprops=dict(arrowstyle="->", connectionstyle="arc3,rad=-.2"))
text(0.06, 20,nbtest, ha='center', va= 'bottom')
text(0.07, 20,"tests par points", ha='center', va= 'bottom')
text(0.075, 10,1/80, ha='center', va= 'bottom')
text(0.06, 10,"Résolution :", ha='center', va= 'bottom')


plt.ylabel('Sorties effectives')
plt.xlabel('Densite')
plt.show()