import copy
from time import sleep
import traceback
from pygame.locals import *
import threading
import pygame
import sys
import socket
import os
import requests





#utile pour le passage en .exe
def resource_path0(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    base_path = getattr(
        sys,
        '_MEIPASS',
        os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)

compilation = None
f = open(resource_path0("./assets/option.txt"), "r")
if f.read() == "true" :
    compilation = True
else :
    compilation = False



##var/lists global
hold_clic = False
fps = 30
cplat_size = (8,6)
coords_pre_move = []
my_color = None #b for black and w for white #### blanc = joueur rouge, noir = joueur jaune
coords_select = None
echec = None
echec_et_mat = None
echec_pre_move = []


#######def var boolean boucles in game
main_loop = True #boucle de la fenêtre de jeu
bataille_loop = False #boucle du menu
wait_loop = True










####init pygame
pygame.init()
pygame.display.set_caption("chess connect")

#Ouverture de la fenêtre Pygame
window = pygame.display.set_mode((0, 0))
clock = pygame.time.Clock()


#fonts
font1 = pygame.font.SysFont("comicsansms", int(1920/55))
font2 = pygame.font.SysFont("comicsansms", int(1920/35))
font3 = pygame.font.SysFont("comicsansms", int(1920/18))






bg_wait_player = pygame.transform.scale(pygame.image.load(resource_path0("./assets/images/background/bg_wait_player.png")).convert(), (1920, 1080))
chess_board = pygame.transform.scale(pygame.image.load(resource_path0("./assets/images/background/chess.png")).convert(), (851, 851))
connect_board = pygame.transform.scale(pygame.image.load(resource_path0("./assets/images/background/connect.png")).convert(), (851, 637))

#pions
cred = pygame.transform.scale(pygame.image.load(resource_path0("./assets/images/pions/connect_pions/cred.png")).convert_alpha(), (85,85))
cyel = pygame.transform.scale(pygame.image.load(resource_path0("./assets/images/pions/connect_pions/cyel.png")).convert_alpha(), (85,85))






ch_pions = {}
name_chpions = ["bishop", "king", "knight", "pawn", "queen"]


#var/list/dicts

cplateau = {}
for y in range(cplat_size[1]) :
    for x in range(cplat_size[0]) :
        cplateau[(x,y)] = cvide




















#threads
def anti_hold_clic():
    global hold_clic
    while main_loop :
        if pygame.mouse.get_pressed()[0] :
            hold_clic = True
            clock.tick(5)
            hold_clic = False
    sys.exit()
#def threads
thread_anti_hold_clic = threading.Thread(target=anti_hold_clic)
thread_anti_hold_clic.start()
















#Boucle infinie
while main_loop:
    

    while wait_loop :


		#Limitation de vitesse de la boucle
        clock.tick(fps) # 30 fps

        #events clavier
        keys = pygame.key.get_pressed()
        for event in pygame.event.get():   #On parcours la liste de tous les événements reçus
            if event.type == QUIT or keys[K_LSHIFT] and keys[K_ESCAPE] :     #Si un de ces événements est de type QUIT
                main_loop = False
                wait_loop = False
        window.blit(bg_wait_player, (0, 0))
        pygame.display.flip()

    while bataille_loop :   
		#Limitation de vitesse de la boucle
        clock.tick(fps) # 30 fps

        #events clavier
        keys = pygame.key.get_pressed()
        for event in pygame.event.get():   #On parcours la liste de tous les événements reçus
            if event.type == QUIT or keys[K_LSHIFT] and keys[K_ESCAPE] :     #Si un de ces événements est de type QUIT
                main_loop = False
                bataille_loop = False


        X, Y = pygame.mouse.get_pos()

        #affichage pions connect
        for y in range(cplat_size[1]) :
            for x in range(cplat_size[0]) :
                window.blit(cplateau[(x,y)], (1034+x*104, 757-y*104))

        pygame.display.flip()
    
os._exit(1)

