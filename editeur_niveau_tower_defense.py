import os
import pickle
import pygame
from pygame.locals import *

taille_sprite = 32
TILES_HORIZONTAL = 10 #le nombre de tiles horizontaux de la map
TILES_VERTICAL = 10

pygame.init()

fenetre = pygame.display.set_mode((taille_sprite * ,408))

#chargement des images
ancien_chemin = os.getcwd()
os.chdir(ancien_chemin + "\\sprites_tower_defense")

dico_textures = {"sol" : pygame.image.load("sol.png").convert(),
                 "mur" : pygame.image.load("mur.png").convert(),
                 "depart" : pygame.image.load("depart.png").convert(),
                 "arrivee" : pygame.image.load("arrivee.png").convert()}


L_sprites = [caisse, mur, objectif, sprite_blanc]


fond = pygame.Surface((408,408)).convert()
fond.fill((255, 255, 255))

fenetre.blit(fond, (0,0))
pygame.display.flip()

#création d'une liste de listes contenant les cases de notre futur niveau
structure_niveau = []

i = 0
a = 0
for i in range(12):
    ligne_niveau = []
    for a in range(12):
        ligne_niveau.append('0')
    structure_niveau.append(ligne_niveau)
    
#_________________________________________________________________

bloc_selectionne = mur

continuer = True

while continuer == True:
    for event in pygame.event.get():
        if event.type == QUIT:
            continuer = False
            
        if event.type == KEYDOWN:
            if event.key == K_s:
                #on sauvegarde le niveau
                os.chdir("C:/Python32/Adrien/niveaux_mario_sokoban")
                with open('n2', 'wb') as fichier:
                    mon_pickler = pickle.Pickler(fichier)
                    mon_pickler.dump(structure_niveau)

                print(structure_niveau)
                    
            elif event.key == K_1:
                bloc_selectionne = mur
            elif event.key == K_2:
                bloc_selectionne = caisse
            elif event.key == K_3:
                bloc_selectionne = objectif

        if event.type == MOUSEBUTTONDOWN:
            if event.button == 1:
                case_x = event.pos[0] // taille_sprite
                case_y = event.pos[1] // taille_sprite
                #calcul de la position en pixel où l'objet sera affiché
                x = case_x * taille_sprite
                y = case_y * taille_sprite
                
                fenetre.blit(bloc_selectionne, (x,y))
                pygame.display.flip()

                if bloc_selectionne == mur:
                    del structure_niveau[case_y][case_x]
                    structure_niveau[case_y].insert(case_x, 'm')
        
                if bloc_selectionne == caisse:
                    del structure_niveau[case_y][case_x]
                    structure_niveau[case_y].insert(case_x, 'c')
        
                if bloc_selectionne == objectif:
                    del structure_niveau[case_y][case_x]
                    structure_niveau[case_y].insert(case_x, 'o')
        
            if event.button == 3:                
                case_x = event.pos[0] // taille_sprite
                case_y = event.pos[1] // taille_sprite
                #calcul de la position en pixel où l'objet sera affiché
                x = case_x * taille_sprite
                y = case_y * taille_sprite
                #on met un bloc blanc sur le bloc a effacer, ce qui revient au
                #meme, et ensuite on remplace par un 0 dans structure_niveau
                fenetre.blit(sprite_blanc, (x,y))
                pygame.display.flip()

                del structure_niveau[case_y][case_x]
                structure_niveau[case_y].insert(case_x, '0')

                
pygame.quit()


os.chdir(ancien_chemin)








