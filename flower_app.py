from flask import Flask, render_template, flash, request, redirect, url_for, session
from wtforms import Form, TextField, TextAreaField, validators, StringField, SubmitField
from werkzeug import generate_password_hash, check_password_hash
import random, threading, webbrowser
import time
from threading import Thread, Event
from datetime import date, datetime, timedelta
import wiringpi as wiringpi
import RPi.GPIO as GPIO
import sys
sys.path.insert(0, '/home/arhelius/flask')

import python.sign_up as sign_up, python.login as login, python.addflower as addflower, python.table_flower as tf, python.deleteFlower as df,python.irrigation as ir, python.history as his
import python.I2C_LCD_driver as I2C_LCD_driver, python.tables_operations as to

GPIO.setmode(GPIO.BCM)
GPIO.setup(17,GPIO.OUT)
GPIO.output(17,1)
mylcd = I2C_LCD_driver.lcd()
change_class=1
pin_base=65
i2c_addr=0x20
wiringpi.wiringPiSetup()
wiringpi.pcf8574Setup(pin_base,i2c_addr)

def loop_process():
    global change_class
    example=0
    flow=None
    while True:
        now=datetime.now()
        if (change_class==1 or example==1):
            flow=to.returnTable()
            change_class=0
            example=0
        print(flow)
        for i in range(len(flow)):
            if(flow[i][4].year<=now.year and flow[i][4].month<=now.month and flow[i][4].day<=now.day and flow[i][4].hour<=now.hour and flow[i][4].minute<=now.minute):
                temp=flow[i][4]
                tonight=datetime.now()+timedelta(seconds=300)
                if(to.updateTable(flow[i][0],flow[i][1])>0):
                   if(to.saveHistory(flow[i][0],temp,tonight)>0):
                       mylcd.lcd_clear()
                       GPIO.output(17,0)
                       
                       mylcd.lcd_display_string("Trwa podlewanie", 1)
                       mylcd.lcd_display_string("Kwiatek: %s" %flow[i][1], 2)
                       wiringpi.digitalWrite(65+int(flow[i][3]),0) 
                       time.sleep(10)
                       mylcd.lcd_clear()
                       wiringpi.digitalWrite(65+int(flow[i][3]),1)
                       GPIO.output(17,1)
                       example=1
                    
        print(now)
        mylcd.lcd_display_string("Time: %s" %time.strftime("%H:%M:%S"), 1)
        mylcd.lcd_display_string("Date: %s" %time.strftime("%m/%d/%Y"), 2)
        time.sleep(1)


thread = threading.Thread(target=loop_process)

app = Flask(__name__)
port = 5000
url = "http://127.0.0.1:{0}".format(port)


def startTime():
    seconds=datetime.now().strftime("%S")
    print(seconds)
    
@app.route("/",methods=['GET', 'POST'])
def main():
    if(session.get('logged_in')==True):
        session.clear()
    form = login.ReusableForm(request.form)
    print(form.errors)
    if request.method == 'POST':
        name=request.form['name']
        password=request.form['password']
        if form.validate():
            if(login.login(name,password)>1):
                session['logged_in'] = True
                session['id_u']=login.setId(name,password)
                print(session['id_u'])
                return redirect(url_for('menu'))
            elif(login.login(name,password)==1):
                flash('Error: Podano złe hasło ')
            else:
                flash('Error: Nie ma takiego użytkownika ')
        else:
            flash('Error: Wszystkie pola muszą być wypełnione ')
    return render_template('index.html',form=form)

@app.route("/menu")
def menu():
    if(session.get('logged_in')==True):
        startTime()
        table=tf.returnTable(session['id_u'])
        print(table)
        return render_template('menu.html',table=table)
    else:
        return redirect(url_for('main'))
    
@app.route("/edycja")
def edycja():
    if(session.get('logged_in')==True):
        table=tf.returnTable(session['id_u'])
        return render_template('edition.html',table=table)
    else:
        return redirect(url_for('main'))
    
@app.route("/edycja/usun",methods=['GET', 'POST'])   
def usun_kwiatka():
    global change_class
    if(session.get('logged_in')==True):
        table=tf.returnTable(session['id_u'])
        lista=request.form.getlist('selectThis[]')
        if(df.delete_flower(table,lista)==2 and lista!=[]):
            flash('Success: Usunieto kwiaty z bazy danych')
            change_class=1
            return redirect(url_for('edycja'))
        elif(lista==[]):
            return render_template('deleteFlower.html',table=table)
        else:
            flash('Error: Błąd bazy danych ')
        
    else:
        return redirect(url_for('main'))
    
    
@app.route("/edycja/dodaj",methods=['GET', 'POST'])
def dodaj_kwiatka():
    global change_class
    form = addflower.ReusableForm(request.form)
 
    print(form.errors)
    if request.method == 'POST':
        flower=request.form['flower']
        device=request.form['device']
        pin=request.form['pin']
        hh=request.form['hh']
        mm=request.form['mm']
        nexty=request.form['nexty']
        if form.validate():
            if(addflower.checkFlowerName(flower)==0):
                if(addflower.checkFlowerPin(pin,device)==0):
                    if(addflower.checkFlowerHours(hh,mm)==0):
                        if(addflower.flower_add(session['id_u'],flower,device,pin,hh,mm,nexty)>0):
                            print(flower, device, pin, hh,mm,nexty)
                            change_class=1
                            return redirect(url_for('edycja'))
                        else:
                            flash('Error: Błąd bazy danych ')
                    elif(addflower.checkFlowerHours(hh,mm)<0):
                        flash('Error: Błąd bazy danych ')
                    else:
                        flash('Error: Podana godzina już zajęta przez inny kwiatek')
                elif(addflower.checkFlowerPin(device,pin)<0):
                    flash('Error: Błąd bazy danych ')
                else:
                    flash('Error: Pin zajęty przez inny kwiatek')
            elif(addflower.checkFlowerName(flower)<0):
                flash('Error: Błąd bazy danych ')
            else:
                flash('Error: Kwiatek o takiej nazwie już istnieje ')
        else:
            flash('Error: Wszystkie pola muszą być wypełnione ')
    return render_template('addflower.html', form=form)
    
    
@app.route("/nawadnianie",methods=['GET', 'POST'])
def nawadnianie():
    if(session.get('logged_in')==True):
        table=tf.returnTable2(session['id_u'])
        lista=request.form.getlist('selectThis[]')
        if(ir.nawadnianie(table,lista)==2 and lista!=[]):
            flash('Success: Dodano listę dodatkowego nawadniania')
        elif(ir.nawadnianie(table,lista)==0 and lista!=[]):
            flash('Error: Błąd bazy danych ')
        return render_template('addwather.html',table=table)
    else:
        return redirect(url_for('main'))
    
@app.route("/historia",methods=['GET', 'POST'])
def historia():
    if(session.get('logged_in')==True):
        months=his.returnMonth()
        years=his.returnYear()
        
        flower=request.form.get('flower')
        mm=request.form.get('MM')
        yy=request.form.get('YYYY')
        if((flower==None and mm==None and yy==None) or (flower=='' and mm=='0' and yy=='0')) :
            print(flower,yy,mm)
            currentMonth = datetime.now().month
            currentYear = datetime.now().year
            table=his.returnTable(currentMonth,currentYear)
            return render_template('history.html',months=months,years=years,Year=currentYear,Month=currentMonth,table=table)
        elif(flower=='' and mm!='0' and yy!='0'):
            table=his.returnTable(mm,yy)
            return render_template('history.html',months=months,years=years,Year=yy,Month=mm,table=table)
        elif(flower!='' and mm!='0' and yy!='0'):
            table=his.returnTable2(flower,mm,yy)
            return render_template('history.html',months=months,years=years,Year=yy,Month=mm,table=table)
        elif(flower!='' and mm=='0' and yy=='0'):
            currentMonth = datetime.now().month
            currentYear = datetime.now().year
            table=his.returnTable2(flower,currentMonth,currentYear)
            return render_template('history.html',months=months,years=years,Year=currentYear,Month=currentMonth,table=table)
        else:
            flash('Error: Błądy wykonywania ')
    else:
        return redirect(url_for('main')) 
   
@app.route("/SignUp",methods=['GET', 'POST'])
def rejestracja():
    form = sign_up.ReusableForm(request.form)
 
    print(form.errors)
    if request.method == 'POST':
        name=request.form['name']
        password=request.form['password']
        hash_passwd=generate_password_hash(password)
        email=request.form['email']
        repeatpassword=request.form['repeatpassword']
        
        if form.validate():
            if(check_password_hash(hash_passwd, repeatpassword)):
                if(sign_up.checkUser(name)<0):
                    if(sign_up.singing(name,email,hash_passwd)<=0):
                        flash('Error: Błąd bazy danych')
                    else:
                        return redirect(url_for('main'))
                elif(sign_up.checkUser(name)==0):
                     flash('Error: Błąd bazy danych')
                else:
                     flash('Error: Podany użytkownik już istnieje')
            else:
                flash('Error: Podane hasła się różnią')
        else:
            flash('Error: Wszystkie pola muszą być wypełnione ')
    return render_template('SignUp.html', form=form)

@app.route('/logout')
def logout():
    session.pop('logged_in',None)
    flash('zostałeś wylogowany')
    return redirect(url_for('menu'))  


if __name__ == "__main__":
    thread.start()
    app.secret_key = 'ssssshhhhh'
    app.run(port=port, debug=False)
