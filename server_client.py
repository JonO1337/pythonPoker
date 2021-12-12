import socket
HEADERSIZE =8
ip = input("ip: ")
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((ip, 1234))


while True:
    msg = s.recv(HEADERSIZE)
    msglen = int(msg[:HEADERSIZE])    
    full_msg = s.recv(msglen).decode("utf-8")
    if full_msg == "send":
        msg = input()
        msg = f"{len(msg):<{HEADERSIZE}}"+msg
        s.send(bytes(msg,"utf-8"))
    else:
        print(full_msg,end="")