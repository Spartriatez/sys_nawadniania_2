from wtforms import Form, TextField, TextAreaField, validators, StringField, SubmitField
from datetime import date, datetime, timedelta
import python.database_static as database_static
import mysql.connector

def addSecs(tm, secs):
    fulldate = datetime(100, 1, 1, tm.hour, tm.minute, tm.second)
    fulldate = fulldate + timedelta(seconds=secs)
    return fulldate.time()

def nawadnianie(listaFlowers,lista):
    try:
        cnx = database_static.connecting()
        cursor = cnx.cursor()
        add_user = ("INSERT INTO `Irrigation` "
                    "(id_f, Nazwa, Zlacze, Pin, godz_wyk) "
                    "VALUES (%s, %s, %s, %s,%s)")
        a = datetime.now().time()
        sec=0
        for i in range(len(listaFlowers)):
            for j in range(len(lista)):
                if(i==int(lista[j])):
                    b = addSecs(a, 600+sec)
                    data_employee = (str(listaFlowers[i][0]), listaFlowers[i][1],listaFlowers[i][2],str(listaFlowers[i][3]) ,b)
                    result=cursor.execute(add_user, data_employee)
                    sec+=60
                    
        cnx.commit()
        cursor.close()
        cnx.close()
        return 2
    except mysql.connector.Error as err:
        print("Something went wrong: {}".format(err))
        return 0
