from wtforms import Form, TextField, TextAreaField, validators, StringField, SubmitField
from datetime import date, datetime, timedelta
import python.database_static as database_static
import mysql.connector

class ReusableForm(Form):
    flower = TextField('Flower:', validators=[validators.required()])
    device = TextField('Device:', validators=[validators.required()])
    pin = TextField('MySelect:', validators=[validators.required()])
    hh = TextField('HH:', validators=[validators.required()])
    mm = TextField('MM:', validators=[validators.required()])
    nexty = TextField('Nexty:', validators=[validators.required()])

def checkedDevice(device):
    if(device==1):
            return "RP Zero";
    elif(device==2):
            return "EXP0";
    elif(device==3):
            return "EXP1";
    elif(device==4):
            return "EXP2";
    else:
            return "nothing";
    
def flower_add(id_u,name,device,pin,hh,mm,nexty):
    try:
        if(int(device)>0):
            cnx = database_static.connecting()
            cursor = cnx.cursor()
            today = datetime.now().date()
            tomorrow=datetime.now().date()+timedelta(days=1)
            db=datetime.strptime(str(tomorrow)+" "+str(hh)+":"+str(mm),'%Y-%m-%d %H:%M')
            db2=datetime.strptime(str(hh)+":"+str(mm),'%H:%M').time()
            dev2=checkedDevice(int(device))
            add_user = ("INSERT INTO Flowers "
                    "(id_u, Nazwa, Zlacze, Pin, data_utw, Godzina_podl, data_podlewania, okr_podl) "
                    "VALUES (%s, %s, %s, %s, %s, %s, %s, %s)")

            data_employee = (str(id_u), name,dev2,str(pin) ,today, db2, db, str(nexty))

            result=cursor.execute(add_user, data_employee)
            print(result)
            cnx.commit()
            cursor.close()
            cnx.close()
            return 2
        else:
            return 0
            
    except mysql.connector.Error as err:
        print("Something went wrong: {}".format(err))
        return 0
    
def checkFlowerName(name):
    try:
        cnx = database_static.connecting()
        cursor = cnx.cursor()
        query="SELECT Nazwa FROM `Flowers` WHERE Nazwa = '"+str(name)+"'"
        
        result=cursor.execute(query)
        for (name) in cursor:
            print("{}".format(name))
        count = cursor.rowcount
        count+=1
        cursor.close()
        cnx.close()
        return count
    except mysql.connector.Error as err:
        print("Something went wrong: {}".format(err))
        return -1
    
def checkFlowerPin(pin,zlacze):
    try:
        print(zlacze)
        cnx = database_static.connecting()
        cursor = cnx.cursor()
        dev2=checkedDevice(int(zlacze))
        query="SELECT Nazwa, Zlacze, Pin FROM `Flowers` WHERE Zlacze = '"+dev2+"'"+ " AND Pin='"+str(pin)+"'"
        print(query)
        result=cursor.execute(query)
        for (Nazwa, Zlacze, Pin) in cursor:
            print("{}, {}, {}".format(Nazwa, Zlacze, Pin))
        count = cursor.rowcount
        count+=1
        cursor.close()
        cnx.close()
        return count
    except mysql.connector.Error as err:
        print("Something went wrong: {}".format(err))
        return 0

def checkFlowerHours(hh,mm):
    try:
        cnx = database_static.connecting()
        cursor = cnx.cursor()
        db=datetime.strptime(str(hh)+":"+str(mm),"%H:%M").time()
        query="SELECT Nazwa,Godzina_podl,data_podlewania FROM `Flowers` WHERE Godzina_podl = '"+str(db)+"'"
        result=cursor.execute(query)
        print(result)
        for (Nazwa, Zlacze, Pin) in cursor:
            print("{}, {}, {}".format(Nazwa, Zlacze, Pin))
        count = cursor.rowcount
        count+=1
        cursor.close()
        cnx.close()
        return count
    except mysql.connector.Error as err:
        print("Something went wrong: {}".format(err))
        return 0
