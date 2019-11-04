import socket
import threading
import sys

recvdata = []
def recv_msg(client_socket):
    global recvdata
    while True:
        message = client_socket.recv(1024).decode()
        print(message)

        for i in range(len(recvdata)):
            if recvdata[i] is None :
                break
            recvdata[i].send((message).encode())

        if message[9:13].lower() == 'quit':
            break

    print('Client Disconnected')

def send_msg():
    global recvdata
    while True:
        message = input('')
        for i in range(len(recvdata)) :
            sendmsg = '[Server] ' + message
            recvdata[i].send((sendmsg).encode())

        if message[0:4].lower() == 'quit':
            break

def main():
    if len(sys.argv) != 2:
        print("python chat_server.py [PORTNUMBER]")
        sys.exit()

    port_number = int(sys.argv[1])

    chat_server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    chat_server_socket.bind(('',port_number))
    chat_server_socket.listen(5)

    while True :
        (client_socket, addr) = chat_server_socket.accept()
        print('Client connect')

        threading.Thread(target = recv_msg, args = (client_socket,)).start()
        recvdata.append(client_socket)

        threading.Thread(target = send_msg ).start()

    print('Client Disconnected')
    chat_server_socket.close()

if __name__ == "__main__":
    main()
