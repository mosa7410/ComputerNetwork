import socket
import os

def main() :
    ip_address = '127.0.0.1'
    port_number = 1234

    server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_sock.bind((ip_address, port_number))
    print("Server socket open...")
    print("Listening...")

    server_sock.listen(5)

    while True :
        client_sock,addr = server_sock.accept()

        request = client_sock.recv(1024)
        request = request.decode()

        filedata = request.split('\r\n')[0].split(" ")

        n = filedata[1]
        if n[0:1] == "/" :
            n = n[1:len(n)]

        fp = str(n)

        if filedata[0] == "GET" and os.path.isfile(fp) == True :
            reheader = "HTTP/1.1 200 OK\r\nContent-Length:\r\n" + str(os.path.getsize(fp)) +"\n\n"
            #reheader = "HTTP/1.1 200 OK\r\nContent-Length:" + str(os.path.getsize(fp)) +"\r\n\n\n"
            f = open(fp,"rb")
            data = f.read()
            reheader = reheader.encode()
            reheader += data
            f.close()

        else :
            reheader = "HTTP/1.1 404 Not Found\r\n"
            reheader = reheader.encode()

        client_sock.send(reheader)
        client_sock.close()

    server_sock.close()

if __name__ == "__main__" :
    main()
