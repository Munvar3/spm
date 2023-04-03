from flask import Flask,request,redirect,render_template,url_for,flash,session
from flask_mysqldb import MySQL
from flask_session import Session
from otp import genotp
from cmail import sendmail
import random
app=Flask(__name__)
app.secret_key='67@ouihfg'
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
            cursor.execute('SELECT email from student');
            edata=cursor.fetchall()
            #print(data)
            if(rollno,) in data:
                flash('user already exists')
                return render_template('register.html')
            if(email,) in edata:
                flash('email id already exists')
                return render_template('register.html')
            cursor.close()
            otp=genotp()
            sendmail(email,otp)
            return render_template('otp.html',otp=otp,rollno=rollno,name=name,group=group,password=password,email=email)
        else:
            flash('invalid college code')
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
        cursor.execute('select count(*) from student where rollno=%s and password=%s',[rollno,password])
        count=cursor.fetchone() [0]
        if count==0:
            flash('Invalid rollno or password')
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
        #implement flash
        flash('LOGIN FIRST')
        return redirect(url_for('login'))
@app.route('/logout')
def logout():
    if session.get('user'):
        session.pop('user')
        return redirect(url_for('index'))
    else:
        flash('Already logged out')
        return redirect(url_for('login'))       
@app.route('/otp/<otp>/<rollno>/<name>/<group>/<password>/<email>',methods=['GET','POST'])
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
            flash('Details registered')
            return redirect(url_for('login'))
        else:
            flash('WRONG OTP')
            return render_template('otp.html',otp=otp,rollno=rollno,name=name,group=group,password=password,email=email)
@app.route('/noteshome')
def notehome():
    if session.get('user'):
        return render_template('addnotetable.html')
    else:
        return redirect(url_for('login'))
@app.route('/addnotes',methods=['GET','POST'])
def addnote():
    if session.get('user'):
        if request.method=='POST':
            tittle=request.form['title']
            content=request.form['content']
            cursor=mysql.connection.cursor()
            rollno=session.get('user')
            cursor.execute('insert into notes(rollno,tittle,content)values(%s,%s,%s)',[rollno,tittle,content])
            mysql.connection.commit()
            cursor.close()
            flash(f'{tittle} added successfully')
            return redirect(url_for('notehome'))            
        return render_template('notes.html')
    else:
        return redirect(url_for('login'))

@app.route('/updatenote/<nid>',methods=['GET','POST'])
def updatenotes(nid):
    if session.get('user')
    cursor=mysql.connection.cursor()
    cursor.execute('select tittle,content from notes
    data=cursor.fetchone()
    cursor.close()
            if request.method=='POST'
                   title=request.form['title']
                   content=request.form['content']
                   cursor=mysql.connection.cursor()
                   cursor.execute('update notes set tittle=%s,content=%s where nid =%s',[title,content,nid])
                   mysql.connection.commit()
                   cursor.close()
                   flash("notes updated succesfully")
                   return redirect(url_for('noteshome'))
            return render_template




@app.route('\deletenotes/<nid>)')
def deletenotes(nid)
    cursor=mysql.connection.cursor()
    cursor.execute('delete from notes where nid=%s',['nid'])
    
    
    mysqlapp.run(use_reloader=True,debug=True)



