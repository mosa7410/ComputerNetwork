from phue import Bridge
import socket
import os

#b = Bridge('192.168.0.19')
#b.connect()
#lights = b.lights

def controllerlight(lightID, data):
    b = Bridge('192.168.0.19')
    b.connect()
    lights = b.lights

    lightID = int(lightID)
    for i in range(len(data)) :
        if 'check' in data[i] :
            if data[i].split('=')[1] == 'on' :
                lights[lightID-1].on = True
            elif data[i].split('=')[1] == 'off' :
                lights[lightID-1].on = False

        elif 'brightness' in data[i] :
            bri = int(data[i].split('=')[1])
            if bri != -1 :
                lights[lightID-1].brightness = bri
            
        elif 'color' in data[i] and 'color' in data[i+1] :
            x = data[i].split('=')[1]
            y = data[i+1].split('=')[1]
            if x is not '' and y is not '' :
                lights[lightID-1].xy = [float(x), float(y)]
            return;

def main() :
    ip_address = '192.168.0.18'
    port_number = 1234

    server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_sock.bind((ip_address, port_number))
    server_sock.listen()

    while True :
        client_sock, addr = server_sock.accept()
        request = client_sock.recv(1024)
        request = request.decode()

        filedata = request.split('\r\n')[0].split(" ")

        n = filedata[1]

        if '?' in filedata[1]:
            html = (filedata[1]).split("?")
            data = html[1].split("&")
            controllerlight(data[0][0], data[1:])
            n = html[0]

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
