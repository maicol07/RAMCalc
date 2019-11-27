import socket
def Risposta():

s=socket.socket()
hostname=socket.gethostname()
ip=socket.gethostbyname(hostname)
s.bind((ip,888))
print(f"L'indirizzo ip di questo server è: {ip}")
s.listen(100)
conn, ip_client=s.accept()
while True:
    r=conn.recv(100)
    richiesta=r.decode()
    conn.send(risposta.encode())




