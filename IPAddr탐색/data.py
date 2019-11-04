import os
import pickle

def main() :
    f = open('oix-full-snapshot-2018-11-01-2200', 'rb')
    p = open('data.pickle', 'wb')
    for i in range(0, 5) :
        f.readline()

    datalist = []
    line = ''
    networkadr = ''
    weight = 0
    locprf = 0
    path = 0
    nextHop = ''

    line = f.readline()
    while True :
        if line is b'' or line is None :
            break
        init = [x for x in line.split(b' ') if x][1:]
        del(init[len(init)-1])
        
        networkadr = init[0]
        weight = int(init[4])
        locprf = int(init[3])
        path = len(init[5:])
        nextHop = init[1]

        nextline = f.readline()
        nextl = [x for x in nextline.split(b' ') if x][1:]
        del(nextl[len(nextl)-1])

        while networkadr == nextl[0] :
            if weight < int(nextl[4]) :
                line = nextline
                weight = int(nextl[4])
                locprf = int(nextl[3])
                path = len(nextl[5:])
                nextHop = nextl[1]

            elif weight == int(nextl[4]) :
                if locprf < int(nextl[3]) :
                    line = nextline
                    weight = int(nextl[4])
                    locprf = int(nextl[3])
                    path = len(nextl[5:])
                    nextHop = nextl[1]

                elif locprf == int(nextl[3]) :
                    if path > len(nextl[5:]) :
                        line = nextline
                        weight = int(nextl[4])
                        locprf = int(nextl[3])
                        path = len(nextl[5:])
                        nextHop = nextl[1]

            nextline = f.readline()
            if nextline is b'' or nextline is None :
                break
            nextl = [x for x in nextline.split(b' ') if x][1:]
            del(nextl[len(nextl)-1])

        data = (networkadr.decode(), nextHop.decode())
        datalist.append(data)
        #pickle.dump(data, p)
        #print(line)
        line = nextline

    pickle.dump(datalist, p)
    f.close()
    p.close()

if __name__ == '__main__' :
    main()
