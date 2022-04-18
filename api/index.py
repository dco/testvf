from flask import Flask, render_template, request
from mongoengine import *
import datetime
import hashlib

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

@app.route('/')
def hello():
    
    return 'Hello, world'


@app.route('/reg', methods=['POST'])
def reg():
    user = Users.objects.filter(email=request.form['email'])
    print(user)
    if user:
        user=user[0]
        user.update_time = datetime.datetime.utcnow()+datetime.timedelta(hours=8)
        user.tk = strMD5(user.email+user.update_time)
        user.save()
        return 'is exists'

    else:
        user = Users()
        user.email = request.form['email']
        user.update_time = datetime.datetime.utcnow()+datetime.timedelta(hours=8)
        user.tk = strMD5(request.form['email']+user.update_time)
        user.save()
        return 'is not exist!'
        
@app.route('/result')
def result():
   dict = {'phy':50,'che':60,'maths':70}
   return render_template('result.html', result = dict)

#app.run()
