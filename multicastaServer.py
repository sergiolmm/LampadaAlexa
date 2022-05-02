import struct
import socket
import sys 
import _thread
import xml.etree.ElementTree as ET
import respostas as resp
import util as ut
from errno import ENOPROTOOPT



'''
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            #sock.bind(('0.0.0.0',mport))#group,mport))
            sock.bind((group,mport))
            print('bind mcast\n')
        except socket.error:
            sock.bind(('', mport))
        print('Listiong multicast on '+group+' port : '+ str(mport)+ '\n')

        mreq = struct.pack("4sl", socket.inet_aton(group), socket.INADDR_ANY)
        sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)
		sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, socket.inet_aton(BCAST_IP) + socket.inet_aton(IP));
		sock.settimeout(1)

'''  
'''
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        if hasattr(socket, "SO_REUSEPORT"):
            try:
                sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
            except socket.error as le:
                # RHEL6 defines SO_REUSEPORT but it doesn't work
                if le.errno == ENOPROTOOPT:
                    pass
                else:
                    raise

        addr = socket.inet_aton(group)
        interface = socket.inet_aton('0.0.0.0')
        cmd = socket.IP_ADD_MEMBERSHIP
        sock.setsockopt(socket.IPPROTO_IP, cmd, addr + interface)
        sock.bind(('0.0.0.0', mport))
        sock.settimeout(1)

'''

def multicast(group, mport,uuid):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        IP = ut.get_ip()
        try:
            sock.bind((IP,mport))
            print('bind mcast\n')
        except socket.error:
            sock.bind(('', mport))
        #print('Listiong multicast on '+group+' port : '+ str(mport)+ '\n')
        #mreq = struct.pack("4sl", socket.inet_aton(group), socket.INADDR_ANY)
        sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, socket.inet_aton(group) + socket.inet_aton(IP))
        sock.settimeout(1)
      
        while True:
            try:
                data, address = sock.recvfrom(12000)
            #except socket.timeout:
            except:
                continue
            
            #print (str(address) + ' >>\n' + data.decode() )
            if data:
                msg = data.decode()
                if msg.__contains__('M-SEARCH'):
                    print(msg.replace('\r\n','\n'))
                    sock.sendto(resp.reposta_m_search(uuid).encode(), address)
                    print ('Enviado :' , end='')
                    print(str(address))
                    print(resp.reposta_m_search(uuid).replace('\r\n','\n'))
                    print()
                    


class MultiCastServer:
    def __init__(self, uuid,group='239.255.255.250', port=1900):
        self.uuid = uuid
        self.group = group
        self.port = port


    def start(self):    
        print("Start Multicast Server at :" + self.group +":"+str(self.port))
        _thread.start_new_thread(multicast,(self.group, self.port, self.uuid))



if __name__ == '__main__':
    print('Testando Multicast class -> ')      
    serial = '38323636-4558-4dda-9188-cda0e6010703'
    uuid = 'Socket-1_0-' + serial  
    multi = MultiCastServer(uuid)
    multi.start()
    while True:
        a = 10

