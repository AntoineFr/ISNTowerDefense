import os
import pygame
from pygame.locals import *
from time import time

pygame.init()

#A mettre dans un fichier constantes.py
LARGEUR_MENU = 100
TAILLE_TILE = 32 #les tuiles sont des carrés de 32 sur 32
TILES_HORIZONTAL = 10 #le nombre de tiles horizontaux de la map
TILES_VERTICAL = 10


grille = [
['depart','mur','mur','mur','mur','mur','mur','mur','mur','mur'],
['sol','mur','sol','sol','sol','sol','sol','sol','sol','arrivee'],
['sol','mur','sol','mur','mur','mur','mur','mur','mur','mur'],
['sol','mur','sol','mur','mur','mur','mur','mur','mur','mur'],
['sol','mur','sol','mur','mur','mur','mur','mur','mur','mur'],
['sol','mur','sol','mur','mur','mur','mur','mur','mur','mur'],
['sol','mur','sol','mur','mur','mur','mur','mur','mur','mur'],
['sol','mur','sol','sol','sol','sol','mur','mur','mur','mur'],
['sol','mur','mur','mur','mur','sol','mur','mur','mur','mur'],
['sol','sol','sol','sol','sol','sol','mur','mur','mur','mur']
]

#Ce dictionnaire regroupe les attributs variables en fonction des monstres, ie leurs caractéristiques
dico_monstres = {"Blob" : {"vie" : 1,
                          "vitesse" : 2, #1 case par seconde
                          "butin" : 10,
                          "xp" : 15,
                          "force" : 1}} #pts de vie perdus par le joueur si le mob passe l'arrivée

#Il faudra aussi faire un dico image pour les monstres car c'est pas possible là
                          
                          

class Monstre:
    def __init__(self, _x, _y, dico_monstres, nom):
        for attribut in dico_monstres[nom].keys():#chargement des attributs
            self.__dict__[attribut] = dico_monstres[nom][attribut]
            
        self.image = pygame.image.load("FaceBlob1.png").convert_alpha()
        self.intervalle = 0
        self.timer = time()
        self.direction = "haut"
        self.x = _x
        self.y = _y
        self.x_case = _x * TAILLE_TILE
        self.y_case = _y * TAILLE_TILE
        
        
    def deplacer(self, grille):
        # Recherche d'un chemin libre

        try: #On évite les erreurs dues à des indices trop grands
            if self.intervalle >= 1/self.vitesse:
                
                if grille[self.y_case - 1][self.x_case] == 'sol' and self.direction != "haut":# Vérifie en haut
                    self.y_case -= 1
                    self.direction = "bas"
                elif grille[self.y_case][self.x_case + 1] == 'sol' and self.direction != "droite":# Vérifie à droite
                    self.x_case += 1
                    self.direction = "gauche"
                elif grille[self.y_case + 1][self.x_case] == 'sol' and self.direction != "bas":# Vérifie en bas
                    self.y_case += 1
                    self.direction = "haut"
                elif grille[self.y_case][self.x_case - 1] == 'sol' and self.direction != "gauche":# Vérifie à gauche
                    self.x_case -= 1
                    self.direction = "droite"

                self.intervalle = 0
                self.timer = time()
            else:
                self.intervalle = time() - self.timer
        except IndexError:
            pass

        afficher_carte(fenetre, grille, dico_textures)
        self.actualiser_position()#on affiche le monstre à la bonne place
        
        

    def actualiser_position(self):
        self.x = self.x_case * TAILLE_TILE
        self.y = self.y_case * TAILLE_TILE
        fenetre.blit(self.image, (self.x, self.y))


fenetre = pygame.display.set_mode((TILES_HORIZONTAL * TAILLE_TILE + LARGEUR_MENU, TILES_VERTICAL * TAILLE_TILE))

ancien_chemin = os.getcwd()
os.chdir(os.getcwd() + "\\sprites_tower_defense")
dico_textures = {"sol" : pygame.image.load("sol.png").convert(),
                 "mur" : pygame.image.load("mur.png").convert(),
                 "depart" : pygame.image.load("depart.png").convert(),
                 "arrivee" : pygame.image.load("arrivee.png").convert()}



def afficher_carte(fenetre, grille, dico_textures): 
    for y, colonne in enumerate(grille):
        for x, case in enumerate(colonne):
            texture = dico_textures[case]#on récupère l'image correspondant à la case
            fenetre.blit(texture, (x * TAILLE_TILE, y * TAILLE_TILE))
        
afficher_carte(fenetre, grille, dico_textures)
monstre1 = Monstre(0, 0, dico_monstres, "Blob")

#BOUCLE INFINIE
continuer = True
while continuer:
    #pygame.time.Clock().tick(30)
    for event in pygame.event.get():
        if event.type == QUIT:
            continuer = False
            
    monstre1.deplacer(grille)
    pygame.display.flip()

pygame.quit()

os.chdir(ancien_chemin)
