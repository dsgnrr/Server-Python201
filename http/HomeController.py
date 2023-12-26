from http.server import BaseHTTPRequestHandler

class HomeController:
    def index(self, handler:BaseHTTPRequestHandler):
        print("INDEX_HOME")
        handler.send_response(200, 'OK')
        handler.send_header('Content-Type', 'text/html')
        handler.end_headers()
        with open('./http/views_home/index.html',"rb") as file:
            handler.wfile.write(file.read())
    def privacy(self,handler:BaseHTTPRequestHandler):
        print("PRIVACY")
        handler.send_response(200, 'OK')
        handler.send_header('Content-Type', 'text/html')
        handler.end_headers()
        with open('./http/views_home/privacy.html',"rb") as file:
            handler.wfile.write(file.read())