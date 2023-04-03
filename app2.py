from flask import Flask,flash,redirect,request,url_for,render_template,session
from flask_session import Session
from flask_mysqldb import MySQL
from otp import genotp
from cmail import sendmail
import random
app=Flask(__name__)
app.secret_key='876@#^%jh'
app.config['SESSION_TYPE']='filesystem'
app.config['MYSQL_HOST']='localhost'
app.config['MYSQL_USER']='root'
app.config['MYSQL_PASSWORD']='admin'
app.config['MYSQL_DB']='SPM'
Session(app)
mysql=MySQL(app)
@app.route('/')
def index():
    return render_template('index.html')
@app.route('/registration',methods=['GET','POST'])
def register():
    if request.method=='POST':
        rollno=request.form['rollno']
        name=request.form['name']
        group=request.form['group']
        password=request.form['password']
        code=request.form['code']
        email=request.form['email']
        #define college code
        ccode='sdmsmkpbsc$#23'
        if ccode==code:
            cursor=mysql.connection.cursor()
            cursor.execute('select rollno from student')
            data=cursor.fetchall()
            cursor.execute('SELECT email from student')
            edata=cursor.fetchall()
            #print(data)
            if (rollno,) in data:
                flash('User already exists')
                return render_template('register.html')
            if (email,) in edata:
                flash('Email id already exists')
                return render_template('register.html')
            cursor.close()
            otp=genotp()
            sendmail(email,otp)
            return render_template('otp.html',otp=otp,rollno=rollno,name=name,group=group,password=password,email=email)
            return otp
        else:
            flash('Invalid college code')
            return render_template('register.html')
    return render_template('register.html')
@app.route('/login',methods=['GET','POST'])
def login():
        if session.get('user'):
            return redirect(url_for('home'))
        if request.method=='POST':
            rollno=request.form['id']
            password=request.form['password']
            cursor=mysql.connection.cursor()
            cursor.execute('select count(*) from  student where rollno=%s and password=%s',[rollno,password])
            count=cursor.fetchone()[0]
            if count==0:
                flash('Invalid roll no or password')
                return render_template('login.html')
            else:
                session['user']=rollno
                return redirect(url_for('home'))
        return render_template('login.html')
@app.route('/studenthome')
def home():
    if session.get('user'):
        return render_template('home.html')
    else:
        flash('LOGIN FIRST')
        return redirect(url_for('login'))
@app.route('/logout')
def logout():
    if session.get('user'):
        session.pop('user')
        return redirect(url_for('index'))
    else:
        flash(" you are already signedoff")
        return redirect(url_for('login'))
@app.route('/otp/<otp>/<name>/<rollno>/<group>/<password>/<email>',methods=['GET','POST'])
def otp(otp,rollno,name,group,password,email):
    if request.method=='POST':
        uotp=request.form['otp']
        if otp==uotp:
            cursor=mysql.connection.cursor()
            lst=[rollno,name,group,password,email]
            query='insert into student values(%s,%s,%s,%s,%s)'
            cursor.execute(query,lst)
            mysql.connection.commit()
            cursor.close()
            flash('Details Registered')
            return redirect(url_for('login'))
        else:
            flash('Wrong OTP')
            return render_template('otp.html',otp=otp,rollno=rollno,name=name,group=group,password=password,email=email)
@app.route('/noteshome')
def notehome():
    if session.get('user'):
        return render_template('addnotetable.html')
    else:
        return redirect(url_for('login'))
@app.route('/addnotes')
def addnote():
    if session.get('user'):
        return render_template('notes.html')
    else:
        return  redirect(url_for('login'))
app.run(use_reloader=True,debug=True)
    
    

            

 
