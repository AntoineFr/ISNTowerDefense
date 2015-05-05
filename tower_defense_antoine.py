##Il faudra créer un groupe des munitions lancées et utiliser groupe.collide
#avec les monstres 
## problème avec le "ennemi" pas défini




import pygame
from pygame.locals import *
from time import time
from collections import OrderedDict


        # A mettre dans un fichier constantes.py
LARGEUR_MENU = 150
TAILLE_TILE = 32        # les tiles sont des carrés de 32 sur 32
TILES_HORIZONTAL = 10       # le nombre de tiles horizontaux de la map
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

        # Ce dictionnaire regroupe les attributs variables en fonction des monstres, ie leurs caractéristiques
dico_monstres = {"Blob" : {"vie" : 5,
                           "vitesse" : 2,       #2 cases par seconde
                           "butin" : 10,
                           "xp" : 15,
                           "force" : 1,
                           "image_haut_src" : "sprites_tower_defense/BlobBack1.png",
                           "image_bas_src" : "sprites_tower_defense/BlobFace1.png",
                           "image_gauche_src" : "sprites_tower_defense/BlobGauche1.png",
                           "image_droite_src" : "sprites_tower_defense/BlobDroite1.png"
                           },
                 "Boss" : {"vie" : 25,
                           "vitesse" : 1,       #1 case par seconde
                           "butin" : 30,
                           "xp" : 30,
                           "force" : 10,
                           "image_haut_src" : "sprites_tower_defense/BossBack.png",
                           "image_bas_src" : "sprites_tower_defense/Boss.png",
                           "image_gauche_src" : "sprites_tower_defense/BossGauche.png",
                           "image_droite_src" : "sprites_tower_defense/BossDroite.png"
                           }
                 }

        # Ce dictionnaire regroupe les attributs variables en fonction des tours, ie leurs caractéristiques
dic_tours = {"base" : {"cout" : 1,
                        "portee" : 25,
                        "cadence" : 1,
                        "degats" : 1,
                        "image_src" : "sprites_tower_defense/Tour1--0t.png"
                        },
              "feu" : {"cout" : 2,
                        "portee" : 10,
                        "cadence" : 1,
                        "degats" : 3,
                        "image_src" : "sprites_tower_defense/Tour2--0t.png"
                        }
              }

# Crée une version ordonnée du dico précedent (ordre alphabétique)
# Pour l'affichage dans le menu en bas à droite
dico_tours = OrderedDict(sorted(dic_tours.items(), key=lambda t: t[0]))


dico_images = { "tours" : {"base" : "sprites_tower_defense/Tour1--0t.png",
                           "feu" : "sprites_tower_defense/Tour2--0t.png"
## si eventuel besoin        "XXX" : "sprites_tower_defense/Tour3--0t.png"
                           },
                "monstres" : {"dos" : { "boss" : "sprites_tower_defense/BossBack.png",
                                         "blobA" : "sprites_tower_defense/BlobBack1.png",
                                         "blobB" : "sprites_tower_defense/BlobBack2.png",
                                         "blobC" : "sprite_tower_defense/BlobBack3.png"},
                               "face" : { "boss" : "sprites_tower_defense/Boss.png",
                                          "blobA" : "sprites_tower_defense/BlobFace1.png",
                                          "blobB" : "sprites_tower_defense/BlobFace2.png",
                                          "blobC" : "sprites_tower_defense/BlobFace3.png"},
                               "droite" : { "boss" : "sprites_tower_defense/BossDroite.png",
                                          "blobA" : "sprites_tower_defense/BlobDroite1.png",
                                          "blobB" : "sprites_tower_defense/BlobDroite2.png",
                                          "blobC" : "sprites_tower_defense/BlobDroite3.png"},
                               "gauche" : { "boss" : "sprites_tower_defense/BossGauche.png",
                                          "blobA" : "sprites_tower_defense/BlobGauche1.png",
                                          "blobB" : "sprites_tower_defense/BlobGauche2.png",
                                          "blobC" : "sprites_tower_defense/BlobGauche3.png"}
                               },
                "boulets" : {"Boulet1" : "sprites_tower_defense/Boule_tour1",
                             "Boulet2" : "sprites_tower_defense/Boule_tour2"}
                }



liste_vagues = [{"intervalle" : 1, "monstres" : ["Blob","Blob","Boss"]}]

liste_tours = []
liste_monstres = []

#groupe_monstres = pygame.sprite.Group()
pygame.init()
fenetre = pygame.display.set_mode((TILES_HORIZONTAL * TAILLE_TILE + LARGEUR_MENU, TILES_VERTICAL * TAILLE_TILE))


################################################################################
class Monstre(pygame.sprite.Sprite):
    def __init__(self, _x, _y, dico_monstres, nom):
        pygame.sprite.Sprite.__init__(self)
        
        for attribut in dico_monstres[nom].keys():      # chargement des attributs
            self.__dict__[attribut] = dico_monstres[nom][attribut]
         
        self.image_haut = pygame.image.load(self.image_haut_src).convert_alpha()
        self.image_bas = pygame.image.load(self.image_bas_src).convert_alpha()
        self.image_gauche = pygame.image.load(self.image_gauche_src).convert_alpha()
        self.image_droite = pygame.image.load(self.image_droite_src).convert_alpha()
        self.image = self.image_bas
        
        self.rect = self.image.get_rect()
        self.intervalle = 0
        self.cases_marchees = 0 #la distance parcourue par le monstre en cases
        self.timer = time()
        self.direction = "bas"
        self.x_case = _x
        self.y_case = _y
        self.x = _x * TAILLE_TILE
        self.y = _y * TAILLE_TILE
        self.cases_marchables = ("sol", "arrivee", "depart")
##        if self.vie == 0 and self in liste_monstres:
##            liste_monstres.remove(self)        
        
    def sur_arrivee(self):
        return grille[self.y_case][self.x_case] == 'arrivee'                
        
        
    def deplacer(self, grille):
        global joueur_vie
        global groupe_monstres
                # Recherche d'un chemin libre
        try:        # On évite les erreurs dues à des indices trop grands
            if self.sur_arrivee():
                joueur_vie -= self.force
                print("Vous perdez des points de vie !!")
                groupe_monstres.remove(self)
            if self.intervalle >= 1/self.vitesse:
                if grille[self.y_case - 1][self.x_case] in self.cases_marchables and self.direction != "bas":# Vérifie en haut
                    self.y_case -= 1
                    self.direction = "haut"
                    self.image = self.image_haut
                elif grille[self.y_case][self.x_case + 1] in self.cases_marchables and self.direction != "gauche":# Vérifie à droite
                    self.x_case += 1
                    self.direction = "droite"
                    self.image = self.image_droite
                elif grille[self.y_case + 1][self.x_case] in self.cases_marchables and self.direction != "haut":# Vérifie en bas
                    self.y_case += 1
                    self.direction = "bas"
                    self.image = self.image_bas
                elif grille[self.y_case][self.x_case - 1] in self.cases_marchables and self.direction != "droite":# Vérifie à gauche
                    self.x_case -= 1
                    self.direction = "gauche"
                    self.image = self.image_gauche
                
                self.intervalle = 0
                self.timer = time()
            else:
                self.intervalle = time() - self.timer

        except IndexError:
            pass        
        
    def draw(self, fenetre):
        self.rect.x = self.x_case * TAILLE_TILE
        self.rect.y = self.y_case * TAILLE_TILE
        fenetre.blit(self.image, (self.x, self.y))

    def update(self, grille, fenetre):
        self.deplacer(grille)
        self.draw(fenetre)

##################################################################################
class Tour(pygame.sprite.Sprite):
    def __init__(self, nom, _x, _y):
        pygame.sprite.Sprite.__init__(self)

        for attribut in dico_tours[nom].keys():
            self.__dict__[attribut] = dico_tours[nom][attribut]
            
        self.intervalle = 0
        self.nom = nom
        self.timer = time()
        self.x_case = _x
        self.y_case = _y
        self.x = _x * TAILLE_TILE
        self.y = _y * TAILLE_TILE
        self.rect = pygame.Rect(self.x, self.y, 30, 30)
        self.image = pygame.image.load(self.image_src).convert_alpha()
            
    def tire(self, ennemi):
        #global liste_monstres
##        """On tire si la distance tourelle/ennemi est inférieure à la portée
##           à une cadence donnée"""
        if (ennemi.x - self.x)**2 + (ennemi.y - self.y)**2 <= self.portee**2 \
           and self.intervalle >= 1/self.cadence and ennemi.vie - self.degats >= 0:
            ennemi.vie -= self.degats
            self.intervalle = 0
            self.timer = time()
            print(ennemi.vie)
            if ennemi.vie == 0 and ennemi in liste_monstres:
                liste_monstres.remove(ennemi)
        else:
            self.intervalle = time() - self.timer

    def draw(self, fenetre):
        fenetre.blit(self.image, (self.x, self.y))

    def update(self, fenetre):
        self.tire(ennemi)
        self.draw(fenetre)

dico_textures = {"sol" : pygame.image.load("sprites_tower_defense/sol.png").convert_alpha(),
                 "mur" : pygame.image.load("sprites_tower_defense/mur.png").convert_alpha(),
                 "depart" : pygame.image.load("sprites_tower_defense/depart.png").convert_alpha(),
                 "arrivee" : pygame.image.load("sprites_tower_defense/arrivee.png").convert_alpha(),
                 "tour" : pygame.image.load("sprites_tower_defense/transparent.png").convert_alpha()
                 }

def afficher_carte(fenetre, grille, dico_textures, groupe_tours, groupe_monstres):
    for y, colonne in enumerate(grille):
        for x, case in enumerate(colonne):
            texture = dico_textures[case]       # on récupère l'image correspondant à la case
            fenetre.blit(texture, (x * TAILLE_TILE, y * TAILLE_TILE))
    groupe_tours.draw(fenetre)
    groupe_monstres.draw(fenetre)


def clear_callback(fenetre, groupe_monstres):
    color = dico_textures["sol"]
    fenetre.fill(color, rect)

#######################################################################################

police = pygame.font.SysFont('Arial', 16)
MENU_X = TILES_HORIZONTAL * TAILLE_TILE

tour_actuelle = "base"
vague_actuelle = 0
vague = liste_vagues[vague_actuelle]["monstres"]
groupe_monstres = pygame.sprite.RenderUpdates()
groupe_tours = pygame.sprite.RenderUpdates()
##groupcollide(dico_monstre, dico_images, Boulet1, Monstre, collided = None)           à revoir

popmonstre_intervalle = 0
popmonstre_timer = time()
pause = False

#BOUCLE INFINIE
continuer = True
while continuer:
    for event in pygame.event.get():
        if event.type == QUIT:
            continuer = False
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:      # clic gauche
            position_souris = pygame.mouse.get_pos()
            if position_souris[0] > MENU_X and position_souris[1] > 96:         # un clic quelque part sur la liste de tours
                pos_case_x = int((position_souris[0] - MENU_X) / TAILLE_TILE)
                pos_case_y = int((position_souris[1] - 96) / TAILLE_TILE)
##        if event.type == pygame.MOUSEMOTION and event.buttons[0] == 1:        # test par Odilon : le darg-click : echec pour l'instant
##            position_souris = pygame.mouse.get_pos()
##            pos_case_x = int((position_souris[0] - MENU_X) / TAILLE_TILE)
##            pos_case_y = int((position_souris[1] - 96) / TAILLE_TILE)
##            if pos_case_x - 16 < event.pos[0] <= pos_case_x + 48 and pos_case_y - 16 < event.pos[1] <= pos_case_ + 48:
##                pos_case_x = event.pos[0]
##                pos_case_y = event.pos[1]
                if pos_case_x == 0 and pos_case_y == 0:
                    tour_actuelle = "base"
                elif pos_case_x == 1 and pos_case_y == 0:
                    tour_actuelle = "feu"
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
                        #liste_tours.append(tour)#inutile à terme
                        groupe_tours.add(tour)
                        grille[pos_case_y][pos_case_x] = "tour"

##        if event.type == MOUSEMOTION:
##            if pos_case_x - 16 < event.pos[0] <= pose_case_x + 48 and pos_case_y - 16 < event.pos[1] <= pos_case_ + 48:
##                if event.buttons[0] == 1:
##                    boss_x = event.pos[0]
##                    boss_y = event.pos[1]

                        
    if not pause:
        ## Arrivée de monstre frais régulièrement
        if popmonstre_intervalle >= liste_vagues[vague_actuelle]["intervalle"]:
            popmonstre_intervalle = 0
            popmonstre_timer = time()
            if len(liste_vagues[vague_actuelle]["monstres"]) == 0:
                pause = True
                vague_actuelle += 1
                continue
            ennemi = Monstre(0, 0, dico_monstres, liste_vagues[vague_actuelle]["monstres"][0])
            groupe_monstres.add(ennemi)
            liste_vagues[vague_actuelle]["monstres"].pop(0)
        else:
            popmonstre_intervalle = time() - popmonstre_timer

    groupe_monstres.update(grille, fenetre)
    groupe_tours.update(fenetre)

    afficher_carte(fenetre, grille, dico_textures, groupe_tours, groupe_monstres)

    rectangle_noir = pygame.Surface((LARGEUR_MENU, 96))
    rectangle_noir.fill((0, 0, 0))
    fenetre.blit(rectangle_noir, (MENU_X, 0))
    
    texte_score = police.render("Score : " + str(joueur_score), 1, (255, 255, 255))
    texte_vie = police.render(str(joueur_vie) + " ♥", 1, (255, 255, 255))
    texte_argent = police.render(str(joueur_argent) + " $", 1, (255, 255, 255))
    
    fenetre.blit(texte_score, (MENU_X + 10, 10))
    fenetre.blit(texte_vie, (MENU_X + 10, 30))
    fenetre.blit(texte_argent, (MENU_X + 10, 50))

    menu_tours_x = menu_tours_y = 0
    for tour in dico_tours:
        image_tour = pygame.image.load(dico_tours[tour]["image_src"]).convert_alpha()
        fenetre.blit(image_tour, (MENU_X + menu_tours_x * TAILLE_TILE, 96 + menu_tours_y * TAILLE_TILE))
        menu_tours_x += 1
        if menu_tours_x > 3:
           menu_tours_x = 0
           menu_tours_y += 1

    pygame.display.flip()

pygame.quit()

