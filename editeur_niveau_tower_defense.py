#1 pour bloc noir
#2 pour blanc
#3 pour depart
#4 pour arrivée
#(et les touches au dessus du clavier, pas le pavé numérique)


import os
import pickle
import pygame
from pygame.locals import *

TAILLE_TILE = 32
TILES_HORIZONTAL = 10 #le nombre de tiles horizontaux de la map
TILES_VERTICAL = 10

pygame.init()

fenetre = pygame.display.set_mode((TAILLE_TILE * TILES_HORIZONTAL,
                                   TAILLE_TILE * TILES_VERTICAL))

#chargement des images
dico_textures = {"sol" : pygame.image.load("sprites_tower_defense/sol.png").convert(),
                 "mur" : pygame.image.load("sprites_tower_defense/mur.png").convert(),
                 "depart" : pygame.image.load("sprites_tower_defense/depart.png").convert(),
                 "arrivee" : pygame.image.load("sprites_tower_defense/arrivee.png").convert()}



fond = pygame.Surface(fenetre.get_size()).convert()
fond.fill((0, 0, 0))

fenetre.blit(fond, (0,0))
pygame.display.flip()

#création d'une liste de listes contenant les cases de notre futur niveau
structure_niveau = [[dico_textures["sol"] for i in range(TILES_HORIZONTAL)] for j in range(TILES_VERTICAL)]



def verifie_niveau(grille):
    "Vérifie que l'on peut aller du départ à l'arrivée en passant par un chemin"""
    
    for y1, colonne in enumerate(grille):
        for x1, case in enumerate(colonne):
            if case == dico_textures['depart']:
                x = x1
                y = y1
                case_depart = (x, y)#les coordonnéesdu depart
    cases_adjacentes = [(x, y+1), (x-1, y), (x+1, y), (x, y+1)]
    try:
        for x, y in cases_adjacentes:
            if grille[y][x] == dico_textures['sol']:
                case_actuelle = (x, y)#le sol à coté du départ, car il n'y en a qu'une
    except IndexError:
        pass
    
    while case_actuelle != dico_textures["arrivee"]:
        cases_testees = 0#si 4 cases testées et pas de cases, suivate, c'est un cul de sac
        for x, y in cases_adjacentes:
            if grille[y][x] != case_precedente and grille[y][x] == dico_textures['sol']:
                #case_suivante = case
                case_precedente = case_actuelle
                case_actuelle = grille[y][x]
            else:
                cases_testées += 1
                if cases_testees == 4:
                    return False
    return True
        
    
#_________________________________________________________________

bloc_selectionne = dico_textures['mur']

continuer = True

while continuer:
    for event in pygame.event.get():
        if event.type == QUIT:
            continuer = False
            
        if event.type == KEYDOWN:
            if event.key == K_s: #and verifie_niveau(structure_niveau):
                #on sauvegarde le niveau
                nom_map = input("Sous quel nom voulez-vous enregistrer cette carte? ")
                with open("maps_tower_defense/" + nom_map, 'wb') as fichier:
                    mon_pickler = pickle.Pickler(fichier)
                    mon_pickler.dump(structure_niveau)

                    
            elif event.key == K_1: #le 1 au dessus du A, pas le pavé numérique
                bloc_selectionne = dico_textures['mur']
            elif event.key == K_2:
                bloc_selectionne = dico_textures['sol']
            elif event.key == K_3:
                bloc_selectionne = dico_textures['depart']
            elif event.key == K_4:
                bloc_selectionne = dico_textures['arrivee']

        if event.type == MOUSEBUTTONDOWN:
            if event.button == 1: #au clic gauche, on blitte l'image
                case_x = event.pos[0] // TAILLE_TILE
                case_y = event.pos[1] // TAILLE_TILE
                #calcul de la position en pixel où l'objet sera affiché
                x = case_x * TAILLE_TILE
                y = case_y * TAILLE_TILE
                
                structure_niveau[case_y][case_x] = bloc_selectionne
                fenetre.blit(bloc_selectionne, (x,y))
        
        
            if event.button == 3:                
                case_x = event.pos[0] // TAILLE_TILE
                case_y = event.pos[1] // TAILLE_TILE
                #calcul de la position en pixel où l'objet sera affiché
                x = case_x * TAILLE_TILE
                y = case_y * TAILLE_TILE
                #on met un mur sur le bloc a effacer, ce qui revient au meme
                fenetre.blit(dico_textures['mur'], (x,y))
                pygame.display.flip()

                structure_niveau[case_y][case_x] = dico_textures['mur']
    

    pygame.display.flip()                

pygame.quit()
