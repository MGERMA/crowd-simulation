# coding: utf8

# Tipe MP 2016 #
# Capdevila - Germa #
# Version 3-27.09.15#


from __future__ import unicode_literals


import sys as Sys

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
    
        if (i-bords<0 or i+bords>dimy or j-bords<0 or j+bords>dimx or (j<dimy/2 and abs(i-dimx)<3) or j<6) and i!=25 and i!=24 and i!=26 and n==0 and not (abs(sorties[0][0]+7-j)<4 and abs(sorties[0][1]-i)<5):
            return(Mur) # 3 par 2
        if (abs(sorties[0][0]+7-j)<4 and abs(sorties[0][1]-i)<5) and n==0 and randint(0,3)==0 :
            return(Mur) # 3 par 2

        else : return(Vide)


def placage(densite):
    n=0
    densite_actuelle=0
    global Cellules
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
                    nbsorties=nbsorties+1
            else :
                Cellules[n+1][x][y]=Vide # On vide l'ancienne case
                Cellules[n+1][x+deplacements[ordre[k]][0]][y+deplacements[ordre[k]][1]]=Occupee # On occupe la nouvelle (qui peut etre identique)
        k+=1

def verif(n,x,y,traj):
    #traj=[[+-1,+-1]]
    verific=SC([x,y],traj)
    verific1=SC([x,y],[sign(traj[0]),sign(traj[1])])
    verific2=SC([x,y],[traj[0]+sign(traj[0]),traj[1]+sign(traj[1])]) # Si plus loin, il y a un mur, on y va pas. Si on cours,
    # alors on ne sera pas pousse par ceux de derriere, alors on peut eviter l obstacle de plus loin
    if verific!=[x,y] and (Cellules[n+1][verific[0]][verific[1]]==Occupee or Cellules[n][verific[0]]
    [verific[1]]==Occupee or Cellules[n][x+traj[0]][y+traj[1]]==Mur or Cellules[n][verific1[0]][verific1[1]]==Mur or Cellules[n][verific2[0]][verific2[1]]==Mur) : return(False) # Si il y a quelque chose : C'est impossible
    return True
global ite
ite=0

global Cellules

def defcell(densite,boule):
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
    placage(densite)
    return Cellules

def value(Cellulles):
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
    return(nbsorties)


def barreprogression(ite,tot):
    long=100
    decimales=2
    longcomplet = int(round(long*ite/float(tot)))
    percents=round(100.0 * ite/float(tot),decimales)
    prefix='Progression : '
    suffix=' Terminé'
    bar= '#' * longcomplet + '-'*(long-longcomplet)
    Sys.stdout.write('%s [%s] %s%s %s\r' % (prefix, bar, percents, '%', suffix)),
    Sys.stdout.flush()
    if ite==tot:
        print('\n')




def opensave(ind):# Verifiee. ok  saufe [-1][-1] np
    file=open('recherche/sauvegarde','r')
    Arch=file.read()
    file.close()
    Architec=[[0 for i in range(dimy)]for j in range(dimx)]
    Arch2=Arch.split('[')
    for indice in range(2,len(Arch2)):
        obj=Arch2[indice].split(',')		
        for ind2 in range(0,len(obj)-1):
            i=0
            while obj[ind2][i]==' ':
                i+=1
            Architec[indice-2][ind2]=int(obj[ind2][i])
    return(Architec)

densite=0.3

def value2(Archit):
    #init
    ite=0
    global Cellules
    global nbsorties
    nbsorties=0
    Cellules=[Archit for k in range(tours+1)]
    placage(densite)
    
    for instance in range(tours): # On lance le calcul
        # Recherche de personne
        startx=randint(0,dimx) # Choix aleatoire a chaque tour du debut de la recherche
        starty=randint(0,dimy)
        for x in range(dimx):
            for y in range(dimy):
                if Cellules[instance][(x+startx)%dimx][(y+starty)%dimy]==Occupee :
                    Comportement(instance,(x+startx)%dimx,(y+starty)%dimy)
                elif Cellules[instance][(x+startx)%dimx][(y+starty)%dimy]!=Occupee and Cellules[instance][((x+startx)%dimx)%dimx][(y+starty)%dimy]!=Vide :
                    Cellules[instance+1][(x+startx)%dimx][(y+starty)%dimy]=Cellules[instance][(x+startx)%dimx][(y+starty)%dimy]

    # ###########
    return(nbsorties)


def sauvegarde(cellule):
        chemin='recherche/sauvegarde'
        sauvegarde=open(chemin,'w')
        if type(cellule[0][0])!=list:
            sauvegarde.write(str(cellule))
        else:
            sauvegarde.write(str(cellule[0]))
        sauvegarde.close()

T=1000
new=input('Nouveau aletatoire ou charger architecture ? 0 aleat / ind != 0 pour charger ind')
if new==0:
    defcell(0.3,0)
else :
    value2(opensave(''))
def resetsave():
    for i in range(len(Cellules[0])) :
        for j in range(len(Cellules[0][i])):    
            Cellules[0][i][j]=int(Cellules[0][i][j]==1)+3*int(Cellules[0][i][j]==3)
    sauvegarde(Cellules)
resetsave()

perc=0.01
 # Pour barre progres
T1=T
k=0
while T1>=1:
    T1=T1-T1*perc
    k+=1
iprog=0
# Fin barre progres
while T>=1:
    i=randint(5,11)
    j=randint(20,30)
    Archirecuit=opensave('')
    Archirecuit[i][j]=1-Archirecuit[i][j]
    a=value2(opensave(''))
    resetsave()
    de=value2(Archirecuit)-a
    resetsave()
    if de>5 :
        sauvegarde(Archirecuit)
    elif rand()<exp(de-5/T):
        sauvegarde(Archirecuit)
    T=T-T*perc
    iprog+=1
    barreprogression(iprog,k)

