import appconfig
from http.server import HTTPServer, BaseHTTPRequestHandler
import importlib
import inspect
import os
import routes
import random
import time
import json
# import HomeController
# import ShopController


class MainHandler(BaseHTTPRequestHandler):
    sessions = {}
    def __init__(self, request,client_address, server) -> None:
        self.response_headers={}
        super().__init__(request,client_address, server)
        

    def do_GET(self) -> None:
        # для початку відокремлюємо query string TODO відокремити hash(#)
        parts = self.path.split('?')
        path=parts[0]
        query_string = parts[1] if len(parts) > 1 else None
        # перевіряємо запит - чи це файл
        if '../' in path or '..\\' in path:
            self.send_404()
            return
        filename = appconfig.WWWROOT_PATH + path
        if os.path.isfile(filename):
            self.flush_file(filename)
            return

        # Робота з сесією
        cookies_header=self.headers.get('Cookie','')
        cookies = dict(cookie.split('=') for cookie in cookies_header.split('; ') if '=' in cookie)
        if 'session-id' in cookies and cookies['session-id'] in MainHandler.sessions:
            # Вилучаємо дані зі статичного сховища і переносимо їх у self
            self.session = MainHandler.sessions[cookies['session-id']]
            pass # Є сесія для запиту

        else: # Немає сесії для запиту
            # стартуємо сесію - генеруємо id, якого немає у sessions
            while True:
                session_id = str(random.randint(1000, 9999))
                if not session_id in MainHandler.sessions:
                    break
            # встановлюємо загловок Cookie
            self.response_headers['Set-Cookie'] = f'session-id={session_id}'
            # утворюємо сховище для даних
            MainHandler.sessions[session_id]={
                'id': session_id,
                'timestamp':time.time()
            }
            self.session = MainHandler.sessions[session_id]
        print(self.session)
        # кінець з сесіями - тепер у self є self.session

        path_info = routes.parse_path(path)        
        try:
            controller_module = importlib.import_module(path_info["controller"])
            # controller_module   = getattr(sys.modules[__name__],controller)
            controller_class    = getattr(controller_module, path_info["controller"])
            controller_instance = controller_class(self)
            controller_action   = getattr(controller_instance, path_info["action"])
        except:
            controller_action=None
        if controller_action:
            controller_action()
        else:
            self.send_404()
        
        return

    def send_view(self, view_name:str=None, layout_name:str=None):
        controller_instance = inspect.currentframe().f_back.f_locals['self']
        if layout_name == None:
            layout_name=appconfig.DEFAULT_VIEW
        if view_name == None:
            controller_short_name = controller_instance.__class__.__name__.removesuffix('Controller').lower()
            action_name=inspect.currentframe().f_back.f_code.co_name
            view_name = f"{appconfig.VIEW_PATH}/{controller_short_name}/{action_name}.html"
        if (not os.path.isfile(layout_name) or
                not os.path.isfile(view_name)):
            self.send_404()
            return
        # Переносимо дані з сесії до статичного сховища
        for k,v in self.session.items():
            MainHandler.sessions[self.session['id']][k] = v
        self.send_response(200, 'OK')
        self.send_header('Content-Type', 'text/html; charset=utf-8')
        for header, value in self.response_headers.items():
            self.send_header(header,value)
        self.end_headers()
        with open(view_name) as view:
            view_content = view.read()
            view_data = getattr(controller_instance,'view_data', None)
            if view_data:
                for k, v in view_data.items():
                    view_content=view_content.replace(k, str(v))
            with open(layout_name) as layout:
                self.wfile.write(
                    layout.read().replace('<!-- RenderBody -->', view_content).encode('cp1251')
                )

      
    def flush_file(self, filename):
        if not os.path.isfile(filename):
            self.send_404()
            return
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
    if os.path.exists('sessions.json'):
        with open('sessions.json','r') as file:
            MainHandler.sessions = json.load(file)
    http_server = HTTPServer(('127.0.0.1',81),MainHandler)
    try:
        print('Server starting at http://localhost:81/')
        http_server.serve_forever()
    except:
        print('Server stopped')
        with open('sessions.json','w') as file:
            file.write(json.dump(MainHandler.sessions,file))

if __name__ == "__main__":
    main()