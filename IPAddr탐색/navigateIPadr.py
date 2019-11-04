import os
import pickle
import time

class convertBin(object) :
    def convert(self, networkIP) :
        data = []
        if '/' in networkIP :
            networkid = (networkIP.split('/')[0]).split('.')
            mask = int(networkIP.split('/')[1])
            for i in range(len(networkid)) :
                b = bin(int(networkid[i]))[2:].zfill(8)
                data.append(b)
            return "".join(data)[:mask]
        else :
            networkid = networkIP.split('.')
            for i in range(len(networkid)) :
                b = bin(int(networkid[i]))[2:].zfill(8)
                data.append(b)
            return "".join(data)

class Node(object) :
    def __init__(self, key, data=None) :
        self.key = key
        self.data = data
        self.child = {}

class Trie(object) :
    def __init__(self) :
        self.root = Node(None)

    def insert(self, networkIP, nextHop) :
        p = self.root
        b = convertBin()
        network_bit = b.convert(networkIP)

        for i in str(network_bit) :
            if i not in p.child :
                p.child[i] = Node(i)
            p = p.child[i]
        p.data = nextHop

    def search(self, networkIP) :
        p = self.root
        b = convertBin()
        network_bit = b.convert(networkIP)
        
        for i in str(network_bit) :
            if i in p.child :
                p = p.child[i]
            else :
                if p.data is not None :
                    return (networkIP, p.data)
                return (networkIP, None)

        if p.data is not None :
            return (networkIP, p.data)
        else :
            return (networkIP, None)

class createTrieTree(object) :
    def __init__(self) :
        self.T = Trie()

    def createTree(self) :
        datalist = []

        t = self.T
        if os.path.isfile('data.pickle') :
            with open('data.pickle', 'rb') as f :
                filedata = pickle.load(f)
                ip_datalist = dict(filedata)
                networkID = list(ip_datalist.keys())

                for data in networkID :
                    value = ip_datalist.get(data)
                    t.insert(data, value)

    def searchIP(self) :
        datalist = []
        t = self.T
        if os.path.isfile('random_ip_list.pickle') :
            with open('random_ip_list.pickle', 'rb') as f :
                randomIP = pickle.load(f)
                #timestamp start
                starttime = time.time()
                for i in range(len(randomIP)) :
                    temp = t.search(randomIP[i])
                    datalist.append(temp)
                #timestamp end
                endtime = time.time()
                searchTime = endtime - starttime
                print('TrieTree : ', searchTime)
        return datalist

class Hash(object) :
    def __init__(self) :
        self.hashTable = dict()

    def createTable(self) :
        table = self.hashTable
        if os.path.isfile('data.pickle') :
            with open('data.pickle', 'rb') as f :
                filedata = pickle.load(f)
                ip_datalist = dict(filedata)
                networkID = list(ip_datalist.keys())

                for data in networkID :
                    value = ip_datalist.get(data)
                    b = convertBin()
                    network_bit = b.convert(data)
                    index = hash(network_bit)
                    table[index] = value

        datalist = []
        if os.path.isfile('random_ip_list.pickle') :
            with open('random_ip_list.pickle', 'rb') as f :
                randomIP = pickle.load(f)
                starttime = time.time()
                for i in range(len(randomIP)) :
                    b = convertBin()
                    network_bit = b.convert(randomIP[i])
                    for j in range(32, 7, -1) :
                        hashIndex = hash(network_bit[:j])
                        if hashIndex in table :
                            data = (randomIP[i], table[hashIndex])
                            datalist.append(data)
                            break
                        if j == 8 :
                            data = (randomIP[i], None)
                            datalist.append(data)
                            break

                endtime = time.time()
                searchTime = endtime - starttime
                print('Hash : ', searchTime)
            return datalist
    
def main() :
    tree = createTrieTree()
    tree.createTree()
    treedata = tree.searchIP()
    with open('trietree.pickle', 'wb') as f :
        pickle.dump(treedata, f)

    h = Hash()
    hashdata = h.createTable()
    with open('hash.pickle', 'wb') as f :
        pickle.dump(hashdata, f)

if __name__ == '__main__' :
    main()
