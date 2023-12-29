import appconfig
import inspect
import os
from starter import MainHandler

class ShopController:
    def __init__(self, handler:MainHandler) -> None:
        self.handler = handler
        # self.short_name = self.__class__.__name__.removesuffix('Controller').lower()
    
    def index(self):
        self.handler.send_view()

    def cart(self):
        self.handler.send_view()
        

    # def return_view(self,action_name):
    #     view_name = f"{appconfig.APP_PATH}/views/{self.short_name}/{action_name}.html"
    #     self.handler.send_view(view_name)
