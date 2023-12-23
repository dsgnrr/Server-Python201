#!D:/Programs/Python3/python.exe
import api_controller
import base64
import hashlib
import mysql.connector

class AuthController(api_controller.ApiController):
    def do_get(self):  
        auth_token=self.get_auth_header_or_exit()
        try:
            login,password=base64.b64decode(auth_token, validate=True).decode().split(':',1)
        except:
            self.send_response(401,'Unauthorized',meta={"service":"auth","status":401,"scheme":"Basic"},
                               data={"message":"Malformed credentials: Basic scheme required"})

        db = self.get_db_or_exit()
        sql = 'SELECT * FROM users u WHERE u.`login`=%s AND u.`password`=%s'
        try:
            with db.cursor() as cursor:
                cursor.execute(sql, (login, 
                                hashlib.md5(password.encode()).hexdigest()))
                row= cursor.fetchone()
                if row == None:
                    self.send_response(401,"Unauthorized", meta={"service":"auth", "status":401, "scheme":"Basic"}, 
                                       data={"message":"Credentials rejected"})
                user_data=dict(zip(cursor.column_names,row))
                self.send_response(200,"OK",meta={"service":"auth", "status":200, "scheme":"Basic"},
                                   data={"scheme":"Bearer","token":str(user_data['id'])})

        except mysql.connector.Error as err:
            self.send_response(500,"Internal Error",
                           meta={"service":"product", "status":200, "count":0},
                           data={"message":"Server error, see logs for details"})

    def do_post(self):
    # send_response(body=dict(os.environ))
        self.send_response(200,"OK",meta={"service":"auth", "status":200, "scheme":"Bearer"},
                           data={"token":str(self.get_bearer_token_or_exit())})

AuthController().serve()