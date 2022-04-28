from flask import Flask, render_template, request
from mongoengine import *
import datetime
import hashlib
from flask_hcaptcha import hCaptcha
import json
import logging
from deta import Deta
import smtplib
from email.mime.text import MIMEText
from email.header import Header


deta = Deta("b0sstzzt_tC6kXutS7Fuwrz2tTdMYK8WUthcrawsp")
loginlog = deta.Base("login_log")

connect(host="mongodb+srv://nodebb:9rGHFMefugTeASfF@cluster0.ntvar.mongodb.net/DCOCD?retryWrites=true&w=majority")

class Users(Document):
    email = StringField(max_length=200, required=True)
    tk = StringField()
    update_time = DateTimeField(default=datetime.datetime.utcnow()+datetime.timedelta(hours=8))

def strMD5(source):
    md5 = hashlib.md5()
    source = source + 'dcocd.com'
    md5.update(source.encode('utf-8'))
    return md5.hexdigest()

def sendmail(receiver,token):
    receivers = []
    receivers.append(receiver)
    mail_msg = open("./mail.html",mode='r',encoding='utf-8').read().replace("mymailtoken",token)
    message = MIMEText(mail_msg, 'html', 'utf-8')
    #message['From'] = Header("菜鸟教程", 'utf-8')
    #message['To'] =  Header("To", 'utf-8')
    subject = '账户Token申请成功'
    message['Subject'] = Header(subject, 'utf-8')
    try:
        smtpObj = smtplib.SMTP_SSL(host="smtp.dcocd.com",port=465)
        smtpObj.login(user="support@dcocd.com",password="e8CATCQCy49L7afZgcSe")
        smtpObj.sendmail("support@dcocd.com", receivers, message.as_string())
        smtpObj.quit()
        return None
    except smtplib.SMTPException as e:
        return e

app = Flask(__name__)
app.config.update(
    HCAPTCHA_SITE_KEY = "bf3450d8-f636-4f7b-b99f-f78abe379cea",
    HCAPTCHA_SECRET_KEY = "0x8A842ebe7bDf2608CEf02DACb887Ab5D583A0D39"
)

hcaptcha = hCaptcha(app)


@app.route('/')
def home():
    return render_template('index.html')

@app.route('/handler', methods=['POST'])
def login():
    loginlog.put(json.loads(request.data.decode('UTF-8')))
    data = {
    "reject": False,
    "unchange": True
    }
    return json.dumps(data), 200

@app.route('/reg', methods=['POST'])
def reg():
    if hcaptcha.verify():
        now_time = datetime.datetime.utcnow()+datetime.timedelta(hours=8)
        user = Users.objects.filter(email=request.form['email'])

        if user:
            user=user[0]
            user.update_time = now_time
            user.tk = strMD5(user.email+str(now_time))
            user.save()
            sendmail(user.email,user.tk)
            return 'is exists'
        else:
            user = Users()
            user.email = request.form['email']
            user.update_time = now_time
            user.tk = strMD5(request.form['email']+str(now_time))
            user.save()
            sendmail(user.email,user.tk)
            return 'is not exist!'
    else:
        return 'verify bad'

# app.run()
