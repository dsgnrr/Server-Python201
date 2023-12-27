import appconfig
import inspect
import os

class ShopController:
    def __init__(self, handler) -> None:
        self.handler = handler
        self.short_name = self.__class__.__name__.removesuffix('Controller').lower()
    
    def index(self):
        self.return_view(inspect.currentframe().f_code.co_name)

    def cart(self):
        self.return_view(inspect.currentframe().f_code.co_name)
        

    def return_view(self, action_name):
        layout_name = f"{appconfig.APP_PATH}/views/_layout.html"
        view_name = f"{appconfig.APP_PATH}/views/{self.short_name}/{action_name}.html"
        print("hello")
        if (not os.path.isfile(layout_name) or
                not os.path.isfile(view_name)):
            self.handler.send_404()
            return

        self.handler.send_response(200,"OK")
        self.handler.send_header('Content-Type','text/html; charset=utf-8')
        self.handler.end_headers()
        with open(layout_name) as layout:
            with open(view_name) as view:
                self.handler.wfile.write(
                    layout.read().replace('<!-- RenderBody -->', view.read()).encode('cp1251')
                )