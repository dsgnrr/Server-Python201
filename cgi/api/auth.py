#!D:/Programs/Python3/python.exe
import hashlib
import json
import mysql.connector
import os
import sys
sys.path.append('../') # додати папку пошуку модулів
import db_ini


query_params=None


def send_response(status_code:int=200,reason_phrase:str=None,body:object=None)->None:
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


def do_get():
    global query_params
    if not 'login' in query_params:
        send_response(400,"Bad request",{"message":"Missing required 'login' parameter"})
    if not 'password' in query_params:
        send_response(400,"Bad request",{"message":"Missing required 'password' parameter"})
                        
    db = get_db_or_exit()
    sql = 'SELECT * FROM users u WHERE u.`login`=%s AND u.`password`=%s'
    try:
        with db.cursor() as cursor:
            cursor.execute(sql, (query_params['login'], 
                                hashlib.md5(query_params['password'].encode()).hexdigest()))
            row= cursor.fetchone()
            if row == None:
                send_response(401,"Unauthorized",{"message":"Credentials rejected"})
            user_data=dict(zip(cursor.column_names,row))
            send_response(200,"Ok", {"auth":"success","token":user_data['id']})

    except mysql.connector.Error as err:
        send_response(503, 'Service Unavaliable',repr(err))
    send_response(200,"OK",{"auth":"works", "data":query_params})


def main():
    global query_params
    query_params = {k: v for k,v in
        (pair.split('=',1)
            for pair in os.environ["QUERY_STRING"].split('&'))} if len(os.environ["QUERY_STRING"]) > 0 else {}
    match os.environ['REQUEST_METHOD']:
        case 'GET':
            return do_get()
        case _:
            send_response(501,"Not implemented")
    pass


if __name__=="__main__":
    main()