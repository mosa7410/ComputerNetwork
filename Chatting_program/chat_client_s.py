import socket
import select
import sys

def main():
    if len(sys.argv) != 3:
        print('python chat_client_s.py [IPADDRESS] [PORTNUMBER]')
        sys.exit()

    ip_address = sys.argv[1]
    port_number = int(sys.argv[2])
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # set a time limit for a recv method
    client_socket.settimeout(2)

    # connect
    try:
        client_socket.connect((ip_address, port_number))
        print("Host connect")
    except:
        print("Unable to connect")
        sys.exit()

    # remove the contents of the buffer
    sys.stdout.flush()

    while True:
        socket_list = [sys.stdin, client_socket]
        # get the list sockets which are readable
        read_sockets, write_sockets, error_sockets = select.select(socket_list, [], [])

        for sock in read_sockets:
            if sock == client_socket:
                # recieve message from server
                data = sock.recv(1024)
                if not data:
                    sys.exit()
                else:
                    # print data
                    sys.stdout.write(data.decode())
                    sys.stdout.flush()
            else:
                # insert data
                message = sys.stdin.readline()
                # send data for server
                client_socket.send(message.encode())
                sys.stdout.flush()


if __name__ == "__main__":
    main()
