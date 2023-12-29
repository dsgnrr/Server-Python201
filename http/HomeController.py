import appconfig
import inspect
import os
from starter import MainHandler

class HomeController:
    def __init__(self, handler:MainHandler) -> None:
        # self.short_name=self.__class__.__name__.removesuffix('Controller').lower()
        self.handler=handler
    
    def index(self):
        self.handler.session['data'] = 'HomeController'
        self.view_data = {
            "@session-timestamp": self.handler.session['timestamp']
        }
        self.handler.send_view() # self.return_view()  #action_name=inspect.currentframe().f_code.co_name)

    def privacy(self):
        self.handler.send_view() # self.return_view()  #action_name=inspect.currentframe().f_code.co_name)

    def about(self ):
        self.handler.send_view()  #action_name=inspect.currentframe().f_code.co_name)

    # def return_view(self,action_name:str=None):
    #     if action_name == None:
    #         action_name=inspect.currentframe().f_back.f_code.co_name # f_back - попередній фрейм
    #     view_name = f"{appconfig.APP_PATH}/views/{self.short_name}/{action_name}.html"
    #     self.handler.send_view(view_name)
