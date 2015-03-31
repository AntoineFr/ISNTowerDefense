import os
import pygame
from pygame.locals import *
from time import time

#A mettre dans un fichier constantes.py
LARGEUR_MENU = 150
TAILLE_TILE = 32 #les tuiles sont des carrés de 32 sur 32
TILES_HORIZONTAL = 10 #le nombre de tiles horizontaux de la map
TILES_VERTICAL = 10

# Les informations sur la personne qui joue
joueur_score = 0
joueur_vie = 42
joueur_argent = 100

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
dico_monstres = {"Blob" : {"vie" : 2,
                          "vitesse" : 3, #2 cases par seconde
                          "butin" : 10,
                          "xp" : 15,
                          "force" : 1} #pts de vie perdus par le joueur si le mob passe l'arrivée
                 }

#Ce dictionnaire regroupe les attributs variables en fonction des tours, ie leurs caractéristiques
dico_tours = {"base" : {"cout" : 20,
                        "portee" : 100,
                        "cadence" : 1,
                        "degats" : 1,
                        "image_src" : "sprites_tower_defense/Tour1--0.png"
                        }
              }

liste_tours = []
liste_monstres = []

#Il faudra aussi faire un dico image pour les monstres car c'est pas possible là
                          
pygame.init()
fenetre = pygame.display.set_mode((TILES_HORIZONTAL * TAILLE_TILE + LARGEUR_MENU, TILES_VERTICAL * TAILLE_TILE))


class Monstre:
    def __init__(self, _x, _y, dico_monstres, nom):
        for attribut in dico_monstres[nom].keys():#chargement des attributs
            self.__dict__[attribut] = dico_monstres[nom][attribut]
            
        self.image = pygame.image.load("sprites_tower_defense/FaceBlob1.png").convert_alpha()
        self.intervalle = 0
        self.timer = time()
        self.direction = "haut"
        self.x_case = _x
        self.y_case = _y
        self.x = _x * TAILLE_TILE
        self.y = _y * TAILLE_TILE
        
    def sur_arrivee(self):
        return False
        
    def deplacer(self, grille):
        global joueur_vie
        # Recherche d'un chemin libre
        try: #On évite les erreurs dues à des indices trop grands
            if self.sur_arrivee():
                joueur_vie -= self.force
##            if self.x_case - 1 >= 0 and (grille[self.y_case - 1][self.x_case] == 'arrivee' or grille[self.y_case + 1][self.x_case] == 'arrivee' or \
##               grille[self.y_case][self.x_case - 1] == 'arrivee' or grille[self.y_case][self.x_case + 1] == 'arrivee'):
##                print("MORT")
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
        
    def afficher(self, fenetre):
        self.x = self.x_case * TAILLE_TILE
        self.y = self.y_case * TAILLE_TILE
        fenetre.blit(self.image, (self.x, self.y))


class Tour:
    def __init__(self, nom, _x, _y):
        self.intervalle = 0
        self.nom = nom
        self.timer = time()
        self.x_case = _x
        self.y_case = _y
        self.x = _x * TAILLE_TILE
        self.y = _y * TAILLE_TILE
        for attribut in dico_tours[nom].keys():
            self.__dict__[attribut] = dico_tours[nom][attribut]
            
        self.rect = pygame.Rect(self.x, self.y, 30, 30)
        self.image = pygame.image.load(self.image_src).convert_alpha()
        
    def tire(self, ennemi):
        global liste_tours
        """On tire si la distance tourelle/ennemi est inférieure à la portée
           et a une cadence donnée"""
        if (ennemi.x - self.x)**2 + (ennemi.y - self.y)**2 <= self.portee**2 \
           and self.intervalle >= 1/self.cadence and ennemi.vie - self.degats >= 0:
            ennemi.vie -= self.degats
            self.intervalle = 0
            self.timer = time()
            print(ennemi.vie)
            if ennemi.vie <= 0 and (ennemi in liste_tours):
                liste_tours.remove(ennemi)
        else:
            self.intervalle = time() - self.timer

    def afficher(self, fenetre):
        fenetre.blit(self.image, (self.x, self.y))

#ancien_chemin = os.getcwd()
#os.chdir(os.getcwd() + "\\sprites_tower_defense")
dico_textures = {"sol" : pygame.image.load("sprites_tower_defense/sol.png").convert(),
                 "mur" : pygame.image.load("sprites_tower_defense/mur.png").convert(),
                 "depart" : pygame.image.load("sprites_tower_defense/depart.png").convert(),
                 "arrivee" : pygame.image.load("sprites_tower_defense/arrivee.png").convert(),
                 "tour" : pygame.image.load("sprites_tower_defense/transparent.png").convert_alpha()
                 }



def afficher_carte(fenetre, grille, dico_textures, monstres, tours):
    global monstre1
    for y, colonne in enumerate(grille):
        for x, case in enumerate(colonne):
            texture = dico_textures[case]#on récupère l'image correspondant à la case
            fenetre.blit(texture, (x * TAILLE_TILE, y * TAILLE_TILE))
            
    for monstre in monstres:#dessin des monstres
        monstre.deplacer(grille)
        monstre.afficher(fenetre)
        
    for tour in tours:#dessin des tours
        tour.tire(monstre1)
        tour.afficher(fenetre)
        
monstre1 = Monstre(0, 0, dico_monstres, "Blob")
liste_monstres.append(monstre1)

police = pygame.font.SysFont('Arial', 16)
MENU_X = TILES_HORIZONTAL * TAILLE_TILE
tour_actuelle = "base"

# Plus tard, il faudra charger automatiquement les images à partir du dictionnaire du dessus.
image_tour1 = pygame.image.load(dico_tours["base"]["image_src"]).convert_alpha()

popmonstre_intervalle = 0
popmonstre_timer = time()

#BOUCLE INFINIE
continuer = True
while continuer:
    #pygame.time.Clock().tick(30)
    for event in pygame.event.get():
        if event.type == QUIT:
            continuer = False
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1: # clic gauche
            position_souris = pygame.mouse.get_pos()
            if position_souris[0] > MENU_X and position_souris[1] > 96: # un clic quelque part sur la liste de tours
                pos_case_x = int((position_souris[0] - MENU_X) / TAILLE_TILE)
                pos_case_y = int((position_souris[1] - 96) / TAILLE_TILE)
                if pos_case_x == 0 and pos_case_y == 0:
                    tour_actuelle = "base"
            elif position_souris[0] < MENU_X: # un clic sur la carte
                pos_case_x = int(position_souris[0] / TAILLE_TILE)
                pos_case_y = int(position_souris[1] / TAILLE_TILE)
                if grille[pos_case_y][pos_case_x] == "mur":
                    cout_tour = int(dico_tours[tour_actuelle]["cout"])
                    if cout_tour > joueur_argent:
                        print("Le cout de la tour est trop cher par rapport à tes moyens")
                    else:
                        joueur_argent -= cout_tour
                        tour = Tour(tour_actuelle, pos_case_x, pos_case_y)
                        liste_tours.append(tour)
                        grille[pos_case_y][pos_case_x] = "tour"

    ## Arrivée de monstre frais régulièrement
    if popmonstre_intervalle >= 1/1:
        popmonstre_intervalle = 0
        popmonstre_timer = time()
        monstre = Monstre(0, 0, dico_monstres, "Blob")
        liste_monstres.append(monstre)
    else:
         popmonstre_intervalle = time() - popmonstre_timer
    
    afficher_carte(fenetre, grille, dico_textures, liste_monstres, liste_tours)

    rectangle_noir = pygame.Surface((LARGEUR_MENU, 96))
    rectangle_noir.fill((0, 0, 0))
    fenetre.blit(rectangle_noir, (MENU_X, 0))
    
    texte_score = police.render("Score : " + str(joueur_score), 1, (255, 255, 255))
    texte_vie = police.render(str(joueur_vie) + " ♥", 1, (255, 255, 255))
    texte_argent = police.render(str(joueur_argent) + " €", 1, (255, 255, 255))
    
    fenetre.blit(texte_score, (MENU_X + 10, 10))
    fenetre.blit(texte_vie, (MENU_X + 10, 30))
    fenetre.blit(texte_argent, (MENU_X + 10, 50))

    fenetre.blit(image_tour1, (MENU_X, 96))
    pygame.display.flip()

pygame.quit()

#os.chdir(ancien_chemin)
