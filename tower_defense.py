import pygame
from pygame.locals import *
from time import time

pygame.init()

#dico_tourelles = {nom1 : {attribut1:valeur2, atr2:val2}}
#etc...
dico_tourelles = {"base" : {"cout" : 100, "portee":100, "cadence":1,
                            "degats":10}}
#attributs: coords, cases, portee, cadence, degats, prix
#le nom correspond au type

dico_ennemis = {"gobelin" : {"x":10, "y":10, "vie":40, "vitesse":2}}
L_ennemis = []
chemin = [(1000, 500)]

fenetre = pygame.display.set_mode((300, 300))
fond = pygame.Surface(fenetre.get_size())
fond.fill((255,255,255))
fenetre.blit(fond, (0,0))
pygame.display.flip()



class Tourelle:
    def __init__(self, nom):
        self.intervalle = 0
        self.nom
        = nom
        self.timer = time()
        for attribut in dico_tourelles[nom].keys():
            self.__dict__[attribut] = dico_tourelles[nom][attribut]
            
        self.rect = pygame.Rect(self.x, self.y, 30, 30)
        self.image = pygame.Surface((30, 30))
        self.image.fill((100,100,100))
        
    def tire(self, ennemi):
        """On tire si la disstance tourelle/ennemi est inférieure à la portée
           et a une cadence donnée"""
        if (ennemi.x - self.x)**2 + (ennemi.y - self.y)**2 <= self.portee**2 \
           and self.intervalle >= 1/self.cadence:
            ennemi.vie -= self.degats
            print(ennemi.vie)
            self.intervalle = 0
            self.timer = time()
        else:
            self.intervalle = time() - self.timer

    def affiche(self, fenetre):
        fenetre.blit(self.image, self.rect.topleft)
        pygame.display.flip()
            
            
class Ennemi:
    def __init__(self, nom):
        self.intervalle = 0
        self.timer = time()
        for attribut in dico_ennemis[nom].keys():
            self.__dict__[attribut] = dico_ennemis[nom][attribut]

        self.rect = pygame.Rect(self.x, self.y, 10, 10)
        self.image = pygame.Surface((30, 30))
        self.image.fill((100,150,100))

    def se_deplace(self, next_pos, fenetre, fond):
        direction = (self.x - next_pos[0], self.y - next_pos[1])
        #comme on ne se déplace que vers gauche droite haut bas, il y a
        #forcément un terme nul, on se sert alors des propriétés des booléens
        #(car bool(0) * x = 0, et bool(x) * x = 1 * x = x)
        if self.intervalle >= 1/self.vitesse:
            self.x += self.vitesse * bool(direction[0])
            self.y += self.vitesse * bool(direction[1])
            print(a.x, a.y)
            self.intervalle = 0
            self.timer = time()
            self.affiche(fenetre, fond)
        else:
            self.intervalle = time() - self.timer

    def affiche(self, fenetre, fond):
        fenetre.blit(fond, (0,0))
        fenetre.blit(self.image, (self.x, self.y))
        pygame.display.flip()
        

def verif_ennemis(L_ennemis):
    """enlève les ennemis morts de la liste"""
    for ennemi in L_ennemis:
        if ennemi.vie <= 0:
            L_ennemis.remove(ennemi)
        

a = Ennemi("gobelin")
t = Tourelle("base")
t.affiche(fenetre)

L_ennemis.append(a)

continuer = True
while continuer:
    for event in pygame.event.get():
        if event.type == QUIT:
            continuer = False
    t.tire(a)
    verif_ennemis(L_ennemis)
    a.se_deplace(chemin[0], fenetre, fond)
    t.affiche(fenetre)             
    pygame.display.flip()

pygame.quit()

    
    


    
        
        
            
            
            
            
        
        
        
