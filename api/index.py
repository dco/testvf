from flask import Flask, render_template, request
from mongoengine import *
import datetime
import hashlib
from flask_hcaptcha import hCaptcha

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

app = Flask(__name__)
app.config.update(
    HCAPTCHA_SITE_KEY = "bf3450d8-f636-4f7b-b99f-f78abe379cea",
    HCAPTCHA_SECRET_KEY = "0x8A842ebe7bDf2608CEf02DACb887Ab5D583A0D39"
)

hcaptcha = hCaptcha(app)

@app.route('/')
def home():
   return render_template('index.html')


@app.route('/reg', methods=['POST'])
def reg():
    now_time = datetime.datetime.utcnow()+datetime.timedelta(hours=8)
    user = Users.objects.filter(email=request.form['email'])
    print(user)
    if user:
        user=user[0]
        user.update_time = now_time
        user.tk = strMD5(user.email+str(now_time))
        user.save()
        return 'is exists'
    else:
        user = Users()
        user.email = request.form['email']
        user.update_time = now_time
        user.tk = strMD5(request.form['email']+str(now_time))
        user.save()
        return 'is not exist!'

#app.run()
