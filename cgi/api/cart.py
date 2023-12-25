#!D:/Programs/Python3/python.exe

import api_controller
import json
import logging
import sys
sys.path.append('../../')
import dao

class CartController(api_controller.ApiController):
    def do_post(self):
        user_id = dao.Auth().get_user_id(self.get_bearer_token_or_exit())
        request_body = sys.stdin.read().encode("cp1251").decode("utf-8")
        try:
            body_data= json.loads(request_body)
        except:
            self.send_response(400,'Bad Request',meta={"service":"cart","count":0,"status":400},
                      data={'message':'Body must be valid JSON'})
        if not "productId" in body_data:
            self.send_response(400,'Bad Request',meta={"service":"cart","count":0,"status":400},
                      data={'message':"Body must included productId"})
        try:
            dao.Cart().add(user_id, body_data["productId"])
        except:
            self.send_response(500,"Internal Error",
                           meta={"service":"cart","count":0,"status":500},
                           data={"message":"Server error, see logs for details"})
        else: 
            self.send_response(201,'Created',meta={"service":"cart", "count":1,"status":201},
                          data={"message":"Created"})


CartController().serve()