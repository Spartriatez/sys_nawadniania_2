from wtforms import Form, TextField, TextAreaField, validators, StringField, SubmitField
from datetime import date, datetime, timedelta
from werkzeug import generate_password_hash, check_password_hash
import python.database_static as database_static
import mysql.connector
   
def returnMonth():
    try:
        cnx = database_static.connecting()
        cursor = cnx.cursor()
    
        query="SELECT DISTINCT MONTH(data_podlewania) FROM `History`"
        r=cursor.execute(query)
        months=[]
        for month, in cursor:
            months.append(month)
        cursor.close()
        cnx.close()
        return months
    except mysql.connector.Error as err:
        print("Something went wrong: {}".format(err))
        return 0
    
def returnYear():
    try:
        cnx = database_static.connecting()
        cursor = cnx.cursor()
        
        query="SELECT DISTINCT Year(data_podlewania) FROM `History`"
        r=cursor.execute(query)
        years=[]
        for year, in cursor:
            years.append(year)
        cursor.close()
        cnx.close()
        return years
    except mysql.connector.Error as err:
        print("Something went wrong: {}".format(err))
        return 0

def returnTable(curMonth,curYear):
    try:
        cnx = database_static.connecting()
        cursor = cnx.cursor()
        
        query="SELECT f.nazwa,h.data_podlewania,h.data_nast_podl from `History` h JOIN `Flowers` f ON h.id_f=f.id_f WHERE MONTH(h.data_podlewania)="+str(curMonth)+" AND YEAR(h.data_podlewania)="+str(curYear)  
        r=cursor.execute(query)
        result=cursor.fetchall() 
        count = cursor.rowcount
        cursor.close()
        cnx.close()
        return result
    except mysql.connector.Error as err:
        print("Something went wrong: {}".format(err))
        return 0

def returnTable2(flower,curMonth,curYear):
    try:
        cnx = database_static.connecting()
        cursor = cnx.cursor()
        
        query="SELECT f.nazwa,h.data_podlewania,h.data_nast_podl from `History` h JOIN `Flowers` f ON h.id_f=f.id_f WHERE MONTH(h.data_podlewania)="+str(curMonth)+" AND YEAR(h.data_podlewania)="+str(curYear)+" AND f.nazwa='"+str(flower)+"'"
        r=cursor.execute(query)
        result=cursor.fetchall() 
        count = cursor.rowcount
        cursor.close()
        cnx.close()
        return result
    except mysql.connector.Error as err:
        print("Something went wrong: {}".format(err))
        return 0
