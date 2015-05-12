##Il faudra créer un groupe des munitions lancées et utiliser groupe.collide
#avec les monstres


import pygame
from pygame.locals import *
from time import time
from collections import OrderedDict

pygame.init()


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

LARGEUR_MENU = 150
TAILLE_TILE = 32 # les tiles sont des carrés de 32 sur 32
TILES_HORIZONTAL = len(grille[0]) #la largeur de la map
TILES_VERTICAL = len(grille)

fenetre = pygame.display.set_mode((TILES_HORIZONTAL * TAILLE_TILE + LARGEUR_MENU, TILES_VERTICAL * TAILLE_TILE))

# Ce dictionnaire regroupe les attributs variables en fonction des monstres, ie leurs caractéristiques
dico_monstres = {"Blob" : {"vie" : 12,
                           "vitesse" : 2,       #2 cases par seconde
                           "butin" : 5,
                           "xp" : 15,
                           "force" : 1,
                           "image_haut_src" : "sprites_tower_defense/BlobBack1.png",
                           "image_bas_src" : "sprites_tower_defense/BlobFace1.png",
                           "image_gauche_src" : "sprites_tower_defense/BlobGauche1.png",
                           "image_droite_src" : "sprites_tower_defense/BlobDroite1.png"
                           },
                 "Blob2" : {"vie" : 10,
                            "vitesse" : 2,
                            "butin" : 10,
                            "xp" : 20,
                            "force" : 3,
                            "image_haut_src" : "sprites_tower_defense/BlobBack2.png",
                            "image_bas_src" : "sprites_tower_defense/BlobFace2.png",
                           "image_gauche_src" : "sprites_tower_defense/BlobGauche2.png",
                           "image_droite_src" : "sprites_tower_defense/BlobDroite2.png"
                            },
                 "Blob3" : {"vie" : 8,
                            "vitesse" : 4,
                            "butin" : 10,
                            "xp" : 20,
                            "force" : 3,
                            "image_haut_src" : "sprites_tower_defense/BlobBack3.png",
                            "image_bas_src" : "sprites_tower_defense/BlobFace3.png",
                           "image_gauche_src" : "sprites_tower_defense/BlobGauche3.png",
                           "image_droite_src" : "sprites_tower_defense/BlobDroite3.png"
                            },
                 "Boss" : {"vie" : 35,
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
dic_tours = {"base" : {"cout" : 20,
                       "portee" : 70, #en pixels
                       "cadence" : 1, #tirs par seconde
                       "degats" : 1,
                       "image_src" : "sprites_tower_defense/Tour1--0t.png",
                       "image_projectile" : "sprites_tower_defense/Boule_tour_base.png"
                        },
              "feu" : {"cout" : 40,
                        "portee" : 50,
                        "cadence" : 1,
                        "degats" : 3,
                        "image_src" : "sprites_tower_defense/Tour2--0t.png",
                        "image_projectile" : "sprites_tower_defense/Boule_tour_feu.png"
                        }
##             ,"0" : {"cout" : 0,
##                    "portee" : 0,
##                    "cadence" : 0,
##                    "degats" : 0,
##                    "image_src" : "sprites_tower_defense/sol.png"}
              }

# Crée une version ordonnée du dico précedent (ordre alphabétique)
# Pour l'affichage dans le menu en bas à droite
dico_tours = OrderedDict(sorted(dic_tours.items(), key=lambda t: t[0]))


dico_images = { "tours" : {"base" : "sprites_tower_defense/Tour1--0t.png",
                           "feu" : "sprites_tower_defense/Tour2--0t.png"
##                           ,"0" : "sprites_tower_defense/mur.png"
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


dico_textures = {"sol" : pygame.image.load("sprites_tower_defense/sol.png").convert_alpha(),
                 "mur" : pygame.image.load("sprites_tower_defense/mur.png").convert_alpha(),
                 "depart" : pygame.image.load("sprites_tower_defense/depart.png").convert_alpha(),
                 "arrivee" : pygame.image.load("sprites_tower_defense/arrivee.png").convert_alpha(),
                 "tour" : pygame.image.load("sprites_tower_defense/transparent.png").convert_alpha()
                 }


liste_vagues = [{"intervalle" : 1, "monstres" : ["Blob"]},
                {"intervalle" : 1, "monstres" : ["Blob3","Blob2","Blob"]},
                {"intervalle" : 1, "monstres" : ["Blob","Blob2","Blob","Blob2","Boss"]},
                {"intervalle" : 1, "monstres" : ["Blob","Blob3","Blob2","Blob3","Blob3","Boss"]},]


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
        self.cases_marchables = ("sol", "arrivee", "depart")
       
        
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
                self.kill()
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
                    
                self.cases_marchees += 1
                self.intervalle = 0
                self.timer = time()
            else:
                self.intervalle = time() - self.timer
        except IndexError:
            pass        
        
    def draw(self, fenetre):
        self.rect.x = self.x_case * TAILLE_TILE
        self.rect.y = self.y_case * TAILLE_TILE

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

               
    def tire(self, groupe_monstres, groupe_projectiles, choix_ennemi):
        """On tire si la distance tourelle/ennemi est inférieure à la portée
           à une cadence donnée"""
        global joueur_argent
        
        ennemi = choix_ennemi(self, groupe_monstres)
        if ennemi:
            if (ennemi.rect.x - self.x)**2 + (ennemi.rect.y - self.y)**2 <= self.portee**2 \
               and self.intervalle >= 1/self.cadence:
                projectile = self.cree_projectile()
                groupe_projectiles.add(projectile)
                projectile.update(ennemi)
                ennemi.vie -= self.degats
                self.intervalle = 0
                self.timer = time()
                print(ennemi.vie)
                if ennemi.vie <= 0:
                    joueur_argent += ennemi.butin
                    ennemi.kill()
            else:
                self.intervalle = time() - self.timer

    def cree_projectile(self):
        """Affiche un projectile se déplaçant de la tour vers l'ennemi"""
        image_projectile = pygame.image.load(self.image_projectile).convert_alpha()
        rect_projectile = image_projectile.get_rect()
        rect_projectile.center = self.rect.center #on centre le projectile au milieu de la tour
        return Projectile(image_projectile, rect_projectile)

    

    def update(self, groupe_monstres, groupe_projectiles, choix_ennemi):
        self.tire(groupe_monstres, groupe_projectiles, choix_ennemi)

################################################################################

class Projectile(pygame.sprite.Sprite):
    def __init__(self, image, rect):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = rect
        self.rect.center = rect.center

    def update(self, ennemi):
        global fenetre
        delta_x = ennemi.rect.centerx - self.rect.centerx
        delta_y = ennemi.rect.centery - self.rect.centery
        self.rect = self.rect.move(delta_x/5, delta_y/5)
        #print(delta_x, delta_y)
        print(self.rect.center)
        self.draw(fenetre)

    def draw(self, fenetre):
        fenetre.blit(self.image, self.rect.topleft)

#################################################################################        

def afficher_carte(fenetre, grille, dico_textures, groupe_tours, groupe_monstres, groupe_projectiles):
    for y, colonne in enumerate(grille):
        for x, case in enumerate(colonne):
            texture = dico_textures[case]# on récupère l'image correspondant à la case
            fenetre.blit(texture, (x * TAILLE_TILE, y * TAILLE_TILE))
    groupe_tours.draw(fenetre)
    groupe_monstres.draw(fenetre)
    groupe_projectiles.draw(fenetre)

def choix_ennemi(tour, groupe_monstres):
    """Renvoie l'ennemi le plus proche de l'arrivée mais à portée de la tour"""

    liste_ennemis = groupe_monstres.sprites()
    #On trie la liste pour ne garder que les ennemis à portée de la tour, puis
    #on prendra le plus proche de l'arrivée
    liste_ennemis_triee = [ennemi for ennemi in liste_ennemis if \
                           (ennemi.rect.x - tour.x)**2 + (ennemi.rect.y - tour.y)**2 <= tour.portee**2]

    if liste_ennemis_triee: #si la liste n'est pas vide
        ennemi = max(liste_ennemis_triee, key=lambda elt: elt.cases_marchees)
        return ennemi

#######################################################################################

police = pygame.font.SysFont('Arial', 14)
MENU_X = TILES_HORIZONTAL * TAILLE_TILE

tour_actuelle = "base"
carac = "base"
vague_actuelle = 0
vague = liste_vagues[vague_actuelle]["monstres"]
groupe_monstres = pygame.sprite.RenderUpdates()
groupe_tours = pygame.sprite.RenderUpdates()
groupe_projectiles = pygame.sprite.RenderUpdates()
##groupcollide(dico_monstre, dico_images, Boulet1, Monstre, collided = None) à revoir

popmonstre_intervalle = 0
popmonstre_timer = time()
pause = True

#BOUCLE INFINIE
continuer = True
while continuer:
    pygame.time.Clock().tick(100)
    for event in pygame.event.get():
        if event.type == QUIT:
            continuer = False
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:      # clic gauche
            position_souris = pygame.mouse.get_pos()

            #Partie pour choisir une tour dans le menu
            if position_souris[0] > MENU_X and position_souris[1] > 96:         # un clic quelque part sur la liste de tours
                pos_case_x = int((position_souris[0] - MENU_X) / TAILLE_TILE)
                pos_case_y = int((position_souris[1] - 96) / TAILLE_TILE)

                if pos_case_x == 0 and pos_case_y == 0:
                    tour_actuelle = "base"
                    carac = "base"
                elif pos_case_x == 1 and pos_case_y == 0:
                    tour_actuelle = "feu"
                    carac = "feu"

            #Partie pour acheter et placer une tour sur la carte
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
                        groupe_tours.add(tour)
                        grille[pos_case_y][pos_case_x] = "tour"

        #Partie pour vendre une tour
        if event.type == pygame.MOUSEBUTTONUP and event.button == 3:
            position_souris = pygame.mouse.get_pos()
            if position_souris[0] > MENU_X and position_souris[1] > 96:
                pos_case_x = int((position_souris[0] - MENU_X) / TAILLE_TILE)
                pos_case_y = int((position_souris[1] - 96) / TAILLE_TILE)
            elif position_souris[0] < MENU_X:
                pos_case_x = int(position_souris[0] / TAILLE_TILE)
                pos_case_y = int(position_souris[1] / TAILLE_TILE)
                if grille[pos_case_y][pos_case_x] == "mur":
                    cout_tour = int(dico_tours[tour_actuelle]["cout"])
                else:
                    joueur_argent += cout_tour/2
                    tour = Tour(tour_actuelle, pos_case_x, pos_case_y)
                    
        if event.type == pygame.KEYDOWN and event.key == K_p:
            texte_ready = police.render("PRETS ?", 1, (255,255,255))
            fenetre.blit(texte_ready, (MENU_X + 10, 250))
            pause = False
            
    if pause == True:#Je n'arrive pas à setup un boutton qui dit quand la pause est
        texte_pause = police.render("JEU EN PAUSE", 1, (255,255,255))
        fenetre.blit(texte_pause, (MENU_X + 10, 250))
    #Si le jeu n'est pas en pause, les monstres arrivent suivant l'ordre défini
    #dans la vague
    if not pause:
        ## Arrivée de monstre frais régulièrement
        if len(liste_vagues) >= vague_actuelle + 1 and popmonstre_intervalle >= liste_vagues[vague_actuelle]["intervalle"]:
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

    #Actualisation de la carte
    groupe_monstres.update(grille, fenetre)
    groupe_tours.update(groupe_monstres, groupe_projectiles, choix_ennemi)
    afficher_carte(fenetre, grille, dico_textures, groupe_tours, groupe_monstres, groupe_projectiles)
    

    #Affichage du texte à l'écran
    rectangle_noir = pygame.Surface((LARGEUR_MENU, 300))
    rectangle_noir.fill((0, 0, 0))
    fenetre.blit(rectangle_noir, (MENU_X, 0))
    
    texte_score = police.render("Score : " + str(joueur_score), 1, (255, 255, 255))
    texte_vie = police.render(str(joueur_vie) + " ♥", 1, (255, 255, 255))
    texte_argent = police.render(str(joueur_argent) + " $", 1, (255, 255, 255))
    prix_tour = police.render("Cout :" + str(dic_tours[carac]["cout"]) + "$", 1, (255,255,255))
    portee_tour = police.render("Portée :" + str(dic_tours[carac]["portee"]), 1, (255,255,255))
    cadence_tour = police.render("Cadence :" + str(dic_tours[carac]["cadence"]) + "tirs par s", 1, (255,255,255))
    degats_tour = police.render("Dégats :" + str(dic_tours[carac]["degats"]) + " par tir", 1, (255,255,255))
    texte_pause = police.render("JEU EN PAUSE", 1, (255,255,255))
    texte_ready = police.render("PRETS ?", 1, (255,255,255))
    
    fenetre.blit(texte_score, (MENU_X + 10, 10))
    fenetre.blit(texte_vie, (MENU_X + 10, 30))
    fenetre.blit(texte_argent, (MENU_X + 10, 50))
    fenetre.blit(prix_tour, (MENU_X + 10, 130))
    fenetre.blit(portee_tour, (MENU_X + 10, 150))
    fenetre.blit(cadence_tour, (MENU_X + 10, 170))
    fenetre.blit(degats_tour, (MENU_X + 10, 190))

    
    #Affichage des tours "achetables" dands le menu
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

