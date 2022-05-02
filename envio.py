

def sendXML(msg):
   resp = ('HTTP/1.1 200 OK\r\n'
           'Content-Type: text/xml\r\n'
           'CONTENT-LENGTH: '+str(len(msg.encode("utf8")))+'\r\n'
           'Connection: close\r\n'  
           '\r\n' + msg)
   return resp 

def sendHTTP(msg):
   resp = ('HTTP/1.1 200 OK\r\n'
           'Content-Type: text/html\r\n'
           'CONTENT-LENGTH: '+str(len(msg.encode("utf8")))+'\r\n'
           'Connection: close\r\n'  
           '\r\n' + msg + '\r\n\r\n')
   return resp 

if __name__ == '__main__':
    print('Testando sendXML() -> ')
    import respostas as rep
    print(sendXML(rep.resposta_statusFalse()).replace('\r\n','\r'))
    msg = ( '<!DOCTYPE HTML>\r\n'
          '<html><head><title>Hello</title></head>\r\n'
          '<body><h1>Alo mundo virtual Wemo</h1>'
          '<p>Vamos iniciar no mundo Iot...</p></body>\r\n'
          '</html>\r\n')
    print('Testando sendHTTP() -> ')
    print(sendHTTP(msg).replace('\r\n','\r'))    