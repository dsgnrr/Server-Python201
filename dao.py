import logging
import sys
import mysql.connector
sys.path.append('cgi/') # додатии папку пошуку модулів
import db_ini

def get_db():
    return mysql.connector.connect(**db_ini.connection_params)


class Cart:
   def add(self, user_id, product_id):
      sql = "INSERT INTO carts (user_id, product_id) VALUES(%d, %d)" %(int(user_id),int(product_id))
      try:
           db = get_db()
           with db.cursor() as cursor:
              cursor.execute(sql)
              db.commit()
      except mysql.connector.Error as err:
         logging.error('Dao cart',{'sql':sql,'err' : str(err)})
         raise RuntimeError() 
      except Exception as err:
         logging.error('Dao cart',{'exc' : str(err)})
         raise RuntimeError()


class Products:
    def get_all(self):
        sql = "SELECT * FROM products"
        res = []
        try:
           db = get_db()
           with db.cursor() as cursor:
              cursor.execute(sql)
              for row in cursor:
                 res.append(dict(zip(cursor.column_names,map(str,row))))
        except mysql.connector.Error as err:
           logging.error('Dao product',{'sql':sql,'err' : str(err)})
           raise RuntimeError() 
        except Exception as err:
           logging.error('Dao product',{'exc' : str(err)})
           raise RuntimeError()
        else:
           return res
        

class Auth:
    def get_user_id(self, token:str) -> str | None:
        # user_id це і є token, але перевіряємо його наявність у БД
        sql = "SELECT COUNT(id) FROM users WHERE id=%s"
        try:
           db=get_db()
           with db.cursor() as cursor:
                cursor.execute(sql, (token,))
                cnt = cursor.fetchone()[0]
        except mysql.connector.Error as err:
           logging.error('Dao product',{'sql':sql,'err' : str(err)})
           raise RuntimeError()
        except Exception as err:
            logging.error('Dao product',{'exc' : str(err)})
            raise RuntimeError()
        else:
          return token if cnt == 1 else None