		
# Tipe MP 2016 #
# Capdevila - Germa #
# Version 3-27.09.15#


from pylab import *

from tkinter import *
from random import *
from math import *
    
def printarchi(ch):
    ## Declarations
    
    # Matrice
    dimx=50
    dimy=50
    bords=4
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
    
    densite=0.2 # Entre 0 et 10
    
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    #Types
    Vide=0
    Mur=1
    Occupee=2
    Sortie=3
    Obstacle=5
    tours=50
    # # # # # # # # # # # # # Paniq mode #
    PM=False
    # # # # # # # # # # # # # 
    sorties=[[1,25]] #Position des sorties
    global nbsorties
    nbsorties=0
    
    
    bords=3
        
    Cellules=[#n
                [#x
                    [0 for i in range(dimy)]#y
                for j in range(dimx)]
            for k in range(tours+1)]

    file=open(ch,'r')
    Arch=file.read()
    Arch2=Arch.split('[') # Fonction de conversion 01.04 qui marche !
    for indice in range(2,len(Arch2)):
        obj=Arch2[indice].split(',')
        for ind2 in range(0,len(obj)-1):
            i=0
            while obj[ind2][i]==' ':
                i+=1
            Cellules[0][indice-2][ind2]=int(obj[ind2][i])
    
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
        "démarrage de l'animation"
        # ######
        for instance in range(tours): # On lance le calcul
            # Recherche de personne
            startx=randint(0,dimx) # Choix aleatoire a chaque tour le du debut de la recherche
            starty=randint(0,dimy)
            for x in range(dimx):
                for y in range(dimy):
                    if type(Cellules[instance][(x+startx)%dimx][(y+starty)%dimy])==str :
                        Comportement(instance,(x+startx)%dimx,(y+starty)%dimy)
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
    
    #vitesse de l'animation (en réalité c'est l'attente entre chaque étapes en ms)
    vitesse=1
    
    OK=0
    
    
    #programme "principal" 
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