import os
import pymysql
import sys

CONFIG = {
    "mysql_host": "127.0.0.1",
    "mysql_port": 3306,
    "mysql_user": "root",
    "mysql_password": "93029302",
    "mysql_db": "gfp_db",
}
def db_connect():
    conn = pymysql.connect(
        host=CONFIG["mysql_host"],
        port=CONFIG["mysql_port"],
        user=CONFIG["mysql_user"],
        password=CONFIG["mysql_password"],
        db=CONFIG["mysql_db"],
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor
    )
    return conn
def db_select(sql):
    conn = db_connect()
    cursor = conn.cursor()
    cursor.execute(sql)
    result = cursor.fetchall()
    cursor.close()
    conn.close()
    return result
def db_insert(sql):
    conn = db_connect()
    cursor = conn.cursor()
    cursor.execute(sql)
    conn.commit()
    cursor.close()
    conn.close()
def db_update(sql):
    conn = db_connect()
    cursor = conn.cursor()
    cursor.execute(sql)
    conn.commit()
    cursor.close()
    conn.close()
def db_delete(sql):
    conn = db_connect()
    cursor = conn.cursor()
    cursor.execute(sql)
    conn.commit()
    cursor.close()
    conn.close()