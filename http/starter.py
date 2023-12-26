from http.server import HTTPServer, BaseHTTPRequestHandler
import os
import sys
import HomeController

class MainHandler(BaseHTTPRequestHandler):
    def do_GET(self) -> None:
        
        # для початку відокремлюємо query string TODO відокремити hash(#)
        parts = self.path.split('?')
        path=parts[0]
        query_string = parts[1] if len(parts) > 1 else None
        print("self.path: ",self.path, query_string)
        # перевіряємо запит - чи це файл
        filename ='./http' + path
        # if(self.path =='/'):
        #     filename='./http/index.html'
        # else:
        #     filename = './http' + self.path
        # print("self.path: ",self.path, os.path.isfile(filename))
        if os.path.isfile(filename):
            self.flush_file(filename)
            return
        
        # розбираємо запит за принципом /controller/action
        parts = self.path.split('/') # запит починаємо з '/', 0-й ігноруємо
        # запит               parts
        # /                   ['','']
        # /controller         ['','controller']
        # /controller/        ['','controller','']
        # /ctrl/act           ['','ctrl','act']
        # /ctrl/act/          ['','ctrl','act','']
        controller = (parts[1].capitalize() if parts[1] != '' else 'Home')+"Controller"
        action = parts[2] if len(parts) > 2 and parts[2] != '' else 'index'

        try:
            controller_module   = getattr(sys.modules[__name__],controller)
            controller_class    = getattr(controller_module, controller)
            controller_instance = controller_class()
            controller_action   = getattr(controller_instance, action)
        except:
            controller_action=None
        if controller_action:
            controller_action(self)
        else:
            self.send_404()

        # print(parts)
        
      
    def flush_file(self, filename):
        ext = filename.split('.')[-1]
        if ext in('css','html'):
            content_type='text/'+ext
        elif ext == 'js':
            content_type='text/javascript'
        elif ext =='ico':
            content_type = 'image/x-icon'
        elif ext in ('png','bmp'):
            content_type='image/' + ext
        elif ext in ('jpg','jpeg'):
            content_type='image/jpeg'
        elif ext in ('py','ini','env','jss','php'):
            self.send_404()
            return
        else:
            content_type='application/octet-stream'

        self.send_response(200, 'OK')
        self.send_header('Content-Type', content_type)
        self.end_headers()
        with open(filename,"rb") as file:
            self.wfile.write(file.read())

    def send_404(self) -> None :
        self.send_response(404, 'Not Found')
        self.send_header('Status', 404)
        self.send_header('Content-Type', 'text/plain')
        self.end_headers()
        self.wfile.write("Resource for request not found".encode())
        
    def log_request(self, code: int | str = "-", size: int | str = "-") -> None:
        return None # відключити логування запитів у консоль
 

def main() -> None:
    http_server = HTTPServer(('127.0.0.1',81),MainHandler)
    try:
        print('Server starting')
        http_server.serve_forever()
    except:
        print('Server stopped')

if __name__ == "__main__":
    main()