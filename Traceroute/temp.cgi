#!/usr/bin/python3

import cgi, cgitb
import sys
import subprocess
import pygeoip

form = cgi.FieldStorage()

print("Content-type:text/html")
print()
print('<html>')
print('<head>')
print('<meta charset="utf-8">')
print('<title>Hello Map</title>')
print('</head>')

print('<body>')
print('<h3>Traceroute - Visualize on Kakao Map</h3>')
print('<form method="get" action="temp.cgi">')
print('<input type="text" name="target"/>', '<input type="submit" value="Submit"/>')
print('</form>')

host = form.getvalue('target')

print('<div id = "map" style = "width:500px; height:400px;"></div>')
print('<script type = "text/javascript" src = "//dapi.kakao.com/v2/maps/sdk.js?appkey=35923f873b69a55a8172418558e261cb"></script>')
print('<script> var container = document.getElementById("map"); var options = { center: new daum.maps.LatLng(36.35111, 127.38500), level : 13 }; var map = new daum.maps.Map(container, options); </script>')
print('<script> var imageSrc = "http://t1.daumcdn.net/localimg/localimages/07/mapapidoc/markerStar.png"; var imageSize = new daum.maps.Size(24, 35); var markerImage = new daum.maps.MarkerImage(imageSrc, imageSize); </script>')

if host != None :
    print('<h3>[Destination] ',host,'</h3>')
    
    proc = subprocess.Popen(["traceroute", "-m", "30", host], stdout = subprocess.PIPE, stderr = subprocess.STDOUT)
    
    iplist = iter(proc.stdout.readline, "")
    
    next(iplist)
    
    for line in iplist :
        sen = line.decode("utf-8")
        if sen == '' : break
        sen = sen.replace("\n", "")
        IPadr = sen.split(" ")
        while "" in IPadr :
            IPadr.remove("")

        if IPadr[1] != "*" :
            gi = pygeoip.GeoIP('GeoLiteCity.dat')
            cityloc = gi.record_by_addr(str(IPadr[1]))

            if cityloc != None :
                print('<p>[IP] ', str(IPadr[1]),',  Lat : ',str(cityloc['latitude']),',  Lon : ',str(cityloc['longitude']),'</p>')
                print('<script>var marker = new daum.maps.Marker({ map:map, position:new daum.maps.LatLng(',str(cityloc['latitude']),', ',str(cityloc['longitude']),'), image: markerImage }); </script>')

print('</body>')
print('</html>')

