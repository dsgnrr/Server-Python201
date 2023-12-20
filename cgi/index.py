#!D:/Programs/Python3/python.exe

import os

print("Content-Type: text/html")
print("") # заголовки від тіла відокремлюються порожнім рядком
print("""<!doctype html>
<html>
    <head>
      <title>Py-201</title>
    </head>
    <body>
      <h1>CGI працює</h1>
      <button onclick="authClick()">Auth</button>
      <button onclick="infoClick()">Info</button>
      <script>
        function authClick(){
            fetch("/auth?login=user&password=1234")
            .then(r=>r.text())
            .then(console.log);
        }
        function infoClick(){
            fetch("/auth",{
              method:'POST',
              headers:{
                'Authorization':'Bearer 100623253483028482'
              }
            })
            .then(r=>r.text())
            .then(console.log);
        }
      </script>
    </body>
</html>""")