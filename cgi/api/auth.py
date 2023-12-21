#!D:/Programs/Python3/python.exe
import base64
import hashlib
import json
import mysql.connector
import os
import re
import sys
sys.path.append('../') # додати папку пошуку модулів
import db_ini


query_params = None


def send_response(status_code:int=200,reason_phrase:str='OK',body:object=None)->None:
    status_header = f"Status: {status_code}"
    if reason_phrase:
        status_header+=f" {reason_phrase}"
    print(status_header)
    print("Content-Type: text/html")
    print("")
    if body:
        print (json.dumps(body),end="")
    exit()


def get_db_or_exit():
    try:
        return mysql.connector.connect(**db_ini.connection_params)
    except mysql.connector.Error as err:
        send_response(503,"Service Unavaliable",repr(err))


def get_auth_header_or_exit(auth_scheme:str='Basic '):
    auth_header_name = 'HTTP_AUTHORIZATION'
    if not auth_scheme.endswith(' '):
        auth_scheme+=' '
    if not auth_header_name in os.environ:
        send_response(401,'Unauthorized',
                      {'message':"Missing 'Authorization' header"})
    auth_header_value = os.environ[auth_header_name]

    if not auth_header_value.startswith(auth_scheme):
        send_response(401,'Unauthorized',
                      {'message':f"Invalid Authorization scheme: {auth_scheme} only"})
    return auth_header_value[len(auth_scheme):] # Вилучаємо зі строки 'auth_scheme ' 


def do_get():
    # global query_params
    # if not 'login' in query_params:
        # send_response(400,"Bad request",{"message":"Missing required 'login' parameter"})
    # if not 'password' in query_params:
        # send_response(400,"Bad request",{"message":"Missing required 'password' parameter"})
    # login,password=query_params['login'],query_params['password']
    # Переходимо на авторизацію за схемою Basic    
    auth_token=get_auth_header_or_exit()

    try:
        login,password=base64.b64decode(auth_token, validate=True).decode().split(':',1)
    except:
        send_response(401,'Unauthorized',
                      {'message':f"Malformed credentials: Basic scheme required"})

    db = get_db_or_exit()
    sql = 'SELECT * FROM users u WHERE u.`login`=%s AND u.`password`=%s'
    try:
        with db.cursor() as cursor:
            cursor.execute(sql, (login, 
                                hashlib.md5(password.encode()).hexdigest()))
            row= cursor.fetchone()
            if row == None:
                send_response(401,"Unauthorized",{"message":"Credentials rejected"})
            user_data=dict(zip(cursor.column_names,row))
            send_response(200,"Ok", {"auth":"success","token":str(user_data['id'])})

    except mysql.connector.Error as err:
        send_response(503, 'Service Unavaliable',repr(err))
    send_response(200,"OK",{"auth":"works", "data":query_params})


def get_bearer_token_or_exit():
    auth_token = get_auth_header_or_exit('Bearer')
    if not re.match("^[0-9a-f-]+$", auth_token):
        send_response(401,'Unauthorized',
                      {'message':"Invalid Authorization token: hexdecimal form expected"})
    return auth_token


def do_post():
    # send_response(body=dict(os.environ))
    send_response(body=str(get_bearer_token_or_exit()))



def main():
    global query_params
    query_params = {k: v for k,v in
        (pair.split('=',1)
            for pair in os.environ["QUERY_STRING"].split('&'))} if len(os.environ["QUERY_STRING"]) > 0 else {}
    
    match os.environ['REQUEST_METHOD']:
        case 'GET':
            return do_get()
        case 'POST':
            return do_post()
        case _:
            send_response(501,"Not implemented")
    pass


if __name__=="__main__":
    main()