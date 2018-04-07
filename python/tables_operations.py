from datetime import date, datetime, timedelta
import python.database_static as database_static
import mysql.connector
    
def returnTable():
    try:
        cnx = database_static.connecting()
        cursor = cnx.cursor()
        
        query="SELECT id_f, Nazwa, Zlacze, Pin,data_podlewania,okr_podl from `Flowers`"
        r=cursor.execute(query)
        result=cursor.fetchall() 
        count = cursor.rowcount
        cursor.close()
        cnx.close()
        return result
    except mysql.connector.Error as err:
        print("Something went wrong: {}".format(err))
        return 0
    
def updateTable(id_f,name):
    try:
        print(id_f,name)
        cnx = database_static.connecting()
        cursor = cnx.cursor()
        query="UPDATE `Flowers` SET data_podlewania=%s WHERE id_f=%s AND Nazwa=%s"
        today = datetime.now()
        b = today + timedelta(seconds=300)
        db=datetime.strptime(str(b.date())+" "+str(b.hour)+":"+str(b.minute),'%Y-%m-%d %H:%M')
        datetm=(db,id_f,name)
        r=cursor.execute(query,datetm)
        cnx.commit()
        cursor.close()
        cnx.close()
        return 2
    except mysql.connector.Error as err:
        print("Something went wrong: {}".format(err))
        return 0
    
def saveHistory(id_f,old_date,new_date):
    try:
        cnx = database_static.connecting()
        cursor = cnx.cursor()
        add_user = ("INSERT INTO `History` "
                    "(id_f, data_podlewania, data_nast_podl) "
                    "VALUES (%s, %s, %s)")

        data_employee = (id_f, old_date,new_date)

        result=cursor.execute(add_user, data_employee)
        print(result)
        cnx.commit()
        cursor.close()
        cnx.close()
        return 2
    except mysql.connector.Error as err:
        print("Something went wrong: {}".format(err))
        return 0
    