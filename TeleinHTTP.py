#!/usr/bin/env python
from BaseHTTPServer import HTTPServer
from SimpleHTTPServer import SimpleHTTPRequestHandler
import teleinfo 

# TODO : Add debug mode
# TODO : Add IP ACL Feature

class HTTPHandler(SimpleHTTPRequestHandler):
    server_version = "TeleinHTTP/0.1"
    #FIXME: Autodetect ?
    ti = teleinfo.Teleinfo("/dev/ttyUSB0")
    
    def do_GET(self):
        # GET what's after the first /
        etiquette = self.path.split("/")[1] 
        self.reponse(etiquette)
     
    def reponse(self,etiquette):
        #Filter by know keys
        #TODO: Add all existing 
        if etiquette in ["IINST","PAPP","MOTDETAT","OPTARIF","ADCO","HCHC","HCHP","IMAX","ISOUSC","HHPHC"]:
            value = -1
            for retry in [0,1]:
                # dont retry if value exists
                if value != -1:
                    break
                if retry == 1:
                    print "Retrying !"
                for serEtiquette, serValue in self.ti.read().items():
                    if (serEtiquette == etiquette):
                            value = serValue
                            break
            
            self.send_response(200)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write(value)

        # Throw 404 to not know etiquettes    
        else:
            self.send_response(404)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write("<h1>Error 404</h1>")
            self.wfile.write("The URL you requested could not be found.")
            
     
httpd = HTTPServer(('', 8353), HTTPHandler)
httpd.serve_forever()
