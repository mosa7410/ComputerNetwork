import socket
import ssl
import sys
import base64

def recv_msg(client_socket):
    message = client_socket.recv(1024)
    print('S : ' + message.decode() + '\r\n')

def main():
    if len(sys.argv) != 3:
        print('python3 pop3_socket.py [ID] [PASSWORD]')
        sys.exit()
        
    hostname = 'pop.naver.com'
    portnumber = '995'
    context = ssl.create_default_context()
    client_sock = socket.create_connection((hostname, portnumber))

    ssl_client_sock = context.wrap_socket(client_sock, server_hostname = hostname)
    recv_msg(ssl_client_sock)

    user = 'user ' + sys.argv[1] + '\r\n'
    ssl_client_sock.send(user.encode())
    print('C : ' + user)

    recv_msg(ssl_client_sock)
    
    pssw = 'pass ' + sys.argv[2] + '\r\n'
    ssl_client_sock.send(pssw.encode())
    print('C : ' + pssw)

    recv_msg(ssl_client_sock)
    
    while True:
        data = input('C : ')
        data = data + '\r\n'
        ssl_client_sock.send(data.encode())
        print('')

        recv_msg(ssl_client_sock)


if __name__ == "__main__":
    main()
