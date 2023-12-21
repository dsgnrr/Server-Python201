#!D:/Programs/Python3/python.exe

import api_controller
import json
import os
import sys

class ProductController(api_controller.ApiController):
    
  def do_get(self):
    self.send_response(body="Product Works")

  def do_put(self):
    auth_token = self.get_bearer_token_or_exit()
    # робота з тілом запиту. По схемі CGI (і не тільки) тіло запиту
    # передається у stdin
    request_body = sys.stdin.read().encode("cp1251").decode("utf-8")
    try:
        body_data= json.loads(request_body)
    except:
        self.send_response(400,'Bad Request',
                      {'message':'Body must be valid JSON'})
    if not( 'name' in body_data and 'price' in body_data ):
        self.send_response(400,'Bad Request',
                      {'message':"Body must include 'name' and 'price'"})
    self.send_response(body={"token":auth_token, "body":request_body})
    pass


ProductController().serve()