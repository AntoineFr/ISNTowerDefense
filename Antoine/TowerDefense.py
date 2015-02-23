import pygame
from pygame.locals import *
import threading

LARGEUR_MENU = 100
TAILLE_TILE = 32
TILES_HORIZONTAL = 10
TILES_VERTICAL = 10
# Directions : 0 -> Haut, 1 -> Droite, 2 -> Bas, 3 -> Gauche

grille = [
['d','m','m','m','m','m','m','m','m','m'],
['s','m','s','s','s','s','s','s','s','a'],
['s','m','s','m','m','m','m','m','m','m'],
['s','m','s','m','m','m','m','m','m','m'],
['s','m','s','m','m','m','m','m','m','m'],
['s','m','s','m','m','m','m','m','m','m'],
['s','m','s','m','m','m','m','m','m','m'],
['s','m','s','s','s','s','m','m','m','m'],
['s','m','m','m','m','s','m','m','m','m'],
['s','s','s','s','s','s','m','m','m','m']
]

def set_interval(func, sec):
    def func_wrapper():
        set_interval(func, sec)
        func()
    t = threading.Timer(sec, func_wrapper)
    t.start()
    return t

class Monstre:
    def __init__(self, _x, _y):
        self.vie = 0
        self.vitesse = 0.5
        self.direction = 0
        self.butin = 0
        self.xp = 0
        self.force = 0
        self.x = _x
        self.y = _y
        self.x_case = _x * TAILLE_TILE
        self.y_case = _y * TAILLE_TILE
        set_interval(self.deplacer, self.vitesse)

    def deplacer(self):
        # Recherche d'un chemin libre
        #if(grille[self.y_case - 1][self.x_case] == 'a' or grille[self.y_case + 1][self.x_case] == 'a'
        #or grille[self.y_case][self.x_case - 1] == 'a' or grille[self.y_case][self.x_case + 1] == 'a'):
            #print("Perdu !")
        if(grille[self.y_case - 1][self.x_case] == 's' and self.direction != 0):# Vérifie en haut
            self.y_case -= 1
            self.direction = 2
        elif(grille[self.y_case][self.x_case + 1] == 's' and self.direction != 1):# Vérifie à droite
            self.x_case += 1
            self.direction = 3
        elif(grille[self.y_case + 1][self.x_case] == 's' and self.direction != 2):# Vérifie en bas
            self.y_case += 1
            self.direction = 0
        elif(grille[self.y_case][self.x_case - 1] == 's' and self.direction != 3):# Vérifie à gauche
            self.x_case -= 1
            self.direction = 1

        self.actualiser_position()

    def actualiser_position(self):
        self.x = self.x_case * TAILLE_TILE
        self.y = self.y_case * TAILLE_TILE
        fenetre.blit(monstre, (self.x, self.y))
        pygame.display.flip()

pygame.init()
fenetre = pygame.display.set_mode((TILES_HORIZONTAL * TAILLE_TILE + LARGEUR_MENU, TILES_VERTICAL * TAILLE_TILE))
sol = pygame.image.load("s.png").convert()
mur = pygame.image.load("m.png").convert()
depart = pygame.image.load("d.png").convert()
arrivee = pygame.image.load("a.png").convert()
monstre = pygame.image.load("b.png").convert()

for y,colonne in enumerate(grille):
    for x,ligne in enumerate(colonne):
        if ligne == 'd':
            fenetre.blit(depart, (x * TAILLE_TILE, y * TAILLE_TILE))
        elif ligne == 'a':
            fenetre.blit(arrivee, (x * TAILLE_TILE, y * TAILLE_TILE))
        elif ligne == 's':
            fenetre.blit(sol, (x * TAILLE_TILE, y * TAILLE_TILE))
        elif ligne == 'm':
            fenetre.blit(mur, (x * TAILLE_TILE, y * TAILLE_TILE))

monstre1 = Monstre(0, 0)
#pygame.display.flip()

#BOUCLE INFINIE
continuer = 1
while continuer:
    for event in pygame.event.get():
        if event.type == QUIT:
            continuer = 0

pygame.quit()