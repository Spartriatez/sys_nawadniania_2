import mysql.connector
from datetime import date, datetime, timedelta

def connecting():
    cnx = mysql.connector.connect(user='phpmyadmin', password='****',
                              host='127.0.0.1',
                              database='phpmyadmin')
    return cnx
