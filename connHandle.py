import socket
import commons
HEADERSIZE = 8
global waitingQueue
waitingQueue = commons.Queue(100)

def initSocket():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((socket.gethostname(), 1234))
    s.listen(5)
    while True:
        clientsocket ,address = s.accept()
        waitingQueue.enqueue(Client(clientsocket))
        print(f"Connection from {address} has been established.")


class Client:
    def __init__(self,socket):
        self.socket = socket
    def sendMsg(self,msg):
        msg = f"{len(msg):<{HEADERSIZE}}"+msg
        print(msg)
        self.socket.send(bytes(msg,"utf-8"))
    def recive(self):
        self.sendMsg("send")
        msg = self.socket.recv(HEADERSIZE)
        msglen = int(msg[:HEADERSIZE])
        full_msg = self.socket.recv(msglen).decode("utf-8")
        return full_msg
