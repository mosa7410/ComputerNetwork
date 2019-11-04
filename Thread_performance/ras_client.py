import time
import socket
from bs4 import BeautifulSoup

number = 0
downloadTime = 0
#parsing src from img tag
def parseHTML(fname) :
    with open(fname, "r") as fp :
        soup = BeautifulSoup(fp, features = "html.parser")

    img_list = soup.find_all("img")
    src_list = []
    for li in img_list :
        src_list.append(li.get('src'))
    return src_list

def main() :
    serverIP = '192.168.0.18'
    serverPort = 1234

    client_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_sock.connect((serverIP,serverPort))
    print("Connect to Server")

    #cln_msg = input()
    client_sock.send(("GET test_50kb.html HTTP/1.1").encode())
    
    #header or data
    res = (client_sock.recv(1024)).decode("utf-8")
    #HTTP/1.1~ , content~ , datasize + data
    redata = res.split("\r\n")
    
    # datasize + data
    data = redata[2].split("\n\n")
    
    # HTTP/1.1 200 or 404
    reheader = redata[0].split(" ")

    if reheader[1] == '404' :
        print('Cannot found')

    elif reheader[1] == '200' :
        title = "data.html"
        f = open(title, "w")
        if int(data[0]) <= 1024 :
            result = data[1]
            f.write(result)

        else :
            temp = data[1]
            data = data[1]
            while temp:
                temp = (client_sock.recv(1024)).decode("utf-8")
                data += temp
            f.write(data)

        f.close()
        client_sock.close()

        imglist = parseHTML(title)
        
        for imgname in imglist :
            downloadimg(imgname)

def downloadimg(img_name) :
    serverIP = '192.168.0.18'
    serverPort = 1234

    client_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_sock.connect((serverIP,serverPort))

    client_sock.send(("GET " + img_name + " HTTP/1.1").encode())
    res = client_sock.recv(1024)
    redata = res.split(b"\r\n")
    data = redata[2].split(b"\n\n")
    reheader = redata[0].split(b" ")

    if reheader[1] == b'404' :
        print('Cannot found')

    elif reheader[1] == b'200' :
        global number
        number += 1
        f = open("IMG" + str(number) + ".jpeg", "ab")

        if int(data[0]) <= 1024 :
            f.write(data[1])

        else :
            f.write(data[1])
            temp = data[1]
            while temp:
                temp = client_sock.recv(1024)
                f.write(temp)

        f.close()
        client_sock.close()


def getDownloadTime() :
    start_time = time.time()
    main()
    end_time = time.time()
    downloadTime = end_time - start_time

    return downloadTime

if __name__ == "__main__" :
    print(getDownloadTime())
