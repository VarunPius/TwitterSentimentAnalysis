import socket

HOST = "127.0.0.1"      # The server's hostname or IP address
PORT = 5555             # The port used by the server

s = socket.socket()
s.connect((HOST, PORT))
s.sendall(b"Hello, world")
try:
    while True:
        data = s.recv(1024)
        data = data.decode('utf-8')
        print(f"Received {data!r}")
finally:
    s.close()
    print("After close")