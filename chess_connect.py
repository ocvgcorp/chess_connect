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
def test_echec(ch_pions) :
    global echec, echec_pre_move, echec_et_mat, a_moi_djouer
    if my_color == "b" :
        col = "w"
    else :
        col = "b"
    pre_move = []
    for y in range(8) :
        for x in range(8) :
            if len(ch_pions[(x, y)]) != 0 :
                if col+"_" not in ch_pions[(x, y)][0] and "king" in ch_pions[(x, y)][0]:
                    king_coords = (x, y)
                elif  col+"_" in ch_pions[(x, y)][0] :
                    if "pawn" in ch_pions[(x, y)][0]  :
                        for move in [(1, 1), (-1, 1)] :
                            try :
                                if cplateau[(x, 5)] == cvide :
                                    if len(ch_pions[(x+move[0], y-move[1])]) != 0 and my_color+"_" in ch_pions[(x+move[0], y-move[1])][0]:
                                        pre_move.append((x+move[0], y-move[1]))
                            except :
                                pass

                    elif "knight" in ch_pions[(x, y)][0]  :
                        help_var_knight = [(-2, 1), (-2, -1), (-1, -2), (1, -2), (2-1), (2, 1), (1, 2), (-1, 2)]
                        for move in help_var_knight :
                            if cplateau[(x, 5)] == cvide:
                                try :
                                    if my_color+"_" in ch_pions[(x+move[0], y-move[1])][0] :
                                        pre_move.append((x+move[0], y-move[1])) #appliquer un filtre jaune
                                except :
                                    pass

                    elif "rook" in ch_pions[(x, y)][0]  :

                        for move in [[(x, 0) for x in range(-1, -8, -1)], [(x, 0) for x in range(1, 8)], [(0, y) for y in range(-1, -8, -1)], [(0, y) for y in range(1, 8)]] :
                            for moveplus in move :
                                if cplateau[(x, 5)] == cvide :
                                    try :
                                        if col+"_" in ch_pions[(x+moveplus[0], y-moveplus[1])][0] :
                                            break
                                        elif my_color+"_" in ch_pions[(x+moveplus[0], y-moveplus[1])][0] :
                                            pre_move.append((x+moveplus[0], y-moveplus[1])) #appliquer un filtre jaune
                                            break
                                    except :
                                        break

                    elif "king" in ch_pions[(x, y)][0]  :
                        for movex in [-1, 0, 1] :
                            for movey in [-1, 0, 1] :
                                if cplateau[(x, 5)] == cvide and not (movex == 0 and movey == 0):
                                    try :
                                        if my_color+"_" in ch_pions[(x+movex, y-movey)][0] :
                                            pre_move.append((x+movex, y-movey)) #appliquer un filtre jaune
                                    except :
                                        pass

                    elif "bishop" in ch_pions[(x, y)][0]  :

                        for help_movex in [-1, 1] :
                            for help_movey in [-1, 1] :
                                for movexy in range(1, 9) :
                                    if cplateau[(x, 5)] == cvide :
                                        try :
                                            if col+"_" in ch_pions[(x+movexy*help_movex, y-movexy*help_movey)][0] :
                                                break
                                            elif my_color+"_" in ch_pions[(x+movexy*help_movex, y-movexy*help_movey)][0] :
                                                pre_move.append((x+movexy*help_movex, y-movexy*help_movey)) #appliquer un filtre jaune
                                                break
                                        except :
                                            break

                    elif "queen" in ch_pions[(x, y)][0]  :

                        for help_movex in [-1, 1] :
                            for help_movey in [-1, 1] :
                                for movexy in range(1, 9) :
                                    if cplateau[(x, 5)] == cvide :
                                        try :
                                            if col+"_" in ch_pions[(x+movexy*help_movex, y-movexy*help_movey)][0] :
                                                break
                                            elif my_color+"_" in ch_pions[(x+movexy*help_movex, y-movexy*help_movey)][0] :
                                                pre_move.append((x+movexy*help_movex, y-movexy*help_movey)) #appliquer un filtre jaune
                                                break
                                        except :
                                            break

                        for move in [[(x, 0) for x in range(-1, -8, -1)], [(x, 0) for x in range(1, 8)], [(0, y) for y in range(-1, -8, -1)], [(0, y) for y in range(1, 8)]] :
                            for moveplus in move :
                                if cplateau[(x, 5)] == cvide :
                                    try :
                                        if col+"_" in ch_pions[(x+moveplus[0], y-moveplus[1])][0] :
                                            break
                                        elif my_color+"_" in ch_pions[(x+moveplus[0], y-moveplus[1])][0] :
                                            pre_move.append((x+moveplus[0], y-moveplus[1])) #appliquer un filtre jaune
                                            break
                                    except :
                                        break
    if king_coords in pre_move :
        return True
    return False
def test_mat() :
        global echec_pre_move, echec_et_mat, echec, a_moi_djouer
        echec_pre_move = {}
        ###test Ajout mat chek (-----------------------------------------------------)
        for y in range(8) :
            for x in range(8) :
                if len(ch_pions[(x, y)]) != 0 :
                    if my_color+"_" in ch_pions[(x, y)][0] and "king" in ch_pions[(x, y)][0]:
                        king_coords = (x, y)
                    if "pawn" in ch_pions[(x, y)][0] and my_color+"_" in ch_pions[(x, y)][0] :
                        if y == 1 :
                            dos = 3
                        else :
                            dos = 2
                        for move in range(1, dos) :
                            try :
                                if cplateau[(x, 5)] == cvide :
                                    if len(ch_pions[(x, y+move)]) == 0 :
                                        ch_copy_pions = my_copy(ch_pions)
                                        ch_copy_pions[(x, y)], ch_copy_pions[(x, y+move)] = [], ch_copy_pions[(x, y)]
                                        if test_echec(ch_copy_pions) == False:
                                            try :
                                                len(echec_pre_move[(x, y)])
                                                echec_pre_move[(x, y)].append(["move_to_vide", (x, y+move)])
                                            except :
                                                echec_pre_move[(x, y)] = [["move_to_vide", (x, y+move)]]
                                    else :
                                        break
                            except :
                                pass

                        for move in [(1, 1), (-1, 1)] :
                            try :
                                if cplateau[(x, 5)] == cvide :
                                    if len(ch_pions[(x+move[0], y+move[1])]) != 0 and my_color+"_" not in ch_pions[(x+move[0], y+move[1])][0]:
                                        ch_copy_pions = my_copy(ch_pions)
                                        ch_copy_pions[(x, y)], ch_copy_pions[(x+move[0], y+move[1])] = [], ch_copy_pions[(x, y)]
                                        if test_echec(ch_copy_pions) == False:
                                            try :
                                                len(echec_pre_move[(x, y)])
                                                echec_pre_move[(x, y)].append(["move_to_eat", (x+move[0], y+move[1])])
                                            except :
                                                echec_pre_move[(x, y)] = [["move_to_eat", (x+move[0], y+move[1])]]
                            except :
                                pass

                    elif "knight" in ch_pions[(x, y)][0] and my_color+"_" in ch_pions[(x, y)][0] :
                        help_var_knight = [(-2, 1), (-2, -1), (-1, -2), (1, -2), (2-1), (2, 1), (1, 2), (-1, 2)]
                        for move in help_var_knight :
                            if cplateau[(x, 5)] == cvide:
                                try :
                                    if len(ch_pions[(x+move[0], y+move[1])]) == 0 :
                                        ch_copy_pions = my_copy(ch_pions)
                                        ch_copy_pions[(x, y)], ch_copy_pions[(x+move[0], y+move[1])] = [], ch_copy_pions[(x, y)]
                                        if test_echec(ch_copy_pions) == False:
                                            try :
                                                len(echec_pre_move[(x, y)])
                                                echec_pre_move[(x, y)].append(["move_to_vide", (x+move[0], y+move[1])])
                                            except :
                                                echec_pre_move[(x, y)] = [["move_to_vide", (x+move[0], y+move[1])]]
                                    elif my_color+"_" not in ch_pions[(x+move[0], y+move[1])][0] :
                                        ch_copy_pions = my_copy(ch_pions)
                                        ch_copy_pions[(x, y)], ch_copy_pions[(x+move[0], y+move[1])] = [], ch_copy_pions[(x, y)]
                                        if test_echec(ch_copy_pions) == False:
                                            try :
                                                len(echec_pre_move[(x, y)])
                                                echec_pre_move[(x, y)].append(["move_to_eat", (x+move[0], y+move[1])])
                                            except :
                                                echec_pre_move[(x, y)] = [["move_to_eat", (x+move[0], y+move[1])]]
                                except :
                                    pass

                    elif "rook" in ch_pions[(x, y)][0] and my_color+"_" in ch_pions[(x, y)][0] :

                        for move in [[(x, 0) for x in range(-1, -8, -1)], [(x, 0) for x in range(1, 8)], [(0, y) for y in range(-1, -8, -1)], [(0, y) for y in range(1, 8)]] :
                            for moveplus in move :
                                if cplateau[(x, 5)] == cvide :
                                    try :
                                        if len(ch_pions[(x+moveplus[0], y+moveplus[1])]) == 0 :
                                            ch_copy_pions = my_copy(ch_pions)
                                            ch_copy_pions[(x, y)], ch_copy_pions[(x+moveplus[0], y+moveplus[1])] = [], ch_copy_pions[(x, y)]
                                            if test_echec(ch_copy_pions) == False:
                                                try :
                                                    len(echec_pre_move[(x, y)])
                                                    echec_pre_move[(x, y)].append(["move_to_vide", (x+moveplus[0], y+moveplus[1])])
                                                except :
                                                    echec_pre_move[(x, y)] = [["move_to_vide", (x+moveplus[0], y+moveplus[1])]]
                                        
                                        elif my_color+"_" in ch_pions[(x+moveplus[0], y+moveplus[1])][0] :
                                            break
                                        else :
                                            ch_copy_pions = my_copy(ch_pions)
                                            ch_copy_pions[(x, y)], ch_copy_pions[(x+moveplus[0], y+moveplus[1])] = [], ch_copy_pions[(x, y)]
                                            if test_echec(ch_copy_pions) == False:
                                                try :
                                                    len(echec_pre_move[(x, y)])
                                                    echec_pre_move[(x, y)].append(["move_to_eat", (x+moveplus[0], y+moveplus[1])])
                                                except :
                                                    echec_pre_move[(x, y)] = [["move_to_eat", (x+moveplus[0], y+moveplus[1])]]
                                            break
                                    except :
                                        break

                    elif "king" in ch_pions[(x, y)][0] and my_color+"_" in ch_pions[(x, y)][0] :

                        for movex in [-1, 0, 1] :
                            for movey in [-1, 0, 1] :
                                if cplateau[(x, 5)] == cvide and not (movex == 0 and movey == 0):
                                    # try :
                                        if len(ch_pions[(x+movex, y+movey)]) == 0 :
                                            ch_copy_pions = my_copy(ch_pions)
                                            ch_copy_pions[(x, y)], ch_copy_pions[(x+movex, y+movey)] = [], ch_copy_pions[(x, y)]
                                            if test_echec(ch_copy_pions) == False:
                                                try :
                                                    len(echec_pre_move[(x, y)])
                                                    echec_pre_move[(x, y)].append(["move_to_vide", (x+movex, y+movey)])
                                                except :
                                                    echec_pre_move[(x, y)] = [["move_to_vide", (x+movex, y+movey)]]
                                        elif my_color+"_" not in ch_pions[(x+movex, y+movey)][0] :
                                            ch_copy_pions = my_copy(ch_pions)
                                            ch_copy_pions[(x, y)], ch_copy_pions[(x+movex, y+movey)] = [], ch_copy_pions[(x, y)]
                                            if test_echec(ch_copy_pions) == False:
                                                try :
                                                    len(echec_pre_move[(x, y)])
                                                    echec_pre_move[(x, y)].append(["move_to_eat", (x+movex, y+movey)])
                                                except :
                                                    echec_pre_move[(x, y)] = [["move_to_eat", (x+movex, y+movey)]]
                                    # except :
                                    #     pass

                    elif "bishop" in ch_pions[(x, y)][0] and my_color+"_" in ch_pions[(x, y)][0] :

                        for help_movex in [-1, 1] :
                            for help_movey in [-1, 1] :
                                for movexy in range(1, 9) :
                                    if cplateau[(x, 5)] == cvide :
                                        try :
                                            if len(ch_pions[(x+movexy*help_movex, y+movexy*help_movey)]) == 0 :
                                                ch_copy_pions = my_copy(ch_pions)
                                                ch_copy_pions[(x, y)], ch_copy_pions[(x+movexy*help_movex, y+movexy*help_movey)] = [], ch_copy_pions[(x, y)]
                                                if test_echec(ch_copy_pions) == False:
                                                    try :
                                                        len(echec_pre_move[(x, y)])
                                                        echec_pre_move[(x, y)].append(["move_to_vide", (x+movexy*help_movex, y+movexy*help_movey)])
                                                    except :
                                                        echec_pre_move[(x, y)] = [["move_to_vide", (x+movexy*help_movex, y+movexy*help_movey)]]
                                            elif my_color+"_" in ch_pions[(x+movexy*help_movex, y+movexy*help_movey)][0] :
                                                break
                                            else :
                                                ch_copy_pions = my_copy(ch_pions)
                                                ch_copy_pions[(x, y)], ch_copy_pions[(x+movexy*help_movex, y+movexy*help_movey)] = [], ch_copy_pions[(x, y)]
                                                if test_echec(ch_copy_pions) == False:
                                                    try :
                                                        len(echec_pre_move[(x, y)])
                                                        echec_pre_move[(x, y)].append(["move_to_eat", (x+movexy*help_movex, y+movexy*help_movey)])
                                                    except :
                                                        echec_pre_move[(x, y)] = [["move_to_eat", (x+movexy*help_movex, y+movexy*help_movey)]]
                                                break
                                        except :
                                            break

                    elif "queen" in ch_pions[(x, y)][0] and my_color+"_" in ch_pions[(x, y)][0] :

                        for help_movex in [-1, 1] :
                            for help_movey in [-1, 1] :
                                for movexy in range(1, 9) :
                                    if cplateau[(x, 5)] == cvide :
                                        try :
                                            if len(ch_pions[(x+movexy*help_movex, y+movexy*help_movey)]) == 0 :
                                                ch_copy_pions = my_copy(ch_pions)
                                                ch_copy_pions[(x, y)], ch_copy_pions[(x+movexy*help_movex, y+movexy*help_movey)] = [], ch_copy_pions[(x, y)]
                                                if test_echec(ch_copy_pions) == False:
                                                    try :
                                                        len(echec_pre_move[(x, y)])
                                                        echec_pre_move[(x, y)].append(["move_to_vide", (x+movexy*help_movex, y+movexy*help_movey)])
                                                    except :
                                                        echec_pre_move[(x, y)] = [["move_to_vide", (x+movexy*help_movex, y+movexy*help_movey)]]
                                            elif my_color+"_" in ch_pions[(x+movexy*help_movex, y+movexy*help_movey)][0] :
                                                break
                                            else :
                                                ch_copy_pions = my_copy(ch_pions)
                                                ch_copy_pions[(x, y)], ch_copy_pions[(x+movexy*help_movex, y+movexy*help_movey)] = [], ch_copy_pions[(x, y)]
                                                if test_echec(ch_copy_pions) == False:
                                                    try :
                                                        len(echec_pre_move[(x, y)])
                                                        echec_pre_move[(x, y)].append(["move_to_eat", (x+movexy*help_movex, y+movexy*help_movey)])
                                                    except :
                                                        echec_pre_move[(x, y)] = [["move_to_eat", (x+movexy*help_movex, y+movexy*help_movey)]]
                                                break
                                        except :
                                            break

                        for move in [[(x, 0) for x in range(-1, -8, -1)], [(x, 0) for x in range(1, 8)], [(0, y) for y in range(-1, -8, -1)], [(0, y) for y in range(1, 8)]] :
                            for moveplus in move :
                                if cplateau[(x, 5)] == cvide :
                                    try :
                                        if len(ch_pions[(x+moveplus[0], y+moveplus[1])]) == 0 :
                                            ch_copy_pions = my_copy(ch_pions)
                                            ch_copy_pions[(x, y)], ch_copy_pions[(x+moveplus[0], y+moveplus[1])] = [], ch_copy_pions[(x, y)]
                                            if test_echec(ch_copy_pions) == False:
                                                try :
                                                    len(echec_pre_move[(x, y)])
                                                    echec_pre_move[(x, y)].append(["move_to_vide", (x+moveplus[0], y+moveplus[1])])
                                                except :
                                                    echec_pre_move[(x, y)] = [["move_to_vide", (x+moveplus[0], y+moveplus[1])]]
                                        
                                        elif my_color+"_" in ch_pions[(x+moveplus[0], y+moveplus[1])][0] :
                                            break
                                        else :
                                            ch_copy_pions = my_copy(ch_pions)
                                            ch_copy_pions[(x, y)], ch_copy_pions[(x+moveplus[0], y+moveplus[1])] = [], ch_copy_pions[(x, y)]
                                            if test_echec(ch_copy_pions) == False:
                                                try :
                                                    len(echec_pre_move[(x, y)])
                                                    echec_pre_move[(x, y)].append(["move_to_eat", (x+moveplus[0], y+moveplus[1])])
                                                except :
                                                    echec_pre_move[(x, y)] = [["move_to_eat", (x+moveplus[0], y+moveplus[1])]]
                                            break
                                    except :
                                        break






        if len(echec_pre_move) == 0 :
            echec_et_mat = king_coords
            a_moi_djouer = False
            print("fin")
        else :
            echec = king_coords

















def ajout_pre_move_visualisation(x, y) :
    global cplateau, coords_pre_move, coords_select, ch_pions
    coords_pre_move = []
    coords_select = (x, y)
    if len(ch_pions[(x, y)]) == 0 :
        return
    if echec != None :
        try :
            for k in range(len(echec_pre_move[(x, y)])) :
                coords_pre_move.append([echec_pre_move[(x, y)][k][0], echec_pre_move[(x, y)][k][1]])
        except :
            pass
        return
    
    if "pawn" in ch_pions[(x, y)][0] and my_color+"_" in ch_pions[(x, y)][0] :
        if y == 1 :
            dos = 3
        else :
            dos = 2
        for move in range(1, dos) :
            try :
                if cplateau[(x, 5)] == cvide :
                    if len(ch_pions[(x, y+move)]) == 0 :
                        coords_pre_move.append(["move_to_vide", (x, y+move)])
                    else :
                        break
            except :
                pass

        for move in [(1, 1), (-1, 1)] :
            try :
                if cplateau[(x, 5)] == cvide :
                    if len(ch_pions[(x+move[0], y+move[1])]) != 0 and my_color+"_" not in ch_pions[(x+move[0], y+move[1])][0]:
                        coords_pre_move.append(["move_to_eat", (x+move[0], y+move[1])])
            except :
                pass

    elif "knight" in ch_pions[(x, y)][0] and my_color+"_" in ch_pions[(x, y)][0] :
        help_var_knight = [(-2, 1), (-2, -1), (-1, -2), (1, -2), (2-1), (2, 1), (1, 2), (-1, 2)]
        for move in help_var_knight :
            if cplateau[(x, 5)] == cvide:
                try :
                    if len(ch_pions[(x+move[0], y+move[1])]) == 0 :
                        coords_pre_move.append(["move_to_vide", (x+move[0], y+move[1])])
                    elif my_color+"_" not in ch_pions[(x+move[0], y+move[1])][0] :
                        coords_pre_move.append(["move_to_eat", (x+move[0], y+move[1])]) #appliquer un filtre jaune
                except :
                    pass

    elif "rook" in ch_pions[(x, y)][0] and my_color+"_" in ch_pions[(x, y)][0] :

        for move in [[(x, 0) for x in range(-1, -8, -1)], [(x, 0) for x in range(1, 8)], [(0, y) for y in range(-1, -8, -1)], [(0, y) for y in range(1, 8)]] :
            for moveplus in move :
               if cplateau[(x, 5)] == cvide :
                   try :
                        if len(ch_pions[(x+moveplus[0], y+moveplus[1])]) == 0 :
                            coords_pre_move.append(["move_to_vide", (x+moveplus[0], y+moveplus[1])])
                        
                        elif my_color+"_" in ch_pions[(x+moveplus[0], y+moveplus[1])][0] :
                            break
                        else :
                            coords_pre_move.append(["move_to_eat", (x+moveplus[0], y+moveplus[1])]) #appliquer un filtre jaune
                            break
                   except :
                       break

    elif "king" in ch_pions[(x, y)][0] and my_color+"_" in ch_pions[(x, y)][0] :

       for movex in [-1, 0, 1] :
           for movey in [-1, 0, 1] :
               if cplateau[(x, 5)] == cvide and not (movex == 0 and movey == 0):
                   try :
                       if len(ch_pions[(x+movex, y+movey)]) == 0 :
                           coords_pre_move.append(["move_to_vide", (x+movex, y+movey)])
                       elif my_color+"_" not in ch_pions[(x+movex, y+movey)][0] :
                           coords_pre_move.append(["move_to_eat", (x+movex, y+movey)]) #appliquer un filtre jaune
                   except :
                       pass

    elif "bishop" in ch_pions[(x, y)][0] and my_color+"_" in ch_pions[(x, y)][0] :

        for help_movex in [-1, 1] :
            for help_movey in [-1, 1] :
                for movexy in range(1, 9) :
                    if cplateau[(x, 5)] == cvide :
                        try :
                            if len(ch_pions[(x+movexy*help_movex, y+movexy*help_movey)]) == 0 :
                                coords_pre_move.append(["move_to_vide", (x+movexy*help_movex, y+movexy*help_movey)])
                            elif my_color+"_" in ch_pions[(x+movexy*help_movex, y+movexy*help_movey)][0] :
                                break
                            else :
                                coords_pre_move.append(["move_to_eat", (x+movexy*help_movex, y+movexy*help_movey)]) #appliquer un filtre jaune
                                break
                        except :
                            break

    elif "queen" in ch_pions[(x, y)][0] and my_color+"_" in ch_pions[(x, y)][0] :

        for help_movex in [-1, 1] :
            for help_movey in [-1, 1] :
                for movexy in range(1, 9) :
                    if cplateau[(x, 5)] == cvide :
                        try :
                            if len(ch_pions[(x+movexy*help_movex, y+movexy*help_movey)]) == 0 :
                                coords_pre_move.append(["move_to_vide", (x+movexy*help_movex, y+movexy*help_movey)])
                            elif my_color+"_" in ch_pions[(x+movexy*help_movex, y+movexy*help_movey)][0] :
                                break
                            else :
                                coords_pre_move.append(["move_to_eat", (x+movexy*help_movex, y+movexy*help_movey)]) #appliquer un filtre jaune
                                break
                        except :
                            break

        for move in [[(x, 0) for x in range(-1, -8, -1)], [(x, 0) for x in range(1, 8)], [(0, y) for y in range(-1, -8, -1)], [(0, y) for y in range(1, 8)]] :
            for moveplus in move :
               if cplateau[(x, 5)] == cvide :
                   try :
                        if len(ch_pions[(x+moveplus[0], y+moveplus[1])]) == 0 :
                            coords_pre_move.append(["move_to_vide", (x+moveplus[0], y+moveplus[1])])
                        
                        elif my_color+"_" in ch_pions[(x+moveplus[0], y+moveplus[1])][0] :
                            break
                        else :
                            coords_pre_move.append(["move_to_eat", (x+moveplus[0], y+moveplus[1])]) #appliquer un filtre jaune
                            break
                   except :
                       break
    else :
        coords_select = None


def ajout_connect_pions(x, col) :
    global cplateau
    for k in range(6) :
        if cplateau[(x, k)] == cvide :
            if col == "w" :
                cplateau[(x, k)] = cred
                break
            else :
                cplateau[(x, k)] = cyel
                break

def test_win_connect(x) :
    if my_color == "b" :
        color_here = cyel
    else :
        color_here = cred
    for k in range(5, -1, -1) :
        if cplateau[(x, k)] == color_here :
            y = k
            break
#check vartical
    cumul_var = 1
    for k in range(1, 4) :
        try :
            if cplateau[(x, y-k)] == color_here :
                cumul_var+=1
                if cumul_var == 4 :
                    return True
            else :
                break
        except :
            break


#check horizontal
    cumul_var = 1
    for k in range(1, 4) :
        try :
            if cplateau[(x-k, y)] == color_here :
                cumul_var+=1
                if cumul_var == 4 :
                    return True
            else :
                break
        except :
            break
    for k in range(1, 4) :
        try :
            if cplateau[(x+k, y)] == color_here :
                cumul_var+=1
                if cumul_var == 4 :
                    return True
            else :
                break
        except :
            break


#chack diagonal
    cumul_var = 1
    for k in range(1, 4) :
        try :
            if cplateau[(x-k, y-k)] == color_here :
                cumul_var+=1
                if cumul_var == 4 :
                    return True
            else :
                break
        except :
            break
    for k in range(1, 4) :
        try :
            if cplateau[(x+k, y+k)] == color_here :
                cumul_var+=1
                if cumul_var == 4 :
                    return True
            else :
                break
        except :
            break

    cumul_var = 1
    for k in range(1, 4) :
        try :
            if cplateau[(x-k, y+k)] == color_here :
                cumul_var+=1
                if cumul_var == 4 :
                    return True
            else :
                break
        except :
            break
    for k in range(1, 4) :
        try :
            if cplateau[(x+k, y-k)] == color_here :
                cumul_var+=1
                if cumul_var == 4 :
                    return True
            else :
                break
        except :
            break
    return False


def my_copy(dict) :
    dict2 = {}
    for key in dict.keys() :
        dict2[key] = dict[key]
    return dict2

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
        X, Y= pygame.mouse.get_pos()
        for y in range(8) :
            for x in range(8) :
            
                if 74+x*104 < X < 74+(x+1)*104 and 955-(y+1)*104 < Y < 955-y*104 and a_moi_djouer :
                    if pygame.mouse.get_pressed()[0] and hold_clic == False :
                        if (x, y) in [k[1] for k in coords_pre_move] :
                            a_moi_djouer = False
                            coords_pre_move = []
                            dat = codes[1]+" "+str(coords_select[0])+" "+str(coords_select[1])+" "+str(x)+" "+str(y)
                            con_serv.send(dat.encode("utf8"))
                            ch_pions[coords_select], ch_pions[(x, y)] = [], ch_pions[coords_select]
                            
                            ajout_connect_pions(coords_select[0], my_color)
                            win = test_win_connect(coords_select[0])
                            coords_select = None
                            if win :
                                print("fin")
                            echec = None
                        else :
                            ajout_pre_move_visualisation(x, y)
                            coords_select = (x, y)
                        

        window.blit(bg_in_game, (0,0))

        #affichage des boards
        window.blit(chess_board, (54, 114)) 
        window.blit(connect_board, (1015, 219)) 
        #affichage pions chess
        if coords_select != None and len(ch_pions[coords_select]) != 0 and my_color+"_" in ch_pions[coords_select][0] and cplateau[(coords_select[0], 5)] == cvide:
            window.blit(pion_selected, (74+coords_select[0]*104, 851-coords_select[1]*103))
        for y in range(8) :
            for x in range(8) :
                if len(ch_pions[(x,y)]) != 0 :
                    window.blit(ch_pions[(x,y)][1], (74+x*104, 851-y*103))

        for im in coords_pre_move :
            if im[0] == "move_to_vide" :
                window.blit(going_to_move, (74+im[1][0]*104, 851-im[1][1]*103))
            else :
                window.blit(going_to_eat, (74+im[1][0]*104, 851-im[1][1]*103))
        if echec != None:
            window.blit(eche, (74+echec[0]*104, 851-echec[1]*103))
        if echec_et_mat != None :
            window.blit(eche_mat, (74+echec_et_mat[0]*104, 851-echec_et_mat[1]*103))

        #affichage pions connect
        for y in range(cplat_size[1]) :
            for x in range(cplat_size[0]) :
                window.blit(cplateau[(x,y)], (1034+x*104, 757-y*104))
        pygame.display.flip()
os._exit(1)

""" touche affilié à quelle player :
zqsd = player 1
sourie : {mouse_up, clic gauche, mouse_doawn, clic droit} = player 2
flèche directionnel = player 3
jn,; ou ijkl = player 4
"""
