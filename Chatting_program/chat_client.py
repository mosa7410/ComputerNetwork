import socket
import sys
import threading

def recv_message(message_socket):
    while True:
        message = message_socket.recv(1024)
        print(message.decode())
        if message[7:11].lower() == 'quit':
            break

    print('Host Disconnected')
    message_socket.close()

def main():
    if len(sys.argv) != 3:
        print('python chat_client.py [IPADDRESS] [PORTNUMBER]')
        sys.exit()

    ip_address = sys.argv[1]
    port_number = int(sys.argv[2])

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((ip_address, port_number))

    print('Host connect')

    threading.Thread(target = recv_message, args = (client_socket,)).start()

    while True:
        message = input('')
        send_msg = '[Client]' + str(message)
        client_socket.send(send_msg.encode())

        if message[0:4].lower() == 'quit':
            break

    print('Host Disconnected')
    client_socket.close()

if __name__ == "__main__":
    main()

