import socket
import json

hostIP = '127.0.0.1'
port = 35970

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((hostIP, port))
client_socket.settimeout(2.5)


def check_server(text, card):
    req = {"id": text, "card": card}
    data = json.dumps(req)
    client_socket.sendall(bytes(data, encoding='utf-8'))
    val = ""
    while True:
        try:
            dt = client_socket.recv(1024).decode('utf-8')
            val = val+dt
        except socket.timeout:
            break
    return val


def server_upt(text, card, contract, wallet):
    req = {"id": text, "card": card, "contract": contract, 'wallet': wallet}
    data = json.dumps(req)
    client_socket.sendall(bytes(data, encoding='utf-8'))
    val = ""
    try:
        val = client_socket.recv(1024).decode("utf-8")
    except socket.timeout:
        return val
    return val
