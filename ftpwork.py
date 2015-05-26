# -*- coding: utf-8 -*-
import telnetlib
from ftplib import FTP
#
# ftpIp = '192.168.254.1'
# user = 'a'
# passw = 'a'
# path=".\\"
# fault_file = 'MERA.txt'
"""
Zrobiłem z tego klase, jak bedziesz coś rozwijal to zawsze lepiej miec klasy niz nie miec
"""


class FtpFun(object): #zgodnie z nowymi zasdami klasy musza dziedziczyc object
    def __init__(self, ftpIp='192.168.254.1', user='a', passw='a', path=".\\" ):
        """
        konstruktor obiektu. Tu z automatu wrzycilem jakies tam parametry, normalnie gdy bedziesz wywolywal obiekt
        podajesz wlasciwe zmienna, jesli nie, polece te, ktore sa teraz wpisane
        podajac dane nie musisz pisac ftpIp=xxx.xxx.xxx.x user='xxx' itp, tylko po kolei 'xxx.xxx.xxx.x', 'tomek', 'szatan666'
        no i ta Twoja nieszczesna sciezna
        self.ftpIp=ftpIP -> dzięki temu pod zemienna self.ftpIp dla calej klasy jest dostepna ta zmienna
        """

        self.ftpIp = ftpIp
        self.user = user
        self.passw = passw
        self.path=path
        self.connectFTP()

    def connectFTP(self):#kazda funkcja w klasie musi dziedziczyc po klasie, wiec jako pierwszy arg. musi byc self
        """teraz wszedzie gdzie wywolas self.connectFTP() bedziesz polaczony z baza"""
        self.ftp = FTP()
        self.ftp.connect(ftpIp)
        self.ftp.login(user, passw)


    def connectAndDownloadFile(self, fileNameRamGet, fileNameLocalGet):
        self.connectFTP() #self.funkcja to odwolanie do wlasnej funkcji klasy (lub klasy po ktorej dziedziczy(ale o tym innym razem)
        self.ftp.retrbinary('RETR '+fileNameRamGet, open(self.path+fileNameLocalGet, 'wb').write)
        #ftp.delete(fileNameRamGet)
        self.ftp.close()
        print "File downloaded"

    def deleteFileFromFtp(self, fileName):
        self.connectFTP()
        self.ftp.delete(fileName)
        self.ftp.close()

    def connectAndPutFile(self, fileNameRamPut, fileNameLocalPut):
        self.connectFTP()
        with open(fileNameLocalPut, "r") as f: # tak nalezy pracowac z plikami (podobno)
            self.ftp.storlines('STOR '+fileNameRamPut, f)
        self.ftp.close()
        print "File put on ram"

    def executeTelnetCommand(self, command):
        tn = telnetlib.Telnet(self.ftpIp, 2323)
        if tn.read_until("$"):
            tn.write(command+"\n")
            screen = tn.read_until("$")
            tn.write("exit\n")
            tn.close()
        else:
            print "Problems with telnet connection"
            print tn.read_all()
        #return self.screen

    def disconnectFTP(self):
        '''
        zamkniecie polaczenia z uzyciem wyjatkow, jesli sie uda(da sie zamknac to zamknie, jesli nie
        zlapie wyjatek i go wydrukuje
        nie jestem przekonany czy po kazdej operacji warto zamykac polaczenie, a nastepnie znowy sie laczyc
        mysle, ze gdyby w konstruktorze uzyc self.self.connectFTP()
        to dla calego zycia obiektu polaczenie bedzie dzialac, a gdy juz obiekt nie jest potrzebny wywolac
        self.disconnectFTP()
        '''
        try: #probuje wykonac kod, jak sie nie uda przejdzie do bloku Exception,
            self.ftp.close() #probuje bo nie wiem czy jak jest zamkniete to nie wywali bledu, ze nie ma czego zamknac
        except Exception as err: # podanie po except Exception lapie wszystkie wyjatki, to nie jest dobra praktyka, ale nie wiem jaki tu powinien sie pojawic
            print err #lepiej wiedziec co lapiemy, potem wiemy do dalej z tym fantem zrobic





if __name__ == '__main__':
    """
    taki zapis pozwla odpalic moduł/klase jak zwykly skrypt,ale gdy uzyjesz modulu/klasy w innym kodzie to ten fragment
    zostanie 'pominiety'
    przydaje się to też do testowania
    """
    
    scriptList = ["skrypt1.txt","skrypt2.txt"]
    resultList = [	"wynik1.txt", "wynik2.txt"]

    ftpIp = '192.168.254.1'
    user = 'a' #unikalbym takich nazw zmiennych, moga byc uzywane w jakism modyle i je nadpiszesz
    passw = 'a'
    path=".\\"
    fault_file = 'MERA.txt'
    
    for scriptFile, resulFile  in zip(scriptList, resultList):
        ff = FtpFun(ftpIp, user, passw, path) #towrzy obiekt, tu mozesz podac dane np. ff=FtpFun('192.168.254.1', 'szatan', '666', 'd:\\tem\\')
        ff.connectAndPutFile(scriptFile, scriptFile)
        temp = ". " + scriptFile
        print ff.temp
        ff.executeTelnetCommand(temp)
        ff.connectAndDownloadFile(resulFile, resulFile)
        ff.deleteFileFromFtp(scriptFile)
        ff.deleteFileFromFtp(resulFile)
        ff.disconnectFTP()
    raw_input('koniec, dowolny klawisz by zamknac')