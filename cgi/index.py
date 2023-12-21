#!D:/Programs/Python3/python.exe

import os

def read_all_text(fname) -> str | None: 
    try:
        with open(fname, mode="r",encoding="utf-8") as f:
            return f.read()
    except OSError as err:
        print("Read file error: ", err)

page =read_all_text('static/main.html')
if(page):
  print("Content-Type: text/html")
  print("") # заголовки від тіла відокремлюються порожнім рядком
  print(page)