from wtforms import Form, TextField, TextAreaField, validators, StringField, SubmitField
from datetime import date, datetime, timedelta
from werkzeug import generate_password_hash, check_password_hash
import python.database_static as database_static
import mysql.connector
    
def returnTable(id_u):
    try:
        cnx = database_static.connecting()
        cursor = cnx.cursor()
        
        query="SELECT Nazwa, Zlacze, Pin,data_utw,Godzina_podl,data_podlewania,okr_podl from `Flowers` WHERE id_u="+str(id_u)
        r=cursor.execute(query)
        result=cursor.fetchall() 
        count = cursor.rowcount
        cursor.close()
        cnx.close()
        return result
    except mysql.connector.Error as err:
        print("Something went wrong: {}".format(err))
        return 0

def returnTable2(id_u):
    try:
        cnx = database_static.connecting()
        cursor = cnx.cursor()
        
        query="SELECT id_f, Nazwa, Zlacze, Pin from `Flowers` WHERE id_u="+str(id_u)
        r=cursor.execute(query)
        result=cursor.fetchall() 
        count = cursor.rowcount
        cursor.close()
        cnx.close()
        return result
    except mysql.connector.Error as err:
        print("Something went wrong: {}".format(err))
        return 0
 