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

codes = ["lance_le_jeu", #0
        "je_joue", #1
        "fin_du_jeu" #2
        ] #codes pour communiqué avec le serveur

##var/lists global
hold_clic = False
fps = 30
cplat_size = (8,6)
a_moi_djouer = None #changé en True uniquement si je suis joeuru blanc (white)
coords_pre_move = []
my_color = None #b for black and w for white #### blanc = joueur rouge, noir = joueur jaune
coords_select = None
con_serv = None
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
bg_in_game = pygame.transform.scale(pygame.image.load(resource_path0("./assets/images/background/bg_in_game.png")).convert(), (1920, 1080))

#pions
cvide = pygame.transform.scale(pygame.image.load(resource_path0("./assets/images/pions/connect_pions/cvide.png")).convert_alpha(), (85,85))
cred = pygame.transform.scale(pygame.image.load(resource_path0("./assets/images/pions/connect_pions/cred.png")).convert_alpha(), (85,85))
cyel = pygame.transform.scale(pygame.image.load(resource_path0("./assets/images/pions/connect_pions/cyel.png")).convert_alpha(), (85,85))



#autre in chess
going_to_move = pygame.transform.scale(pygame.image.load(resource_path0("./assets/images/pions/chess_pions/going_to_move.png")).convert_alpha(), (85,85))
going_to_eat = pygame.transform.scale(pygame.image.load(resource_path0("./assets/images/pions/chess_pions/going_to_eat.png")).convert_alpha(), (85,85))
pion_selected = pygame.transform.scale(pygame.image.load(resource_path0("./assets/images/pions/chess_pions/pion_selected.png")).convert_alpha(), (85,85))
eche = pygame.transform.scale(pygame.image.load(resource_path0("./assets/images/pions/chess_pions/echec.png")).convert_alpha(), (85,85))
eche_mat = pygame.transform.scale(pygame.image.load(resource_path0("./assets/images/pions/chess_pions/echec_mat.png")).convert_alpha(), (85,85))



ch_pions = {}
name_chpions = ["bishop", "king", "knight", "pawn", "queen", "rook"]


#var/list/dicts

cplateau = {}
for y in range(cplat_size[1]) :
    for x in range(cplat_size[0]) :
        cplateau[(x,y)] = cvide



def get_next_line(text, ind) :
    try :
        while True :
            if text[ind] == "\n" :
                return ind
            ind+=1
    except :
        return 0



#threads serveur
def goto_command(com) :
    global bataille_loop, wait_loop, ch_pions, my_color, a_moi_djouer
    if com[0] in codes[0] :
        if com[1] == "b" :
            a_moi_djouer = False
            my_color = "b"
            ch_pions = {}
            ch_pions[(2, 7)] = ["w_bishop1", pygame.transform.scale(pygame.image.load(resource_path0("./assets/images/pions/chess_pions/w_bishop.png")).convert_alpha(), (90,90)), (2, 7)]
            ch_pions[(5, 7)] = ["w_bishop2", pygame.transform.scale(pygame.image.load(resource_path0("./assets/images/pions/chess_pions/w_bishop.png")).convert_alpha(), (90,90)), (5, 7)]

            ch_pions[(4, 7)] = ["w_king", pygame.transform.scale(pygame.image.load(resource_path0("./assets/images/pions/chess_pions/w_king.png")).convert_alpha(), (90,90)), (4, 7)]

            ch_pions[(1, 7)] = ["w_knight1", pygame.transform.scale(pygame.image.load(resource_path0("./assets/images/pions/chess_pions/w_knight.png")).convert_alpha(), (90,90)), (1, 7)]
            ch_pions[(6, 7)] = ["w_knight2", pygame.transform.scale(pygame.image.load(resource_path0("./assets/images/pions/chess_pions/w_knight.png")).convert_alpha(), (90,90)), (6, 7)]

            ch_pions[(3, 7)] = ["w_queen", pygame.transform.scale(pygame.image.load(resource_path0("./assets/images/pions/chess_pions/w_queen.png")).convert_alpha(), (90,90)), (3, 7)]

            ch_pions[(0, 7)] = ["w_rook1", pygame.transform.scale(pygame.image.load(resource_path0("./assets/images/pions/chess_pions/w_rook.png")).convert_alpha(), (90,90)), (0, 7)]
            ch_pions[(7, 7)] = ["w_rook2", pygame.transform.scale(pygame.image.load(resource_path0("./assets/images/pions/chess_pions/w_rook.png")).convert_alpha(), (90,90)), (7, 7)]

            ch_pions[(0, 6)] = ["w_pawn", pygame.transform.scale(pygame.image.load(resource_path0("./assets/images/pions/chess_pions/w_pawn.png")).convert_alpha(), (90,90)), (0, 6)]
            ch_pions[(1, 6)] = ["w_pawn", pygame.transform.scale(pygame.image.load(resource_path0("./assets/images/pions/chess_pions/w_pawn.png")).convert_alpha(), (90,90)), (1, 6)]
            ch_pions[(2, 6)] = ["w_pawn", pygame.transform.scale(pygame.image.load(resource_path0("./assets/images/pions/chess_pions/w_pawn.png")).convert_alpha(), (90,90)), (2, 6)]
            ch_pions[(3, 6)] = ["w_pawn", pygame.transform.scale(pygame.image.load(resource_path0("./assets/images/pions/chess_pions/w_pawn.png")).convert_alpha(), (90,90)), (3, 6)]
            ch_pions[(4, 6)] = ["w_pawn", pygame.transform.scale(pygame.image.load(resource_path0("./assets/images/pions/chess_pions/w_pawn.png")).convert_alpha(), (90,90)), (4, 6)]
            ch_pions[(5, 6)] = ["w_pawn", pygame.transform.scale(pygame.image.load(resource_path0("./assets/images/pions/chess_pions/w_pawn.png")).convert_alpha(), (90,90)), (5, 6)]
            ch_pions[(6, 6)] = ["w_pawn", pygame.transform.scale(pygame.image.load(resource_path0("./assets/images/pions/chess_pions/w_pawn.png")).convert_alpha(), (90,90)), (6, 6)]
            ch_pions[(7, 6)] = ["w_pawn", pygame.transform.scale(pygame.image.load(resource_path0("./assets/images/pions/chess_pions/w_pawn.png")).convert_alpha(), (90,90)), (7, 6)]
            #----------------------
            ch_pions[(2, 0)] = ["b_bishop1", pygame.transform.scale(pygame.image.load(resource_path0("./assets/images/pions/chess_pions/b_bishop.png")).convert_alpha(), (90,90)), (2, 0)]
            ch_pions[(5, 0)] = ["b_bishop2", pygame.transform.scale(pygame.image.load(resource_path0("./assets/images/pions/chess_pions/b_bishop.png")).convert_alpha(), (90,90)), (5, 0)]

            ch_pions[(4, 0)] = ["b_king", pygame.transform.scale(pygame.image.load(resource_path0("./assets/images/pions/chess_pions/b_king.png")).convert_alpha(), (90,90)), (4, 0)]

            ch_pions[(1, 0)] = ["b_knight1", pygame.transform.scale(pygame.image.load(resource_path0("./assets/images/pions/chess_pions/b_knight.png")).convert_alpha(), (90,90)), (1, 0)]
            ch_pions[(6, 0)] = ["b_knight2", pygame.transform.scale(pygame.image.load(resource_path0("./assets/images/pions/chess_pions/b_knight.png")).convert_alpha(), (90,90)), (6, 0)]

            ch_pions[(3, 0)] = ["b_queen", pygame.transform.scale(pygame.image.load(resource_path0("./assets/images/pions/chess_pions/b_queen.png")).convert_alpha(), (90,90)), (3, 0)]

            ch_pions[(0, 0)] = ["b_rook1", pygame.transform.scale(pygame.image.load(resource_path0("./assets/images/pions/chess_pions/b_rook.png")).convert_alpha(), (90,90)), (0, 0)]
            ch_pions[(7, 0)] = ["b_rook2", pygame.transform.scale(pygame.image.load(resource_path0("./assets/images/pions/chess_pions/b_rook.png")).convert_alpha(), (90,90)), (7, 0)]

            ch_pions[(0, 1)] = ["b_pawn", pygame.transform.scale(pygame.image.load(resource_path0("./assets/images/pions/chess_pions/b_pawn.png")).convert_alpha(), (90,90)), (0, 1)]
            ch_pions[(1, 1)] = ["b_pawn", pygame.transform.scale(pygame.image.load(resource_path0("./assets/images/pions/chess_pions/b_pawn.png")).convert_alpha(), (90,90)), (1, 1)]
            ch_pions[(2, 1)] = ["b_pawn", pygame.transform.scale(pygame.image.load(resource_path0("./assets/images/pions/chess_pions/b_pawn.png")).convert_alpha(), (90,90)), (2, 1)]
            ch_pions[(3, 1)] = ["b_pawn", pygame.transform.scale(pygame.image.load(resource_path0("./assets/images/pions/chess_pions/b_pawn.png")).convert_alpha(), (90,90)), (3, 1)]
            ch_pions[(4, 1)] = ["b_pawn", pygame.transform.scale(pygame.image.load(resource_path0("./assets/images/pions/chess_pions/b_pawn.png")).convert_alpha(), (90,90)), (4, 1)]
            ch_pions[(5, 1)] = ["b_pawn", pygame.transform.scale(pygame.image.load(resource_path0("./assets/images/pions/chess_pions/b_pawn.png")).convert_alpha(), (90,90)), (5, 1)]
            ch_pions[(6, 1)] = ["b_pawn", pygame.transform.scale(pygame.image.load(resource_path0("./assets/images/pions/chess_pions/b_pawn.png")).convert_alpha(), (90,90)), (6, 1)]
            ch_pions[(7, 1)] = ["b_pawn", pygame.transform.scale(pygame.image.load(resource_path0("./assets/images/pions/chess_pions/b_pawn.png")).convert_alpha(), (90,90)), (7, 1)]



            for y in range(2, 6) :
                for x in range(8) :
                    ch_pions[(x, y)] = []
        else :
            a_moi_djouer = True
            my_color = "w"
            ch_pions = {}
            ch_pions[(2, 7)] = ["b_bishop1", pygame.transform.scale(pygame.image.load(resource_path0("./assets/images/pions/chess_pions/b_bishop.png")).convert_alpha(), (90,90)), (2, 7)]
            ch_pions[(5, 7)] = ["b_bishop2", pygame.transform.scale(pygame.image.load(resource_path0("./assets/images/pions/chess_pions/b_bishop.png")).convert_alpha(), (90,90)), (5, 7)]

            ch_pions[(4, 7)] = ["b_king", pygame.transform.scale(pygame.image.load(resource_path0("./assets/images/pions/chess_pions/b_king.png")).convert_alpha(), (90,90)), (4, 7)]

            ch_pions[(1, 7)] = ["b_knight1", pygame.transform.scale(pygame.image.load(resource_path0("./assets/images/pions/chess_pions/b_knight.png")).convert_alpha(), (90,90)), (1, 7)]
            ch_pions[(6, 7)] = ["b_knight2", pygame.transform.scale(pygame.image.load(resource_path0("./assets/images/pions/chess_pions/b_knight.png")).convert_alpha(), (90,90)), (6, 7)]

            ch_pions[(3, 7)] = ["b_queen", pygame.transform.scale(pygame.image.load(resource_path0("./assets/images/pions/chess_pions/b_queen.png")).convert_alpha(), (90,90)), (3, 7)]

            ch_pions[(0, 7)] = ["b_rook1", pygame.transform.scale(pygame.image.load(resource_path0("./assets/images/pions/chess_pions/b_rook.png")).convert_alpha(), (90,90)), (0, 7)]
            ch_pions[(7, 7)] = ["b_rook2", pygame.transform.scale(pygame.image.load(resource_path0("./assets/images/pions/chess_pions/b_rook.png")).convert_alpha(), (90,90)), (7, 7)]

            ch_pions[(0, 6)] = ["b_pawn", pygame.transform.scale(pygame.image.load(resource_path0("./assets/images/pions/chess_pions/b_pawn.png")).convert_alpha(), (90,90)), (0, 6)]
            ch_pions[(1, 6)] = ["b_pawn", pygame.transform.scale(pygame.image.load(resource_path0("./assets/images/pions/chess_pions/b_pawn.png")).convert_alpha(), (90,90)), (1, 6)]
            ch_pions[(2, 6)] = ["b_pawn", pygame.transform.scale(pygame.image.load(resource_path0("./assets/images/pions/chess_pions/b_pawn.png")).convert_alpha(), (90,90)), (2, 6)]
            ch_pions[(3, 6)] = ["b_pawn", pygame.transform.scale(pygame.image.load(resource_path0("./assets/images/pions/chess_pions/b_pawn.png")).convert_alpha(), (90,90)), (3, 6)]
            ch_pions[(4, 6)] = ["b_pawn", pygame.transform.scale(pygame.image.load(resource_path0("./assets/images/pions/chess_pions/b_pawn.png")).convert_alpha(), (90,90)), (4, 6)]
            ch_pions[(5, 6)] = ["b_pawn", pygame.transform.scale(pygame.image.load(resource_path0("./assets/images/pions/chess_pions/b_pawn.png")).convert_alpha(), (90,90)), (5, 6)]
            ch_pions[(6, 6)] = ["b_pawn", pygame.transform.scale(pygame.image.load(resource_path0("./assets/images/pions/chess_pions/b_pawn.png")).convert_alpha(), (90,90)), (6, 6)]
            ch_pions[(7, 6)] = ["b_pawn", pygame.transform.scale(pygame.image.load(resource_path0("./assets/images/pions/chess_pions/b_pawn.png")).convert_alpha(), (90,90)), (7, 6)]
            #----------------------
            ch_pions[(2, 0)] = ["w_bishop1", pygame.transform.scale(pygame.image.load(resource_path0("./assets/images/pions/chess_pions/w_bishop.png")).convert_alpha(), (90,90)), (2, 0)]
            ch_pions[(5, 0)] = ["w_bishop2", pygame.transform.scale(pygame.image.load(resource_path0("./assets/images/pions/chess_pions/w_bishop.png")).convert_alpha(), (90,90)), (5, 0)]

            ch_pions[(4, 0)] = ["w_king", pygame.transform.scale(pygame.image.load(resource_path0("./assets/images/pions/chess_pions/w_king.png")).convert_alpha(), (90,90)), (4, 0)]

            ch_pions[(1, 0)] = ["w_knight1", pygame.transform.scale(pygame.image.load(resource_path0("./assets/images/pions/chess_pions/w_knight.png")).convert_alpha(), (90,90)), (1, 0)]
            ch_pions[(6, 0)] = ["w_knight2", pygame.transform.scale(pygame.image.load(resource_path0("./assets/images/pions/chess_pions/w_knight.png")).convert_alpha(), (90,90)), (6, 0)]

            ch_pions[(3, 0)] = ["w_queen", pygame.transform.scale(pygame.image.load(resource_path0("./assets/images/pions/chess_pions/w_queen.png")).convert_alpha(), (90,90)), (3, 0)]

            ch_pions[(0, 0)] = ["w_rook1", pygame.transform.scale(pygame.image.load(resource_path0("./assets/images/pions/chess_pions/w_rook.png")).convert_alpha(), (90,90)), (0, 0)]
            ch_pions[(7, 0)] = ["w_rook2", pygame.transform.scale(pygame.image.load(resource_path0("./assets/images/pions/chess_pions/w_rook.png")).convert_alpha(), (90,90)), (7, 0)]

            ch_pions[(0, 1)] = ["w_pawn", pygame.transform.scale(pygame.image.load(resource_path0("./assets/images/pions/chess_pions/w_pawn.png")).convert_alpha(), (90,90)), (0, 1)]
            ch_pions[(1, 1)] = ["w_pawn", pygame.transform.scale(pygame.image.load(resource_path0("./assets/images/pions/chess_pions/w_pawn.png")).convert_alpha(), (90,90)), (1, 1)]
            ch_pions[(2, 1)] = ["w_pawn", pygame.transform.scale(pygame.image.load(resource_path0("./assets/images/pions/chess_pions/w_pawn.png")).convert_alpha(), (90,90)), (2, 1)]
            ch_pions[(3, 1)] = ["w_pawn", pygame.transform.scale(pygame.image.load(resource_path0("./assets/images/pions/chess_pions/w_pawn.png")).convert_alpha(), (90,90)), (3, 1)]
            ch_pions[(4, 1)] = ["w_pawn", pygame.transform.scale(pygame.image.load(resource_path0("./assets/images/pions/chess_pions/w_pawn.png")).convert_alpha(), (90,90)), (4, 1)]
            ch_pions[(5, 1)] = ["w_pawn", pygame.transform.scale(pygame.image.load(resource_path0("./assets/images/pions/chess_pions/w_pawn.png")).convert_alpha(), (90,90)), (5, 1)]
            ch_pions[(6, 1)] = ["w_pawn", pygame.transform.scale(pygame.image.load(resource_path0("./assets/images/pions/chess_pions/w_pawn.png")).convert_alpha(), (90,90)), (6, 1)]
            ch_pions[(7, 1)] = ["w_pawn", pygame.transform.scale(pygame.image.load(resource_path0("./assets/images/pions/chess_pions/w_pawn.png")).convert_alpha(), (90,90)), (7, 1)]

            for y in range(2, 6) :
                for x in range(8) :
                    ch_pions[(x, y)] = []
        wait_loop = False
        bataille_loop = True
    elif com[0] in codes[1] :
        ch_pions[(int(com[1]), 7-int(com[2]))], ch_pions[(int(com[3]), 7-int(com[4]))] = [], ch_pions[(int(com[1]), 7-int(com[2]))]

        if my_color == "w" :
            col = "b"
        else :
            col = "w"
        ajout_connect_pions(int(com[1]), col)


        a_moi_djouer = True
        dit = test_echec(ch_pions)
        if dit :
            test_mat()



class Connection(threading.Thread) :
    def __init__(self):
        threading.Thread.__init__(self)
    def run(self) :
        global con_serv
        ##thread+connection
        if compilation :
            host, port = ("localhost", 5555)
        try :
            con_serv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            con_serv.connect((host, port))
            print("connection effectué")

            while True :
                try :
                    data = con_serv.recv(1024)
                    data = data.decode("utf8")
                    com = data.split(" ")
                    goto_command(com)
                except Exception :
                    traceback.print_exc()

        except Exception :
            traceback.print_exc()
            print("<system> : Connexion au serveur échoué")
        finally :
            if con_serv != None :
                print("connection fermé")
                con_serv.close()
            con_serv = None
            sys.exit()



#####fonction auxilière


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













#se connecter
Connection().start()



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

