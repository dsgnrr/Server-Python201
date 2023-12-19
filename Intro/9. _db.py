# Робота з БД на прикладі MySQL
# 1. Підключення
#   - конектор(драйвер БД): модуль/бібліотека, що узгоджує передачу
#   даних між середовищем виконання та СУБД. Конектор вибириаєтсья
#   під конкретну БД та конкретну мову.
#   pip install mysql-connector-python
# - тест підключення модуля

import mysql.connector
import hashlib
# - створюємо БД та користувача для неї
#   CREATE DATABASE py201;
#   GRANT ALL PRIVILIGES ON py201.* TO <username> IDENTIFIED by '<password>';
#   створюємо dict з параметрами БД
db_connection = None
db_ini = {
    "host":"localhost",
    "port":3306,
    "database":"py201",
    "user":"py2013",
    "password":"py201_pass",
    "charset":"utf8mb4",
    "use_unicode":True,
    "collation":"utf8mb4_unicode_ci" # utf8mb4_general_ci
}


def add_product(name:str, price:float, img_url:str|None = None):
    sql = f"INSERT INTO products (name, price, img_url) VALUES('{name}', '{price}', '{img_url}')"
    try:
       with db_connection.cursor() as cursor:
           cursor.execute(sql)
           db_connection.commit()
    except mysql.connector.Error as err:
        print(err)
        return
    else:
        print("INSERT products OK")


def create_products()-> None:
    sql ='''
CREATE TABLE IF NOT EXISTS products (
    id        BIGINT UNSIGNED PRIMARY KEY DEFAULT(UUID_SHORT()),
    `name`    VARCHAR(64)   NOT NULL,
    `price`   FLOAT         NOT NULL,
    `img_url` VARCHAR(256)  NULL
) Engine = InnoDB, DEFAULT CHARSET = utf8mb4 COLLATE utf8mb4_unicode_ci
'''
    try:
        with db_connection.cursor() as cursor:
            cursor.execute(sql)
    except mysql.connector.Error as err:
        print(err)
        return
    else:
        print("Create products OK")


def create_carts() -> None:
    sql = '''
CREATE TABLE IF NOT EXISTS carts(
    id BIGINT UNSIGNED PRIMARY KEY DEFAULT(UUID_SHORT()),
    `owner_id` BIGINT UNSIGNED NOT NULL,
    `product_id` BIGINT UNSIGNED NOT NULL,
    `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (`owner_id`) REFERENCES users (id),
    FOREIGN KEY (`product_id`) REFERENCES products (id)
) Engine = InnoDB, DEFAULT CHARSET = utf8mb4 COLLATE utf8mb4_unicode_ci
'''
    try:
        with db_connection.cursor() as cursor:
            cursor.execute(sql)
    except mysql.connector.Error as err:
        print(err)
        return
    else:
        print("Create carts OK")


def add_record_to_cart(owner_id:int, product_id:int):
    sql = f"INSERT INTO carts (owner_id, product_id) VALUES('{owner_id}', '{product_id}')"
    try:
       with db_connection.cursor() as cursor:
           cursor.execute(sql)
           db_connection.commit()
    except mysql.connector.Error as err:
        print(err)
        return
    else:
        print("INSERT carts OK")


def create_users()->None:
    sql ='''
CREATE TABLE IF NOT EXISTS users (
    id              BIGINT UNSIGNED PRIMARY KEY DEFAULT(UUID_SHORT()),
    `password`      VARCHAR(64)   NOT NULL,
    `login`         VARCHAR(32)   NOT NULL,
    `avatar`        VARCHAR(256)  NULL
) Engine = InnoDB, DEFAULT CHARSET = utf8mb4 COLLATE utf8mb4_unicode_ci
'''
    try:
        with db_connection.cursor() as cursor:
            cursor.execute(sql)
    except mysql.connector.Error as err:
        print(err)
        return
    else:
        print("Create users OK")


def add_user(login:str, password:str, avatar:str|None = None):
    password = hashlib.md5(password.encode()).hexdigest()
    sql = f"INSERT INTO users (`login`, `password`, `avatar`) VALUES('{login}', '{password}', '{avatar}')"
    try:
       with db_connection.cursor() as cursor:
           cursor.execute(sql)
           db_connection.commit()
    except mysql.connector.Error as err:
        print(err)
        return
    else:
        print("INSERT users OK")


def main()->None:
    global db_connection
    try:
        db_connection = mysql.connector.connect(**db_ini)
    except mysql.connector.Error as err:
        print(err)
        return
    else:
        print("Connection OK")

    # 2. Виконання запитів, одержання результатів
    sql = "SHOW DATABASES"
    cursor = db_connection.cursor() # ~ statement(Java), ~ sqlCommand(ADO)
    cursor.execute(sql)
    print(cursor.column_names)
    for row in cursor:
        print(row)
    # create_products()
    product = {
        "name":"Коробка 20х30х40",
        "price": 30,
        "img_url":"box1.png"
    }
    # add_product(**product)
    # create_users()
    user={
        "login":"user",
        "password":"1234",
        "avatar":"user.png"
    }
    # add_user(**user)
    # create_carts()
    cart = {
        "owner_id":100623253483028482,
        "product_id":100623253483028481
    }
    # add_record_to_cart(**cart)

if __name__ == "__main__":
    main()