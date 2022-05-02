import util as ut


def reposta_m_search(uuid):
    resp = (
        'HTTP/1.1 200 OK\r\n'
        'CACHE-CONTROL: max-age=86400\r\n'
        'DATE: Tue, 14 Dec 2016 02:30:00 GMT\r\n'
        'EXT:\r\n'
        'LOCATION: http://' + ut.get_ip() + ':8080/setup.xml\r\n'
        'OPT: \"http://schemas.upnp.org/upnp/1/0/\"; ns=01\r\n'
        '01-NLS: '+uuid+'\r\n'
        'SERVER: Unspecified, UPnP/1.0, Unspecified\r\n'
        'X-User-Agent: redsonic\r\n'
        'ST: urn:Belkin:service:basicevent:1\r\n' #'ST: urn:Belkin:service:basicevent:1\r\n'
        'USN: uuid:' +uuid + '::urn:Belkin:service:basicevent:1\r\n'#urn:Belkin:device:**' #upnp:rootdevice\r\n'
#        'ST: urn:ssdp:all\r\n' #'ST: urn:Belkin:service:basicevent:1\r\n'
#        'USN: uuid:' +uuid + '::urn:ssdp:all'#urn:Belkin:device:**' #upnp:rootdevice\r\n'
        '\r\n\r\n')
    return resp    


def resposta_setup_xml(name, uuid):
    setup_xml = (
            '<?xml version=\"1.0\"?>'
            '<root>'
            '<device>'
            '<deviceType>urn:Belkin:device:controllee:1</deviceType>'
            '<friendlyName>'+name+'</friendlyName>'
            '<manufacturer>Belkin International Inc.</manufacturer>'
            '<modelName>Emulated Socket</modelName>'
            '<modelNumber>3.1415</modelNumber>'
            '<UDN>uuid:'+uuid+'</UDN>'
            '<serviceList>'
            '<service>'
                '<serviceType>urn:Belkin:service:basicevent:1</serviceType>'
                '<serviceId>urn:Belkin:serviceId:basicevent1</serviceId>'
                '<controlURL>/upnp/control/basicevent1</controlURL>'
                '<eventSubURL>/upnp/event/basicevent1</eventSubURL>'
                '<SCPDURL>/eventservice.xml</SCPDURL>'
            '</service>'
            '<service>'
                '<serviceType>urn:Belkin:service:metainfo:1</serviceType>'
                '<serviceId>urn:Belkin:serviceId:metainfo1</serviceId>'
                '<controlURL>/upnp/control/metainfo1</controlURL>'
                '<eventSubURL>/upnp/event/metainfo1</eventSubURL>'
                '<SCPDURL>/metainfoservice.xml</SCPDURL>'
            '</service>'
            '</serviceList>'
        '</device>'
        '</root>'
        )
    return setup_xml

def resposta_eventService():
    eventservice_xml = (
            '<scpd xmlns=\"urn:Belkin:service-1-0\">'
            '<specVersion><major>1</major><minor>0</minor></specVersion>'
            '<actionList>'
            '<action>'
            '<name>SetBinaryState</name>'
            '<argumentList>'
            '<argument>'
            '<retval />'
            '<name>BinaryState</name>'
            '<relatedStateVariable>BinaryState</relatedStateVariable>'
            '<direction>in</direction>'
            '</argument>'
            '</argumentList>'
            '</action>'
            '<action>'
            '<name>GetBinaryState</name>'
            '<argumentList>'
            '<argument>'
            '<retval/>'
            '<name>BinaryState</name>'
            '<relatedStateVariable>BinaryState</relatedStateVariable>'
            '<direction>out</direction>'
            '</argument>'
            '</argumentList>'
            '</action>'
            '</actionList>'
            '<serviceStateTable>'
            '<stateVariable sendEvents=\'yes\'>'
            '<name>BinaryState</name>'
            '<dataType>Boolean</dataType>'
            '<defaultValue>0</defaultValue>'
            '</stateVariable>'
            '<stateVariable sendEvents=\'yes\'>'
            '<name>level</name>'
            '<dataType>string</dataType>'
            '<defaultValue>0</defaultValue>'
            '</stateVariable>'
            '</serviceStateTable>'
            '</scpd>')
    return eventservice_xml


def resposta_statusTrue():
    statusResponseTrue = (
            '<?xml version=\"1.0\" encoding=\"utf-8\"?>'
            '<s:Envelope xmlns:s=\"http://schemas.xmlsoap.org/soap/envelope/\" s:encodingStyle=\"http://schemas.xmlsoap.org/soap/encoding/\">'
            '<s:Body>'
            '<u:GetBinaryStateResponse xmlns:u=\"urn:Belkin:service:basicevent:1\">'
            '<BinaryState>1</BinaryState>'
            '</u:GetBinaryStateResponse>'
            '</s:Body>'
            '</s:Envelope>')
    return statusResponseTrue        

def resposta_statusFalse():
    statusResponseFalse = (
            '<?xml version=\"1.0\" encoding=\"utf-8\"?>'
            '<s:Envelope xmlns:s=\"http://schemas.xmlsoap.org/soap/envelope/\" s:encodingStyle=\"http://schemas.xmlsoap.org/soap/encoding/\">'
            '<s:Body>'
            '<u:GetBinaryStateResponse xmlns:u=\"urn:Belkin:service:basicevent:1\">'
            '<BinaryState>0</BinaryState>'
            '</u:GetBinaryStateResponse>'
            '</s:Body>'
            '</s:Envelope>')
    return statusResponseFalse

def sendIndex():
    msg = ('<!DOCTYPE HTML>\r\n'
               '<html><head><title>Hello</title></head>\r\n'
               '<body><h1>Alo mundo virtual Wemo</h1>'
               '<p>Vamos iniciar no mundo Iot...</p></body></html>\r\n')
    return msg


if __name__ == '__main__':
    print('Testando resposta_m_search -> ')
    serial = '38323636-4558-4dda-9188-cda0e6010703'
    uuid = 'Socket-1_0-' + serial
    name = 'luz'
    print(reposta_m_search(uuid).replace('\r\n','\r'))
    #print(resposta_location(name, uuid), end='')
    import xml.etree.ElementTree as ET
    element = ET.XML(resposta_setup_xml(name, uuid))
    ET.indent(element)
    print(ET.tostring(element, encoding='unicode'))

    print('Testando resposta_eventService -> ')
    element = ET.XML(resposta_eventService())
    ET.indent(element)
    print(ET.tostring(element, encoding='unicode'))


    print('Testando resposta_statusTrue -> ')
    element = ET.XML(resposta_statusTrue())
    ET.indent(element)
    print(ET.tostring(element, encoding='unicode'))

    print('Testando resposta_statusFalse -> ')
    element = ET.XML(resposta_statusFalse())
    ET.indent(element)
    print(ET.tostring(element, encoding='unicode'))

