#!D:/Programs/Python3/python.exe

import api_controller
import json
import logging
import sys
sys.path.append('../../')
import dao

class ProductController(api_controller.ApiController):
    
  def do_get(self):
    try:
       res = dao.Products().get_all()
    except:
        self.send_response(500,"Internal Error",
                           meta={"service":"product","count":0,"status":500},
                           data={"message":"Server error, see logs for details"})
    else:
       self.send_response(meta={"service":"product", "count":len(res),"status":200},
                          data=res)

  def do_post(self):
    auth_token = self.get_bearer_token_or_exit()
    # робота з тілом запиту. По схемі CGI (і не тільки) тіло запиту
    # передається у stdin
    request_body = sys.stdin.read().encode("cp1251").decode("utf-8")
    try:
        body_data= json.loads(request_body)
    except:
        self.send_response(400,'Bad Request',meta={"service":"product","count":0,"status":400},
                      data={'message':'Body must be valid JSON'})
    if not( 'name' in body_data and 'price' in body_data ):
        self.send_response(400,'Bad Request',meta={"service":"product","count":0,"status":400},
                      data={'message':"Body must include 'name' and 'price'"})
    db = self.get_db_or_exit()
    sql = "INSERT INTO products (name, price, img_url) VALUES(%(name)s, %(price)s, %(img_url)s)"
    try:
       with db.cursor() as cursor:
           cursor.execute(sql,body_data)
           db.commit()
    except :
       self.send_response(500,"Internal Error",
                           meta={"service":"product","count":0,"status":500},
                           data={"message":"Server error, see logs for details"})
    else:
       self.send_response(201,"OK",
                           meta={"service":"product","count":1,"status":201},
                           data={"message":"Created"})


ProductController().serve()