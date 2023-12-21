import json
import mysql.connector
import os
import re
import sys
sys.path.append('../') # додати папку пошуку модулів
import db_ini

class ApiController:
    

    def send_response(self, status_code:int=200,reason_phrase:str='OK',body:object=None)->None:
        status_header = f"Status: {status_code}"
        if reason_phrase:
            status_header+=f" {reason_phrase}"
        print(status_header)
        print("Content-Type: text/html")
        print("")
        if body:
            print (json.dumps(body),end="")
        exit()
    

    def get_db_or_exit(self):
        try:
            return mysql.connector.connect(**db_ini.connection_params)
        except mysql.connector.Error as err:
            self.send_response(503,"Service Unavaliable",repr(err))


    def get_auth_header_or_exit(self,auth_scheme:str='Basic '):
        auth_header_name = 'HTTP_AUTHORIZATION'
        if not auth_scheme.endswith(' '):
            auth_scheme+=' '
        if not auth_header_name in os.environ:
            self.send_response(401,'Unauthorized',
                          {'message':"Missing 'Authorization' header"})
        auth_header_value = os.environ[auth_header_name]
    
        if not auth_header_value.startswith(auth_scheme):
            self.send_response(401,'Unauthorized',
                          {'message':f"Invalid Authorization scheme: {auth_scheme} only"})
        return auth_header_value[len(auth_scheme):] # Вилучаємо зі строки 'auth_scheme ' 
    

    def get_bearer_token_or_exit(self):
        auth_token = self.get_auth_header_or_exit('Bearer')
        if not re.match("^[0-9a-f-]+$", auth_token):
            self.send_response(401,'Unauthorized',
                          {'message':"Invalid Authorization token: hexdecimal form expected"})
        return auth_token


    def serve(self):
        method=os.environ['REQUEST_METHOD']
        action=f"do_{method.lower()}"
        attr = getattr(self,action,None)
        if attr:
            attr()
        else:
            self.send_response(501,"Not Implemented")
