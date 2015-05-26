import telnetlib
from ftplib import FTP

ftpIp = '192.168.254.1'
user = 'a'
passw = 'a'
path=".\\"
fault_file = 'MERA.txt'


class FtpFun(object):
    def __init__(self, ftpIp='192.168.254.1', user='a', passw='a', path=".\\" ):
        self.ftpIp = ftpIp
        self.user = user
        self.passw = passw
        self.path=path
        self.connectFTP()

    def connectFTP(self):
        self.ftp = FTP()
        self.ftp.connect(ftpIp)
        self.ftp.login(user, passw)


    def connectAndDownloadFile(self, fileNameRamGet, fileNameLocalGet):
        self.connectFTP()
        self.ftp.retrbinary('RETR '+fileNameRamGet, open(path+fileNameLocalGet, 'wb').write)
        #ftp.delete(fileNameRamGet)
        self.ftp.close()
        print "File downloaded"

    def deleteFileFromFtp(self, fileName):
        self.connectFTP(self):
        self.ftp.delete(fileName)
        self.ftp.close()

    def connectAndPutFile(self, fileNameRamPut, fileNameLocalPut):
        self.connectFTP(self):
        f = open(fileNameLocalPut, "r")
        self.ftp.storlines('STOR '+fileNameRamPut, f)
        f.close()
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


if __name__ == '__main__':
    
    scriptList = ["skrypt1.txt","skrypt2.txt"]
    resultList = [	"wynik1.txt", "wynik2.txt"]
    
    for scriptFile, resulFile  in zip(scriptList, resultList):
        ff = FtpFun()
        ff.connectAndPutFile(scriptFile, scriptFile)
        ff.temp = ". " + scriptFile
        print ff.temp
        ff.executeTelnetCommand(". " + scriptFile)
        ff.connectAndDownloadFile(resulFile, resulFile)
        ff.deleteFileFromFtp(scriptFile)
        ff.deleteFileFromFtp(resulFile)