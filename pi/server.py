import http.server
import socketserver
import os
import json
import datetime

PORT = 8081
Handler = http.server.SimpleHTTPRequestHandler

with open("./o.json", "r+") as file:
	o = json.loads(file.read())

class RequestHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):  
        rootdir = os.path.dirname(os.path.realpath(__file__) ) + '/photos/' #file location  
        try:  
            if self.path.endswith('.jpg'):
                print(rootdir + self.path)
                f = open(rootdir + self.path, "rb") #open requested file  
                
        
                #send code 200 response  
                self.send_response(200)
        
                #send header first  
                self.send_header('Content-type','image/jpeg')  
                self.end_headers()  
        
                #send file content to client  
                self.wfile.write(f.read())
                f.close()
                return
            else:
                f = open("./data.json", "r+")
                data = json.loads(f.read())

                self.send_response(200)

                self.send_header('Content-type','text/html')  
                self.end_headers() 

                self.wfile.write(bytes("<p>Current view of camera: </p><img width='200' src='http://" + o["cameraip"] + "/index.jpg' />", encoding="utf-8"))

                for event in data['events'][-5:]:
                    self.wfile.write(bytes("<p>Inicident Reported on " + str(datetime.datetime.fromtimestamp(int(event["timestamp"]))) + "</p><img width='300' src='/" + event["imageFile"].split("/")[-1] + "' /><br>", encoding="utf-8"))
                
                f.close()
                return
        except IOError:
            self.send_error(404, 'file not found')

with socketserver.TCPServer(("", PORT), RequestHandler) as httpd:
    print("serving at port", PORT)
    httpd.serve_forever()