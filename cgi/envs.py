#!D:/Programs/Python3/python.exe

import os
# os.environ -- dict із змінними оточення (ім'я-значення)
env_list=''
for key, value in os.environ.items():
    env_list+= f"{key} : {value}<br>"

envs =f"<ul>{"".join("<li>%s = %s</li>" %(k,v) for k, v in os.environ.items())}</ul>"
var_names=['REQUEST_METHOD',
'QUERY_STRING',
'REQUEST_URI',
'REMOTE_ADDR']
vars= f"<ul>{"".join("<li>%s = %s</li>" %(k,v) for k, v in os.environ.items() if k in var_names)}</ul>"

query_params= {k: v for k, v in 
               ( pair.split('=') 
                for pair in os.environ["QUERY_STRING"].split('&'))}
lang = query_params['lang']

resource = {
    'uk':'Вітання',
    'en':'Greeting',
    'de':'Hertzlich willkommen'
}
if not lang in resource:
    lang = 'uk' # default

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
      {query_params}
    </body>
</html>
      """)