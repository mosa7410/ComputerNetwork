import socket
import ssl
import sys
import base64

def recv_msg(client_socket):
    message = client_socket.recv(5000)

    print('S : ' + message.decode() + '\r\n')

def main():
    if len(sys.argv) != 3:
        print('python3 imap_socket.py [ID] [PASSWORD]')
        sys.exit()

    hostname = 'imap.naver.com'
    portnumber = '993'
    context = ssl.create_default_context()
    client_sock = socket.create_connection((hostname, portnumber))
    ssl_client_sock = context.wrap_socket(client_sock, server_hostname = hostname)

    recv_msg(ssl_client_sock)

    logindata = 'a login ' + sys.argv[1] + ' ' + sys.argv[2] + '\r\n'
    print('C : ' + logindata)
    ssl_client_sock.send(logindata.encode())

    recv_msg(ssl_client_sock)

    while True:
        data = input('C : ')
        data = data + '\r\n'
        ssl_client_sock.send(data.encode())
        print('')

        recv_msg(ssl_client_sock)

if __name__ == "__main__":
    main()

