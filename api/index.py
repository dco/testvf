from flask import Flask, render_template, request
from mongoengine import *
import datetime

connect(host="mongodb+srv://nodebb:9rGHFMefugTeASfF@cluster0.ntvar.mongodb.net/DCOCD?retryWrites=true&w=majority")

class Users(Document):
    email = StringField(max_length=200, required=True)
    tk = StringField()
    update_time = DateTimeField(default=datetime.datetime.utcnow()+datetime.timedelta(hours=8))

user = Users()

app = Flask(__name__)

@app.route('/')
def hello():
    return 'Hello, world'

@app.route('/reg', methods=['POST'])
def reg():
    user.email = request.form['email']
    user.update_time = datetime.datetime.utcnow()+datetime.timedelta(hours=8)
    user.tk = 'testmd5'
    user.save()
    return 'adcpost'

@app.route('/result')
def result():
   dict = {'phy':50,'che':60,'maths':70}
   return render_template('result.html', result = dict)
