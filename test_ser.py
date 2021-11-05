import socket

def run_server(HOST = "192.168.219.108", PORT=55555):
    with socket.socket() as s:
        s.bind((HOST,PORT))
        s.listen(1)

        conn,addr = s.accept()
        msg = conn.recv(1024)
        print(f'{msg.decode()}')
        conn.sendall(msg)
        conn.close()