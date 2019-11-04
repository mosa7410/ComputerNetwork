import socket
import ssl
import sys
import base64

def recv_msg(client_socket):
    message = client_socket.recv(1024)
    print('S : ' + str(message) + '\r\n')


def main():
    if len(sys.argv) != 3:
        print('python3 smtp_socket.py [ID] [PASSWORD]')
        sys.exit()
        
    hostname = 'smtp.naver.com'
    portNumber = '465'
    context = ssl.create_default_context()
    client_sock = socket.create_connection((hostname, portNumber))
    ssl_client_sock = context.wrap_socket(client_sock, server_hostname = hostname)

    recv_msg(ssl_client_sock)
    
    data = 'EHLO naver.com\r\n'
    print('C : ' + data)
    ssl_client_sock.send((data).encode())

    recv_msg(ssl_client_sock)
    
    data = 'AUTH LOGIN\r\n'
    print('C : ' + data)
    ssl_client_sock.send((data).encode())

    recv_msg(ssl_client_sock)
    
    naverid = base64.b64encode((sys.argv[1]).encode())
    naverid = naverid.decode() + '\r\n'
    print('C : ' + naverid)
    ssl_client_sock.send(naverid.encode())
    
    recv_msg(ssl_client_sock)

    naverpass = base64.b64encode((sys.argv[2]).encode())
    naverpass = naverpass.decode() + '\r\n'
    print('C : ' + naverpass)
    ssl_client_sock.send(naverpass.encode())

    recv_msg(ssl_client_sock)
    
    mail_from = input('C : MAIL FROM: ')
    mail_from = 'MAIL FROM: ' + mail_from + '\r\n'
    ssl_client_sock.send(mail_from.encode())
    print('')
    
    recv_msg(ssl_client_sock)

    rcpt_to = input('C : RCPT TO: ')
    rcpt_to = 'RCPT TO: ' + rcpt_to + '\r\n'
    ssl_client_sock.send(rcpt_to.encode())
    print('')

    recv_msg(ssl_client_sock)
    
    data = 'DATA\r\n'
    print('C : ' + data)
    ssl_client_sock.send(data.encode())

    recv_msg(ssl_client_sock)
    
    subject = input('C : SUBJECT: ')
    subject = 'SUBJECT: ' + subject + '\r\n'
    ssl_client_sock.send(subject.encode())
    print('')
    
    fr = input('C : FROM: ')
    fr = 'FROM: ' + fr + '\r\n'
    ssl_client_sock.send(fr.encode())
    print('')
    
    to = input('C : TO: ')
    to = 'TO: ' + to + '\r\n'
    ssl_client_sock.send(to.encode())
    print('')
    
    con = input('C : ')
    con = con + '\r\n'
    ssl_client_sock.send(con.encode())
    print('')
    
    while con != '.\r\n':
        con = input('C : ')
        con = con + '\r\n'
        ssl_client_sock.send(con.encode())

    print('')
    
    recv_msg(ssl_client_sock)

    q = input('C : ')
    q = q + '\r\n'
    ssl_client_sock.send(q.encode())
    ssl_client_sock.close()
    

if __name__ == "__main__" :
    main()

