import sqlhelper
import socket
import json

port = 35970
sql = sqlhelper
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(("127.0.0.1", port))
server_socket.listen(5)
server_socket.settimeout(2.5)
clients = {}
requests_dict = {'exist': lambda data2: sql.get_exists(data2['card']),
                 'create': lambda data2: str(sql.new_card()),
                 'getinfo': lambda data2: str(sql.get_card_info(data2['card'])),
                 'update': lambda data2: sql.add_update_card(data2['card'], data2['contract'], data2['wallet']),
                 'load': lambda data2: sql.get_all_cards()}


# handel requests from the client pull/push relevant data to the sql database
def handle_request(data2):
    if data2['id'] in requests_dict.keys():
        return requests_dict[data2['id']](data2)
    else:
        return 'Not a valid server request type'


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    while True:
        # adding clients to clients que
        try:
            client, address = server_socket.accept()
            if client not in clients:
                clients[client] = address
                client.settimeout(2.5)
        except socket.timeout:
            print("No accept. Timed out.")
        del_keys = []
        # handle waiting clients
        if clients:
            for c in clients:
                try:
                    data = c.recv(1024).decode('utf-8')
                    try:
                        d = json.loads(data)
                        c.sendall(bytes(handle_request(d), encoding='utf-8'))
                    except ValueError:
                        print('invalid data')
                        c.sendall(bytes('data error', encoding='utf-8'))
                except socket.timeout:
                    print("no massages from client", clients[c])
                except ConnectionError:
                    print(f"{clients[c]} has disconnected.")
                    del_keys.append(c)
            for i in del_keys:
                del clients[i]
