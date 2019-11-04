import socket
import select
import sys

socket_list = []
def main():
    if len(sys.argv) != 2:
        print("python chat_server_s.py [PORTNUMBER]")
        sys.exit()

    port_number = int(sys.argv[1])

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # set socket option
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind(('', port_number))
    server_socket.listen(5)

    # add server socket object to the list
    socket_list.append(server_socket)

    while True:
        # get the list sockets which are ready to be read through select
        read_sockets, write_sockets, error_sockets = select.select(socket_list, [], [])
        for tempsocket in read_sockets:
            # a new client connection request recieved
            if tempsocket == server_socket:
                client_socket, addr = server_socket.accept()
                socket_list.append(client_socket)
                print("Client connect")

            # message from client
            else:
                try:
                    # recieve data from socket
                    data = tempsocket.recv(1024)
                    if data:
                        # send message to all connected clients
                        broadcast(server_socket, tempsocket, "[Client]" + data.decode())
                    else:
                        # if socket broke, remove
                        if tempsocket in socket_list:
                            socket_list.remove(tempsocket)
                except:
                    continue

    server_socket.close()

# send message to all connect clients
def broadcast(server_socket, tempsocket, message):
    for socket in socket_list:
        # not server and not me
        if socket != server_socket and socket != tempsocket:
            try:
                # send mesage
                socket.send(message.encode())
            except:
                # if socket broke, remove
                socket.close()
                if socket in socket_list:
                    socket_list.remove(socket)


if __name__ == "__main__":
    main()
