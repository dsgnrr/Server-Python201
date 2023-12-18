#!D:/Programs/Python3/python.exe
import os
query_params= {k: v for k, v in 
               ( pair.split('=') 
                for pair in os.environ["QUERY_STRING"].split('&'))}
lang = query_params['lang']

var_names=['REQUEST_METHOD',
'QUERY_STRING',
'REQUEST_URI',
'REMOTE_ADDR']
vars= f"<ul>{"".join("<li>%s = %s</li>" %(k,v) for k, v in os.environ.items() if k in var_names)}</ul>"

resource = {
    'uk':'Корзина',
    'en':'Cart',
}
if not lang in resource:
    lang = 'uk'

print("Content-Type: text/html")
print("") # заголовки від тіла відокремлюються порожнім рядком
print(f"""<!doctype html>
<html>
    <head>
      <title>Py-201</title>
    </head>
    <body>
      <h1>{resource[lang]}</h1>
      {vars}
    </body>
</html>
      """)