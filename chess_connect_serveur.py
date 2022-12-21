from random import randint
import socket
import threading
import sys
from datetime import datetime
import traceback

##listes/variables
codes = ["lance_le_jeu", #0
        "je_joue", #1
        "fin_du_jeu" #2
        ] #codes pour communiqué avec le serveur




conn = []
adresse = []
message = []





historique = open("./historique connexion.txt", "a")
historique.write("\n\n~~~~~~~~~~~~~~~~~~~~~~~~~~ALLUMAGE SERVEUR le "+str(datetime.now())+" ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
historique.close()

##fonctions secondaire




def goto_commande(com, idUser) :
    # global
    print("comiku : ", com)
    if com[0] in codes[1] :
        dat = " ".join(com)
        if idUser == 0 :
            message[1].append(dat)
        else :
            message[0].append(dat)
    




##classe qui reçois les messages
class RecoiInfo(threading.Thread) :
    def __init__(self):
        threading.Thread.__init__(self)
    def run(self) :
        idUser = len(conn)-1
        while True :
            try :
                data = conn[idUser].recv(1024)
                data = data.decode("utf8")
                if data == "" :
                    break
                else :
                    goto_commande(data.split(" "), idUser)
            except Exception :
                traceback.print_exc()
                break
        print("<system> :  viens de ce déconnecter")
        conn[idUser] = None

        sys.exit()





##classe qui evoi les messages 
class EnvoiInfo(threading.Thread) :
    def __init__(self):
        threading.Thread.__init__(self)
    def run(self) :
        try :
            idUser = len(conn)-1
            message.append([])
            while conn[idUser] != None :
                if len(message[idUser]) != 0 :
                    try :
                        print("sys_envoi_vers  : ",message[idUser][0])
                    except :
                        print("sys_envoi_vers [idUser-:-"+str(idUser)+"] : ",message[idUser][0])
                    if conn[idUser] != None:
                        conn[idUser].send(message[idUser][0].encode("utf8"))
                    message[idUser].pop(0)
        except Exception:
            traceback.print_exc()
            print("bug du ", idUser)
            sys.exit()


##Connection
def connection():
    for k in range(2) :
        socket.listen()
        con, adrese = socket.accept()
        conn.append(con)
        adresse.append(adrese)
        EnvoiInfo().start()
        RecoiInfo().start()
    if randint(0,1) == 0 :
        prout = ("w", "b")
    else :
        prout = ("b", "w")
    message[0].append(codes[0]+" "+prout[0])
    message[1].append(codes[0]+" "+prout[1])
    sys.exit()

host, port = ("", 5555)

socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socket.bind((host, port))
print("<system> : connexion établie")


##Threads
thead_listen = threading.Thread(target=connection)

thead_listen.start()