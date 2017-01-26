# -*- coding=utf-8 -*-
 
# TIPE Gordon -- Feu de forêt

from tkinter import *
from random import *
from math import floor, sqrt

fen = Tk()
fen.title("Feu de forêt")
h_cellule, w_cellule = 4, 4
canevas = Canvas(fen, height=h_cellule*71, width=w_cellule*71, bg='black')
canevas.pack()

def strength_wind(v):
    if v == 0: return 0
    elif v <= 25: return 1
    elif v <= 50: return 2
    else: return 3
    

def bernoulli(p):
    u = uniform(0,1)
    if u < 1-p:
        return 'g'
    else: return 'r'

    
def createmap(m,n, density):
    nb_filled = floor(m*n*density)
    trees = [[(choice([0]*(m*n - nb_filled) + ['g']*nb_filled), 1) for j in range(n)] for i in range(m)]
    return trees

            
trees = createmap(70,70,0.4)
trees[34][27] = 'r', 0.5


# propagation
def nextmap_(map_, i, j, vent, v):
    # the probability of the box in the wind direction is increased, or in contrary decreased
    h = strength_wind(v)
    
    if vent == 'NORD':
            c, p = map_[i+1][j]
            c2, p2 = map_[i-1][j]
            map_[i+1][j] = c, sqrt(p)
            map_[i-1][j] = c2, p2**(h+1)
            
    elif vent == 'SUD':
            c, p = map_[i-1][j]
            c2, p2 = map_[i+1][j]
            map_[i-1][j] = c, sqrt(p)
            map_[i+1][j] = c2, p2**(h+1)
            
    elif vent == 'EST':
            c, p = map_[i][j-1]
            c2, p2 = map_[i][j+1]
            map_[i][j-1] = c, sqrt(p)
            map_[i][j+1] = c2, p2**(h+1)
            
    elif vent == 'OUEST':
            c, p = map_[i][j+1]
            c2, p2 = map_[i][j-1]
            map_[i][j+1] = c, sqrt(p)
            map_[i][j-1] = c2, p2**(h+1)
            
    for m in range(-1,2):
        for n in range(-1,2):
            c, p = map_[i+m][j+n]
            if c == 'g' and (m,n) != (0,0):
                map_[i+m][j+n] = bernoulli(p), p
    map_[i][j] = 'grey', p
    return map_


# refresh map
def nextmap(vent, v):
    newmap = [i[:] for i in trees]
    for j in range(len(trees[0])-1):
        for i in range(len(trees)-1):
            c, p = trees[i][j]
            if c == 'r':
                nextmap_(newmap, i, j, vent, v)
    return newmap


# waiting for clic
def play(event):
    makemap()


# color map
def makemap():
    global trees
    canevas.delete(ALL)
    for j in range(len(trees[0])-1):
        for i in range(len(trees)-1):
            c, p = trees[i][j]
            if c == 'g':
                canevas.create_rectangle((j+1)*h_cellule, (i+1)*w_cellule,
                                         (j+2)*h_cellule,(i+2)*w_cellule, fill='green')
            elif c == 'r':
                canevas.create_rectangle((j+1)*h_cellule, (i+1)*w_cellule,
                                         (j+2)*h_cellule,(i+2)*w_cellule, fill='red')
            elif c == 'grey':
                canevas.create_rectangle((j+1)*h_cellule, (i+1)*w_cellule,
                                         (j+2)*h_cellule,(i+2)*w_cellule, fill='grey')
    trees = nextmap('EST', 110)
    fen.after(1, makemap) # refresh every 1 second


    
canevas.bind("<Button-1>", play)
fen.mainloop()
