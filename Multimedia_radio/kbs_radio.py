import subprocess
import time
import os
import signal
import mutagen
import mutagen.mp3
from mutagen.easyid3 import EasyID3
from time import localtime, strftime

def main () :
    presentTime = strftime('%Y%m%d%H%M%S', localtime())
    presentDate = strftime('%Y%m%d', localtime())
    radiofile_name = 'pcm:file=/home/ahnje/Desktop/CN/HW10/' +  presentTime + '_KBS.mp3'
    addr = "http://onair.kbs.co.kr/index.html?sname=onair&stype=live&ch_code=24&ch_type=radioList"

    url = ['curl', '-s', addr]
    grep = 'grep service_url'.split()
    tail = 'tail -1'.split()
    cut = 'cut -d\" -f16'.split()
    cut1 = 'cut -d\\ -f1'.split()
    
    url_data = subprocess.Popen(url, stdout=subprocess.PIPE).stdout
    grep_data = subprocess.Popen(grep, stdin=url_data, stdout=subprocess.PIPE).stdout
    url_data.close()
    tail_data = subprocess.Popen(tail, stdin=grep_data, stdout=subprocess.PIPE).stdout
    grep_data.close()
    cut_data = subprocess.Popen(cut, stdin=tail_data, stdout=subprocess.PIPE).stdout
    tail_data.close()
    cut1_data = subprocess.Popen(cut1, stdin=cut_data, stdout=subprocess.PIPE).stdout
    cut_data.close()

    result_url = cut1_data.read().decode()
    result_url = result_url.replace('\n', '')
    cut1_data.close()
    print(result_url)

    kbs_radio = ['mplayer', result_url, '-ao', radiofile_name, '-vc', 'dummy', '-vo', 'null']

    p = subprocess.Popen(kbs_radio)
    p.communicate()
    #time.sleep(5)
    #os.killpg(p.pid, signal.SIGKILL)

    filepath = '/home/ahnje/Desktop/CN/HW10/' + presentTime + '_KBS.mp3'
    try :
        meta = EasyID3(filepath)
    except mutagen.id3.ID3NoHeaderError :
        meta = mutagen.File(filepath, easy = True)
        meta.add_tags()

    meta['title'] = presentDate + 'Ahnjeongeun'
    meta['artist'] = '201602021'
    meta['genre'] = 'KBS_RADIO'
    meta.save()

if __name__ == "__main__" :
    main()
