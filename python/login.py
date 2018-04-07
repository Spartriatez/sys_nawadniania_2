from wtforms import Form, TextField, TextAreaField, validators, StringField, SubmitField
from datetime import date, datetime, timedelta
from werkzeug import generate_password_hash, check_password_hash
import python.database_static as database_static
import mysql.connector

class ReusableForm(Form):
    name = TextField('Name:', validators=[validators.required()])
    password = TextField('Password:', validators=[validators.required(), validators.Length(min=3, max=35)])

def login(name,password):
    try:
        hashed_passwd=None
        cnx = database_static.connecting()
        cursor = cnx.cursor()
        
        query="SELECT Nazwa_User, mail, haslo, data_utw FROM `Users` WHERE Nazwa_User = '"+str(name)+"'"
        
        result=cursor.execute(query)
        print(result)
        for (Nazwa_User, mail, haslo, data_utw) in cursor:
            hashed_passwd=haslo
            print("{}, {}, {} was hired on {:%d %b %Y}".format(Nazwa_User, mail, haslo, data_utw))
        count = cursor.rowcount
        cursor.close()
        cnx.close()
        if(count>=0):
            if(check_password_hash(hashed_passwd, password)):
                count=2
            else:
                count=1
        
        return count
    except mysql.connector.Error as err:
        print("Something went wrong: {}".format(err))
        return 0

def setId(name,password):
    try:
        cnx = database_static.connecting()
        cursor = cnx.cursor()
        query="SELECT id FROM `Users` WHERE Nazwa_User = '"+str(name)+"'"
        
        result=cursor.execute(query)
        print(result)
        count=0
        for id_u, in cursor:
            count=int(id_u)
        cursor.close()
        cnx.close()
        return count
    except mysql.connector.Error as err:
        print("Something went wrong: {}".format(err))
        return 0
