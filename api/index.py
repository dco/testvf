from flask import Flask, render_template
from mongoengine import *
import datetime

connect(host="mongodb+srv://nodebb:9rGHFMefugTeASfF@cluster0.ntvar.mongodb.net/DCOCD?retryWrites=true&w=majority")

class Users(Document):
    email = StringField(max_length=200, required=True)
    tk = StringField()
    date_modified = DateTimeField(default=datetime.datetime.now())


user1 = Users(
    email = 'test@test.com',
    tk = 'abcdefg'
    )

user1.save()
print(user1.email)

app = Flask(__name__)

@app.route('/')
def hello():
    return 'Hello, world'

@app.route('/test')
def test():
    return user1.email

@app.route('/result')
def result():
   dict = {'phy':50,'che':60,'maths':70}
   return render_template('result.html', result = dict)
