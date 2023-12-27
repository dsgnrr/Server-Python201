import appconfig
import inspect
import os
from starter import MainHandler

class HomeController:
    def __init__(self, handler:MainHandler) -> None:
        self.short_name=self.__class__.__name__.removesuffix('Controller').lower()
        self.handler=handler
    
    def index(self):
        self.return_view(action_name=inspect.currentframe().f_code.co_name)

    def privacy(self):
        self.return_view(action_name=inspect.currentframe().f_code.co_name)

    def about(self ):
        self.return_view(action_name=inspect.currentframe().f_code.co_name)

    def return_view(self,action_name):
        layout_name =f"{appconfig.APP_PATH}/views/_layout.html"
        view_name = f"{appconfig.APP_PATH}/views/{self.short_name}/{action_name}.html"
        # print("HomeController::privacy",view_name)
        if (not os.path.isfile(layout_name) or
                not os.path.isfile(view_name)):
            self.handler.send_404()
            return
        
        self.handler.send_response(200, 'OK')
        self.handler.send_header('Content-Type', 'text/html; charset=utf-8')
        for header, value in self.handler.response_headers.items():
            self.handler.send_header(header,value)
        self.handler.end_headers()
        with open(view_name) as view:
            with open(layout_name) as layout:
                self.handler.wfile.write(
                    layout.read().replace('<!-- RenderBody -->', view.read()).encode('cp1251')
                )
