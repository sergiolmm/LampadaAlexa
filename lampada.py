import struct
import socket
import sys 
import _thread
import xml.etree.ElementTree as ET
import multicastaServer as multi
import envio as sd
import respostas as rp
import util as ut
import uuid

name = 'luz'
serial = '39cdc7bf-2bbe-477b-a2ae-97ddf7e3aa79'#str(uuid.uuid4())
message = 'projeto alexa python 1'
persistent_uuid = 'Socket-1_0-' + serial
estado_dispotivo = False 


def on_new_client(clientesocket, addr):
    while True:
        msg = clientesocket.recv(1024)
        if msg:
            print (str(addr) + ' >>' + msg.decode().replace('\r\n','\n') )
            break;
        else:
            break;

    msg1 = msg.decode()
    
    if msg1.__contains__('/index.html') | msg1.__contains__('/ ') :
        clientesocket.send(sd.sendHTTP(rp.sendIndex()).encode())
    else:
        if msg1.find('/upnp/control/basicevent1') > 0:
            global estado_dispotivo
            pos = msg1.find('s:encodingStyle')
            msg1 = msg1[:pos] + ' ' + msg1[pos:]
            inicio = msg1.find('<?xml')
            resp = msg1[inicio:1000]
            root = ET.fromstring(resp)
            root_tag = root.tag

            for child in root:
                for ch2 in child:
                    str4 = ch2.tag
                    if str4.find('SetBinaryState') > 0:
                        for ch3 in ch2:
                            valor = int(ch3.text)
                            if valor == 1:
                                estado_dispotivo = True
                            else:
                                estado_dispotivo = False  
            # decodifica a msg e liga ou deliga o led
            # retorna o status de ligado ou nao 
            if (estado_dispotivo):
                msg = sd.sendXML(rp.resposta_statusTrue())    
                print('Ligando o dispositivo\n')
            else:
                msg = sd.sendXML(rp.resposta_statusFalse())        
                print('Desligando o dispositivo\n')
            clientesocket.send(msg.encode())
        else:
            if msg1.find('/eventservice.xml') > 0:
                msg = sd.sendXML(rp.resposta_eventService())    
                clientesocket.send(msg.encode())
            else:             
                if msg1.find('/setup.xml') > 0:
                    msg = sd.sendXML(rp.resposta_setup_xml(name, persistent_uuid))    
                    clientesocket.send(msg.encode())
                else:
                    msg = ('HTTP/1.1 404 Not Found\r\n'
                    'Date: Sun, 18 Oct 2009 10:36:20 GMT\r\n'
                    'Server: Wemo\r\n'
                    'Content-Type: text/html; charset=iso-8859-1\r\n'
                    'Connection: close\r\n'  
                    '\r\n'
                    '\r\n'
                    '<!DOCTYPE HTML>\r\n'
                    '<html><head><title>404 Not Found</title></head><body>\r\n'
                    '<h1>Pagina nao encontrada neste site</h1><p>The requested URL /t.html was not found on this server.</p></body>\r\n'
                    '</html>\r\n')
                    clientesocket.send(msg.encode())


    clientesocket.close()

# http part - thread para servir como webserver local
##

https = ut.get_ip()
hport = 8080

sockH = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    sockH.bind((https,hport))
    print("bind Servidor http" + https)
except socket.error:
    sockH.bind(('', hport))
    print("bind Servidor http")

sockH.listen(1)
print('Listiong HTTP on '+https+' port : '+ str(hport)+ '\n')
multi = multi.MultiCastServer(persistent_uuid)
multi.start()
while True:
    c, addr = sockH.accept()
    print('aberto um socket')
    _thread.start_new_thread(on_new_client,(c,addr))
    
sockH.close()    

    

    #https://www.electricmonk.nl/log/2016/07/05/exploring-upnp-with-python/
 
#https://github.com/sagen/hue-upnp/blob/master/hueUpnp.py