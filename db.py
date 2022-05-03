#db.py
import os
import pymysql
from flaskext.mysql import MySQL
from flask import jsonify

def auth_user(employee_id, password):
    conn = mysql.connect()
    with conn.cursor() as cursor: 
        result = cursor.execute('SELECT * FROM Employee WHERE employee_id = %s and password = %s', (employee_id, password))
        customers = cursor.fetchall()
        if result > 0:
            got_customers = "auth pass"
        else:
            got_customers = "Authentication Failed"
    conn.close()
    return got_customers
