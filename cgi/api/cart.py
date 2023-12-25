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
        self.send_response(meta={"service":"cart", "count":1,"status":200},
                          data={"user_id":user_id,"body_data":body_data})


CartController().serve()