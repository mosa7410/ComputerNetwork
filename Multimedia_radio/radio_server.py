import socket
import os
from bs4 import BeautifulSoup
import shutil

def downloadRadio(data) :
    fileName = data.split("=")[0]
    return fileName

def fileList() :
    path_dir = '/home/ahnje/Desktop/CN/HW10/'
    file_list = os.listdir(path_dir)
    file_list.sort()
    downloadList = []

    for item in file_list:
        if item.find('mp3') is not -1:
            downloadList.append(item)

    with open("/home/ahnje/Desktop/CN/HW10/downloadRadioMP3.html", 'r') as fp :
        soup = BeautifulSoup(fp, features="html.parser")

    check = []
    prefile = soup.find_all('input')

    for name in prefile :
        filename = name.get('name')
        check.append(filename)

    soup = checkList(soup, downloadList, check)
    data = soup.prettify().encode()
    with open('/home/ahnje/Desktop/CN/HW10/downloadRadioMP3.html', 'wb') as file :
        file.write(b'')
        file.write(data)
        #print("IS PROBLEM?")

def checkList(soup, downloadList, check) :
    index = -1
    for item in downloadList:
        data = str(item)
        if data not in check :
            index = downloadList.index(item)
    if index is -1 :
        return soup
    new_p = soup.new_tag('div')
    soup.form.append(new_p)
    new_file = soup.new_tag('input')
    new_file.attrs = {'type': 'submit', 'name': str(downloadList[index]), 'value': str(downloadList[index]) }
    new_p.append(new_file)
    return soup

def main() :
    ip_address = ''
    port_number = 1234

    server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_sock.bind((ip_address, port_number))
    server_sock.listen()

    while True :
        client_sock, addr = server_sock.accept()
        request = client_sock.recv(1024)
        request = request.decode()

        filedata = request.split('\r\n')[0].split(" ")
        
        fileList()
        n = filedata[1] #html + ? + data
        file_name = ''
        downloadfile = ''

        if '?' in n:
            html = n.split("?")
            n = html[0]
            downloadfile = downloadRadio(html[1])
            print(downloadfile)

        if n[0:1] == "/" :
            n = n[1:len(n)]

        file_name = str(n)
        if filedata[0] == "GET" and os.path.isfile(file_name) == True :
            if downloadfile is not '' :
                shutil.copy('/home/ahnje/Desktop/CN/HW10/' + downloadfile, '/home/ahnje/Desktop/downloadRadioFile/' + downloadfile)
            reheader = "HTTP/1.1 200 OK\r\nContent-Length:\r\n" + str(os.path.getsize(file_name)) +"\n\n"
            f = open(file_name,"rb")
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
