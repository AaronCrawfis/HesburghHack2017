###########################################################
# Name:         Aaron Crawfis, Jack Casey
# Date:         31 March 2017
# Name:         __init__.py
# Description:  Main Flask Handler for Food App
#               Hesburgh Hacks 2017
###########################################################


# Libraries -----------------------------------------------
from flask import Flask, render_template, url_for, request, redirect
import flask_login

from twilio import TwilioRestException
from twilio.rest import TwilioRestClient

import datetime
import os
import sys

import nutrition

# Variables -----------------------------------------------

# App
app = Flask(__name__)

# Login Manager
login_manager = flask_login.LoginManager()
login_manager.init_app(app)

# Database
users = {'acrawfis@nd.edu': {'pw': 'Password1234'}}

# Twilio
account_sid = "ACfd1692446b867fa4e3166f7d6cb455a9" 
auth_token  = "51c06d2d51ac43b722d0ac2e9b57a38c"
twilioClient = TwilioRestClient(account_sid, auth_token)

# User Manager --------------------------------------------

class User(flask_login.UserMixin):
    pass

@login_manager.user_loader
def user_loader(email):
    if email not in users:
        return

    user = User()
    user.id = email.split('@')[0]
    return user

@login_manager.request_loader
def request_loader(request):
    email = request.form.get('UserName')
    if email not in users:
        return
    
    user = User()
    user.id = email.split('@')[0]

    # DO NOT ever store passwords in plaintext and always compare password
    # hashes using constant-time comparison!
    user.is_authenticated = request.form['Password'] == users[email]['pw']

    return user

# Functions -----------------------------------------------

def sendTextForFood(food, venue):
    try:
        message = twilioClient.messages.create(body="{} is being served today at {}!".format(food,venue),
        to="+19897870227",
        from_="+19897873042")
    except TwilioRestException as e:
        print(e)

def nameOfDayInXDays(x):
    dt = datetime.date.today() + datetime.timedelta(days=x)
    return dt.strftime("%A")

def writeFileFromForm(form):
    # Variables --------------
    filePath = '/var/www/food/food/uploads/'

    # All
    dayNum = int(form['dayNum'])

    # Prep
    filename = filePath + str(dayNum) + ".txt"
    if os.path.isfile(filename):
        os.remove(filename)

    # Breakfast ----------------------------
    if form['breakfast'] == 'yes':
        eat = True
    else:
        eat = False
    venue = form['bVenue']
    course = 'Breakfast'
    # Run Functions
    sys.stdout.flush()
    mealoptions = nutrition.getOptions(eat, venue, course, dayNum)
    if mealoptions:
        mealchoice = nutrition.getMeal(mealoptions, course, venue)
        nutrition.writetxtfile(mealchoice, course, dayNum)
    # Lunch ---------------------------------
    if form['lunch'] == 'yes':
        eat = True
    else:
        eat = False
    venue = form['lVenue']
    course = 'Lunch'
    # Run Functions
    mealoptions = nutrition.getOptions(eat, venue, course, dayNum)
    print mealoptions
    if mealoptions:
        mealchoice = nutrition.getMeal(mealoptions, course, venue)
        nutrition.writetxtfile(mealchoice, course, dayNum)
    # Dinner ---------------------------------
    if form['dinner'] == 'yes':
        eat = True
    else:
        eat = False
    venue = form['dVenue']
    course = 'Dinner'
    # Run Functions
    mealoptions = nutrition.getOptions(eat, venue, course, dayNum)
    if mealoptions:
        mealchoice = nutrition.getMeal(mealoptions, course, venue)
        nutrition.writetxtfile(mealchoice, course, dayNum)

def getMacros():
    macros = dict()
    for i in range(7):
        filename = '/var/www/food/food/uploads/' + str(i) + '.txt'
        dayMacros = dict()
        if os.path.isfile(filename):
            with open(filename) as file:
                lines = file.readlines()
            for line in lines:
                if ':' in line:
                    info = line.split(':')
                    dayMacros[info[0]] = info[1].lstrip().rstrip()
            macros[i] = dayMacros 
    return macros

# Path Handlers -------------------------------------------

# Index ------------------------
@app.route('/')
def index():
    return redirect(url_for('login'))

# Dashboard --------------------
@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

# Login ------------------------
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html', failedLogin=False)
    else:
        netID = request.form['login_id']
        password = request.form['pw']
        #p0 = searchForNetID(netID)
        if True:
            user = User()
            user.id = netID
            flask_login.login_user(user)
            return redirect(url_for('dashboard'))
        else:
            return render_template('login.html', failedLogin=True)

# Protected ----------------------
@app.route('/protected')
@flask_login.login_required
def protected():
    #return 'Logged in as: ' + flask_login.current_user.id
    return 'Protected'

# Logout --------------------------
@app.route('/logout')
def logout():
    flask_login.logout_user()
    return redirect(url_for('login'))

# New User ------------------------
@app.route('/newUser', methods=['GET', 'POST'])
def newUser():
    if request.method == 'GET':
        return render_template('newUser.html', failedCreate=False)
    else:
        return redirect(url_for('login'))

# Unauthorized ---------------------
@login_manager.unauthorized_handler
def unauthorized_handler():
    return 'Unauthorized'

# Food Alerts ----------------------
@app.route('/foodAlerts', methods=['GET', 'POST'])
def foodAlerts():
    if request.method == 'GET':
        return render_template('foodAlerts.html', showSearch=True, showFood=False, foodDone=False)
    else:
        if request.form['submit'] == 'Search':
            return render_template('foodAlerts.html', showSearch=False, showFood=True, foodDone=False)
        else:
            return render_template('foodAlerts.html', showSearch=True, showFood=False, foodDone=True)

# Text Food ------------------------
@app.route('/textFood')
def textFood():
    sendTextForFood('Burrito Bar','NDH')
    return render_template('foodAlerts.html', showSearch=True, showFood=False, foodDone=True)

# Menu Planner ----------------------
@app.route('/menuPlanner', methods=['GET','POST'])
def menuPlanner():
    if request.method == 'GET':
        return render_template('menuPlanner.html', dayName=nameOfDayInXDays(0), dayNum=0)
    else:
        dayNum = int(request.form['dayNum']) + 1
        if dayNum <= 6:
            writeFileFromForm(request.form)
            return render_template('menuPlanner.html', dayName=nameOfDayInXDays(dayNum), dayNum=dayNum)
        else:
            writeFileFromForm(request.form)
            return redirect(url_for('myMenu'))

# My Menu ---------------------------
@app.route('/myMenu')
def myMenu():
    realMenu = nutrition.structfromFile()
    print realMenu
    return render_template('myMenu.html', Menu=realMenu)

# Macro Tracker ----------------------
@app.route('/macroTracker')
def macroTracker():
    macros = getMacros()
    return render_template('macroTracker.html', macros=macros)

# Main Execution ------------------------------------------