from socket import *
from phue import Bridge

b = Bridge('192.168.0.19')
b.connect()
lights = b.lights

def controllerLight(lightID, data) :
    lightID = int(lightID)
    if 'set' in data[2] :
        if data[3] in 'on':
            lights[lightID-1].on = True
        elif data[3] in 'off':
            lights[lightID-1].on = False
    elif 'brightness' in data[2] :
        lights[lightID-1].brightness = int(data[3])

    elif 'color' in data[2] :
        x = float(data[3])
        y = float(data[4])
        if x is not '' and y is not '':
            lights[lightID-1].xy = [x, y]
        return

def main() :
    portNumber = 6667
    servername = 'chat.freenode.net'

    sock = socket(AF_INET, SOCK_STREAM)
    sock.connect((servername, portNumber))

    sock.send("NICK U201600000\r\n".encode())
    sock.send("USER U201600000 U201600000 U201600000 :cnu bot\r\n".encode())
    sock.send("JOIN #CNU\r\n".encode())

    while True :
        text = sock.recv(4096)
        text = text.decode()

        if text.find("U201602021") != -1 :
            text = text.replace('\r\n', '')
            data = text.split(':')
            data = data[2].split(' ')

            if data[0] in 'hue' and len(data) > 3:
                lightID = data[1]
                controllerLight(lightID, data)
    sock.close()

if __name__ == "__main__" :
    main()
