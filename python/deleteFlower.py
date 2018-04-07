from wtforms import Form, TextField, TextAreaField, validators, StringField, SubmitField
from datetime import date, datetime, timedelta
from werkzeug import generate_password_hash, check_password_hash
import python.database_static as database_static
import mysql.connector

def delete_flower(listaFlowers,lista):
    try:
        cnx = database_static.connecting()
        cursor = cnx.cursor()
        
        query="DELETE FROM `Flowers` WHERE "
        print(query)
        for i in range(len(listaFlowers)):
            query2=[]
            for j in range(len(lista)):
                if(i==int(lista[j])):
                    print("usunieto ")
                    print(listaFlowers[i])
                    query2="Nazwa='" +listaFlowers[i][0]
                    query2+="' AND ZLACZE='" +listaFlowers[i][1]
                    query2+="' AND Pin='"+str(listaFlowers[i][2])
                    query2+="' AND data_utw='"+str(listaFlowers[i][3])
                    query2+="' AND Godzina_podl='"+str(listaFlowers[i][4])
                    query2+="' AND data_podlewania='"+str(listaFlowers[i][5])
                    query2+="' AND okr_podl='"+str(listaFlowers[i][6])+"'"
                    s=str(query)+str(query2)
                    cursor.execute(s)
                    print(s)
        cnx.commit()
        cursor.close()
        cnx.close()
        return 2
    except mysql.connector.Error as err:
        print("Something went wrong: {}".format(err))
        return 0
    
