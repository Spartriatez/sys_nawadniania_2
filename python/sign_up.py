from wtforms import Form, TextField, TextAreaField, validators, StringField, SubmitField
from datetime import date, datetime, timedelta
import python.database_static as database_static
import mysql.connector
class ReusableForm(Form):
    name = TextField('Name:', validators=[validators.required()])
    email = TextField('Email:', validators=[validators.required(), validators.Length(min=6, max=35)])
    password = TextField('Password:', validators=[validators.required(), validators.Length(min=3, max=35)])
    repeatpassword = TextField('Repeat Password:', validators=[validators.required(), validators.Length(min=3, max=35)])
    
def singing(name,email,password):
    try:
        cnx = database_static.connecting()
        cursor = cnx.cursor()
        tomorrow = datetime.now().date()

        add_user = ("INSERT INTO Users "
                "(Nazwa_User, mail, haslo, data_utw) "
                "VALUES (%s, %s, %s, %s)")

        data_employee = (name, email, password ,tomorrow)

        cursor.execute(add_user, data_employee)
        cnx.commit()
        cursor.close()
        cnx.close()
        return 2
    except mysql.connector.Error as err:
        print("Something went wrong: {}".format(err))
        return 0
        
def checkUser(name):
    try:
        cnx = database_static.connecting()
        cursor = cnx.cursor()
        
        query="SELECT Nazwa_User, mail, haslo, data_utw FROM `Users` WHERE Nazwa_User = '"+str(name)+"'"
        
        result=cursor.execute(query)
        print(result)
        for (Nazwa_User, mail, haslo, data_utw) in cursor:
            print("{}, {}, {} was hired on {:%d %b %Y}".format(Nazwa_User, mail, haslo, data_utw))
        count = cursor.rowcount
        cursor.close()
        cnx.close()
        return count
    except mysql.connector.Error as err:
        print("Something went wrong: {}".format(err))
        return 0
