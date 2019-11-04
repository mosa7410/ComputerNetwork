import subprocess
import mutagen
import mutagen.mp3
from mutagen.easyid3 import EasyID3
from time import localtime, strftime

def main () :
    radio_addr = 'rtmp://58.229.187.11/iradio/iradiolive_m4a'
    presenttime = strftime('%Y%m%d%H%M%S', localtime())
    presentDate = strftime('%Y%m%d', localtime())
    downloadfile_name = '/home/ahnje/Desktop/CN/HW10/' + presenttime + '_ebs.flv'
    radiofile_name = '/home/ahnje/Desktop/CN/HW10/' + presenttime + '_EBS.mp3'

    rtmpdump = ['rtmpdump', '-r', radio_addr, '-B', '10', '-o', downloadfile_name]
    ffmpeg = ['ffmpeg', '-i', downloadfile_name, '-acodec', 'mp3', radiofile_name]

    p = subprocess.Popen(rtmpdump)
    p.communicate()
    p = subprocess.Popen(ffmpeg)
    p.communicate()

    filePath = radiofile_name

    try :
        meta = EasyID3(filePath)
    except mutagen.id3.ID3NoHeaderError :
        meta = mutagen.File(filePath, easy = True)
        meta.add_tags()

    meta['title'] = presentDate + 'Ahnjeongeun'
    meta['artist'] = '201602021'
    meta['genre'] = 'EBS_RADIO'
    meta.save()

if __name__ == "__main__" :
    main()
