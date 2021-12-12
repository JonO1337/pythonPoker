import socket
import commons
import threading
import time
HEADERSIZE = 8
global waitingQueue
waitingQueue = commons.Queue(100)

def initSocket():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(("0.0.0.0", 1234))
    s.listen(5)
    while True:
        clientsocket ,address = s.accept()
        t1 = threading.Thread(target=login,args=(Client(clientsocket),))
        t1.start()
        print(f"Connection from {address} has been established.")

def login(client):
    try:
        client.sendMsg("Username : ")
        username = client.recive()
        client.sendMsg("Password : ")
        password = client.recive()
        bal= commons.validateCreds(username,password)
        if bal:
            waitingQueue.enqueue(commons.Player(username,bal,client))
        else:
            client.sendMsg("Failed to login")
            client.close()
    except:
        client.close()
        return



class Client:
    def __init__(self,socket):
        self.socket = socket
        self.socket.settimeout(300)
    def sendMsg(self,msg):
        msg = f"{len(msg):<{HEADERSIZE}}"+msg
        print(msg)
        self.socket.send(bytes(msg,"utf-8"))
    def recive(self):
        self.sendMsg("send")
        try:
            msg = self.socket.recv(HEADERSIZE)
            msglen = int(msg[:HEADERSIZE])
            full_msg = self.socket.recv(msglen).decode("utf-8")
        except TimeoutError:
            self.close()
            raise Exception
        return full_msg
    def close(self):
        self.socket.close()
