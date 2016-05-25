#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Version : Courir/Couleur/Non ordonne/Mode panique. Recupere une architecture sauvegardee. Affiche les differences avec l archietecture de base en rouge. Simulation visuelle."""

__author__ = "Mathis GERMA"
__version__ = "3-9.5.3"
__email__ = "germa.mathis@gmail.com"
__status__ = "Production"


from pylab import *

from tkinter import *
from random import *
from math import *

## Declarations

# Matrice
dimx=50
dimy=50
bords=4
densite=0.2 # Entre 0 et 1

#Types
Vide=0
Mur=1
Occupee=2
Sortie=3
Obstacle=5
tours=50
PM=False
sorties=[[1,25]] #Position des sorties. Possiblement plusieurs.

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


def opensave(ind):
    file=open('C:/Users/mathis/Documents/MP/TIPE/recherche/sauvegarde','r')
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

Archit=opensave('')
def ArchiParam(n,i,j):
        
        if (i-bords<0 or i+bords>dimy or j-bords<0 or j+bords>dimx or (j<dimy/2 and abs(i-dimx)<3) or j<6) and i!=25 and i!=24 and i!=26 and n==0:
            return(Mur) # 3 par 2
        elif Archit[j][i]==1 :return(Obstacle) #boule
        else : return(Vide)

def placage(Cellules, densite):
    n=0
    densite_actuelle=n/(dimx-2*bords)*(dimy-2*bords)
    while densite_actuelle<densite:
        aleai=randint(bords,dimx-bords+1)
        aleaj=randint(bords,dimy-bords+1)
        if (Cellules[0][aleai][aleaj]==Vide and (abs(sorties[0][0]-aleai)>7 or abs(sorties[0][1]-aleaj)>3)): # et pas dans la zone d'exclusion
            Cellules[0][aleai][aleaj]=str('#%02x%02x%02x' % (int(255*(abs(sorties[0][0]-aleai))/(dimx)),int(255*(abs(sorties[0][1]-aleaj))/(dimy)),100))
            n+=1
            densite_actuelle=n/((dimx-2*bords)*(dimy-2*bords)-6*7)
            print(densite_actuelle)
    return(True)
    
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

## Outils
def SC(cp1,cp2): # Sommes de couples
    return([cp1[0]+cp2[0],cp1[1]+cp2[1]])

## Mouvements
distance=[dimx,dimy]
ordre=[4,1,2,3,0]

##### Comportement ####
#### v29.01.16 ########
######### 1 ###########
##### 3 # 2 # 6 #######
# 4 # 5 #%%###########


def Comportement(n,x,y):
    if not PM:
        distance=[dimx,dimy]
        for couple in sorties:
            if abs(distance[0])**2+abs(distance[1])**2>abs(x-couple[0])**2+abs(y-couple[1])**2 :
                distance[0]=x-couple[0]
                distance[1]=y-couple[1]
        #Ordre des mouvements                             
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
                Cellules[n+1][x+deplacements[ordre[k]][0]][y+deplacements[ordre[k]][1]]=Cellules[n][x][y] # On occupe la nouvelle (qui peut etre identique)
        k+=1

def verif(n,x,y,traj):
    #traj=[[+-1,+-1]]
    verific=SC([x,y],traj)
    verific1=SC([x,y],[sign(traj[0]),sign(traj[1])])
    verific2=SC([x,y],[traj[0]+sign(traj[0]),traj[1]+sign(traj[1])]) # Si plus loin, il y a un obstacle, on y va pas. Si on cours,
    if verific!=[x,y] and (
    type(Cellules[n+1][verific[0]][verific[1]])==str or # quelqu'un au tours suivant
    type(Cellules[n][verific[0]][verific[1]])==str or # quelq'un maintenant
    Cellules[n][x+traj[0]][y+traj[1]] in (Mur,Obstacle) or # quelque chose la ou on veut aller
    Cellules[n][verific1[0]][verific1[1]] in (Mur, Obstacle) or # ou entre la et ou on veut aller
    Cellules[n][verific2[0]][verific2[1]]==Obstacle):
        return(False) # Si il y a quelque chose : C'est impossible
    return True


#### Partie graphique

global ite
ite=0

def damier(): #fonction dessinant le tableau
    global ite
    can1.delete(ALL)
    n=ite
    ligne_vert()
    ligne_hor()
    for i in range(dimx):
        for j in range(dimy):
            x=i*c
            y=j*c
            if Cellules[n][i][j]==Vide:
                can1.create_rectangle(x, y, x+c, y+c, fill='white')
            elif type(Cellules[n][i][j])==str:
                can1.create_rectangle(x, y, x+c, y+c, fill=Cellules[n][i][j])        
            elif Cellules[n][i][j]==Mur:
                can1.create_rectangle(x, y, x+c, y+c, fill='black')
            elif Cellules[n][i][j]==Sortie:
                can1.create_rectangle(x, y, x+c, y+c, fill='green')
            elif Cellules[n][i][j]==Obstacle:
                can1.create_rectangle(x, y, x+c, y+c, fill='red')
    
def ligne_vert():
    c_x = 0
    while c_x != larg:
        can1.create_line(c_x,0,c_x,hauteur,width=1,fill='black')
        c_x+=c
        
def ligne_hor():
    c_y = 0
    while c_y != hauteur:
        can1.create_line(0,c_y,larg,c_y,width=1,fill='black')
        c_y+=c

def click_gauche(event): #creer un occupant
    x = event.x -(event.x%c)
    y = event.y -(event.y%c)
    
    if type(Cellules[0][x//c][y//c])!=str:
        can1.create_rectangle(x, y, x+c, y+c, fill=str('#%02x%02x%02x' % (255,0,0)))
        Cellules[0][x//c][y//c]=str('#%02x%02x%02x' % (255,0,0))
    else:
        can1.create_rectangle(x, y, x+c, y+c, fill='white')
        Cellules[0][x//c][y//c]=Vide
    

def click_droit(event): #creer un mur
    x = event.x -(event.x%c)
    y = event.y -(event.y%c)
    print(x,y)
    if Cellules[0][x//c][y//c]!=Mur:
        can1.create_rectangle(x, y, x+c, y+c, fill='black')
        Cellules[0][x//c][y//c]=Mur
    else:
        can1.create_rectangle(x, y, x+c, y+c, fill='white')
        Cellules[0][x//c][y//c]=Vide
        

def go():
    sx=1
    sy=1
    #démarrage de l'animation
    # ######
    for instance in range(tours): # On lance le calcul	
        # Recherche de personne
        startx=randint(0,dimx) # Choix aleatoire a chaque tour le du debut de la recherche
        starty=randint(0,dimy)
        for x in range(dimx):
            for y in range(dimy):
                if type(Cellules[instance][(x+startx)%dimx][(y+starty)%dimy])==str :
                    Comportement(instance,(sx*x+startx)%dimx,(sy*y+starty)%dimy)
                elif type(Cellules[instance][(x+startx)%dimx][(y+starty)%dimy])!=str and Cellules[instance][((x+startx)%dimx)%dimx][(y+starty)%dimy]!=Vide :
                    Cellules[instance+1][(x+startx)%dimx][(y+starty)%dimy]=Cellules[instance][(x+startx)%dimx][(y+starty)%dimy]

    # ###########
    print('nbsorties=',nbsorties)
    global OK
    OK =1
    play()
        
def stop():
    "arrêt de l'animation"
    global OK    
    OK =0
    

    
def play(): #??
    global OK, vitesse, ite
    ite+=1
    damier()
    if OK!=0 and ite<tours:
        fen1.after(vitesse,play)


#les différentes variables:

echelle=30
# taille de la grille
hauteur = echelle*dimx
larg = echelle*dimy

#taille des cellules
c = echelle

vitesse=1 # Attente en ms entre chaque rafraichissement

OK=0

fen1 = Tk()

can1 = Canvas(fen1, width=larg, height=hauteur, bg ='white')
can1.bind("<Button-1>", click_gauche)
can1.bind("<Button-3>", click_droit)
can1.pack(side =TOP, padx =5, pady =5)

damier()

b1 = Button(fen1, text ='Départ', command =go)
b2 = Button(fen1, text ='Arrêt', command =stop)
b1.pack(side =LEFT, padx =3, pady =3)
b2.pack(side =LEFT, padx =3, pady =3)



fen1.mainloop()
