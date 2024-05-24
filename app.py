from flask import Flask, url_for, request, redirect, render_template, session, flash
import os
from werkzeug.utils import secure_filename
import mysql.connector
from passlib.hash import sha256_crypt
from functools import wraps
import math, random
import requests
import re
import secrets
import string

mysqldb = mysql.connector.connect(
            host = 'localhost',
            user = 'root',
            password = '',
            database = 'Art Genics'
          )

app = Flask(__name__)



# Password verification starts
def password_verification(pwd):
    password = pwd
    flag = 0
    while True:
        if (len(password)<8):
            flag = -1
            break
        elif not re.search("[a-z]", password):
            flag = -1
            break
        elif not re.search("[A-Z]", password):
            flag = -1
            break
        elif not re.search("[0-9]", password):
            flag = -1
            break
        elif re.search("\s", password):
            flag = -1
            break
        else:
            flag = 0
            return True
            break

    if flag ==-1:
        return False
# Password verification ends

# Upload files starts
UPLOAD_FOLDER = 'C:/Users/hp/Desktop/Art Genics Project/Art Genics Project/static/upload/addart'
ALLOWED_EXTENSIONS = {'pdf','png','jpg','jpeg'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.',1)[1].lower() in ALLOWED_EXTENSIONS
# Upload files ends


# Login required function starts
def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            return redirect(url_for('index'))
    return wrap
# Login required function ends


# OTP function starts
def generateOTP():
    digits = "0123456789"
    OTP = ""
    for i in range(4):
        OTP += digits[math.floor(random.random() * 10)]
    return OTP

url = "https://www.fast2sms.com/dev/bulk"
# OTP function ends


# Register page starts
@app.route('/register', methods = ['GET','POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        address = request.form['address']
        password = sha256_crypt.encrypt(str(request.form['password']))
        category = request.form['category']
        pwd = request.form['password']
        result = password_verification(pwd)

        #email validation
        cur = mysqldb.cursor()
        cur.execute('SELECT * FROM register WHERE email = %s', [email])
        emails = cur.fetchone()
        if emails:
            flash(u'E-mail ID already registered','warning')
            return redirect(url_for('register'))

        #Mobile number validation
        cur = mysqldb.cursor()
        cur.execute('SELECT * FROM register WHERE phone = %s', [phone])
        phones = cur.fetchone()
        if phones:
            flash(u'Mobile Number already registered','warning')
            return redirect(url_for('register'))

        #password verification
        cur = mysqldb.cursor()
        if result:
            cur.execute('INSERT INTO register(name, email, phone, address, password, category) VALUES(%s,%s,%s,%s,%s,%s)', (name, email, phone, address, password, category))
            mysqldb.commit()
            cur.close()
            flash(u'Registration Successfull!', 'success')
            return redirect(url_for('index'))
        else:
            flash(u'Weak Password!', 'warning')
    return render_template('register.html')
# Registration page ends


# Main index login page starts
@app.route('/', methods = ['GET','POST'])
def index():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        cur = mysqldb.cursor()
        cur.execute('SELECT * FROM register WHERE email = %s',[email])
        res = cur.fetchone()
        if res:
            passwd = res[5]
            if sha256_crypt.verify(password,passwd):
                session['logged_in'] = True
                session['email'] = email
                session['fullname'] = res[1]
                session['id']=res[0]
                return redirect(url_for('home'))
            else:
                flash(u'Inavlid password!', 'error')
                return redirect(url_for('index'))
        else:
            flash(u'Inavlid Email-ID!', 'error')
            return redirect(url_for('index'))

    return render_template('index.html')
# Main index login page ends


# Forgot password page starts
lis = []
@app.route('/forgot', methods = ['GET','POST'])
def forgot():
    if request.method == 'POST':
        phone = request.form['phone']
        otp = generateOTP()
        cur = mysqldb.cursor()
        cur.execute('SELECT * FROM register WHERE phone = %s',[phone])
        res = cur.fetchone()
        if res:
            lis.append(phone)
            lis.append(otp)
            querystring = {"authorization":"UMN2jGrthQWZmBlJfKVTgaHOxAR6bq1XEoydLvPIw39scu5708uRKPgHN9DUeM34vLjSC8tbXcGBFhf0","sender_id":"FSTSMS","language":"english","route":"qt","numbers":phone,"message":"28361","variables":"{#AA#}","variables_values":otp}
            headers = {
            'cache-control': "no-cache"
            }
            response = requests.request("GET", url, headers=headers, params=querystring)
            return redirect(url_for('otps'))
        else:
            flash(u'Not yet registered with this number', 'error')
            return redirect(url_for('forgot'))
    return render_template('forgot.html')
# Forgot password page ends


# Otp page starts
@app.route('/otp', methods = ['GET','POST'])
def otps():
    otp = lis[1]
    if request.method == 'POST':
        otpss = request.form['otp']
        if otp == otpss:
            return redirect(url_for('changepassword'))
        else:
            flash(u'Invalid OTP', 'warning')
    return render_template('otp.html')
# Otp page ends


# Change password page starts
@app.route('/changepassword', methods = ['GET','POST'])
def changepassword():
    phone = lis[0]
    if request.method == 'POST':
        password = sha256_crypt.encrypt(str(request.form['password']))
        cur = mysqldb.cursor()
        cur.execute('UPDATE register SET password = %s WHERE phone = %s',(password,phone))
        mysqldb.commit()
        cur.close()
        lis.clear()
        flash(u'Password changed Successfully','success')
        return redirect(url_for('index'))
    return render_template('changepassword.html')
# Change password page ends


# log out
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))
# Log out


# Home page starts
@app.route('/home', methods = ['GET','POST'])
@login_required
def home():
    return render_template('home.html')
# Home page ends


# Artworks page starts
@app.route('/artworks', methods = ['GET','POST'])
@login_required
def artworks():
    cur = mysqldb.cursor()
    cur.execute('SELECT * FROM addart')
    res = cur.fetchall()
    cur.close()
    return render_template('artworks.html', res = res)
# Artworks page ends


# Art page starts
@app.route('/art/<string:id>', methods = ['GET','POST'])
def art(id):
    cur = mysqldb.cursor()
    cur.execute('SELECT * FROM addart WHERE id = %s',[id])
    res = cur.fetchone()
    if request.method == 'POST':
        name = request.form['fullname']
        bidamount = request.form['bidamount']
        cur = mysqldb.cursor()
        id = id
        cur.execute('INSERT INTO bidding (name, bidamount, paint_id) VALUES(%s,%s,%s)',(name, bidamount, id))
        mysqldb.commit()
        cur.close()
    cur = mysqldb.cursor()
    cur.execute('SELECT * FROM bidding WHERE paint_id=%s ORDER BY bidamount DESC',[id])
    rest = cur.fetchall()
    return render_template("art.html",res = res,rest = rest)
# Art page ends


# Seller details page starts
@app.route('/sellerdetails/<string:id>', methods = ['GET','POST'])
def sellerdetails(id):
    cur = mysqldb.cursor()
    cur.execute('SELECT * FROM register WHERE id = %s', [id])
    res = cur.fetchone()
    return render_template('sellerdetails.html', res = res)
# Seller details page ends


# Buyer details page starts
@app.route('/buyerdetails/<string:id>', methods = ['GET','POST'])
def buyerdetails(id):
    cur = mysqldb.cursor()
    cur.execute('SELECT * FROM register WHERE id = %s', [id])
    res = cur.fetchone()
    return render_template('buyerdetails.html', res = res)
# Buyer details page ends


#Past auctions page starts
@app.route('/pastauctions', methods = ['GET','POST'])
def pastauctions():
    cur = mysqldb.cursor()
    cur.execute('SELECT * FROM finalbid')
    winner = cur.fetchall()
    return render_template('pastauctions.html', winner = winner)
#Past auctions page ends

# Finalbid starts
@app.route('/finalbid/<string:id>', methods = ['GET','POST'])
def finalbid(id):
    if request.method == 'POST':
        res = request.form['result']

        # Selecting the maximum amount bidded on artwork
        cur = mysqldb.cursor()
        cur.execute('SELECT max(bidamount),name from bidding where paint_id=%s',[id])
        maxi = cur.fetchone()

        # Selecting the artwork which the timer has ended
        cur = mysqldb.cursor()
        cur.execute('SELECT * from addart where id=%s',[id])
        img = cur.fetchone()

        # Selecting the details of the aucion winner and inserting in finalbid table
        seller = img[1]
        contact = img[14]
        artist = img[2]
        arttitle = img[3]
        amount = maxi[1]
        winner = maxi[0]
        artwork = img[15]
        cur = mysqldb.cursor()
        cur.execute('INSERT INTO finalbid(seller,contact, artistname, arttitle, finalprice, winner, artimage) VALUES(%s, %s, %s, %s, %s, %s, %s)',(seller, contact, artist, arttitle, winner, amount, artwork))
        mysqldb.commit()
        cur.close()

        # Deleting artwork which is sold
        cur = mysqldb.cursor()
        cur.execute('DELETE FROM bidding WHERE paint_id=%s',[id])
        mysqldb.commit()
        cur.close()
        cur = mysqldb.cursor()
        cur.execute('DELETE FROM addart WHERE id=%s',[id])
        mysqldb.commit()
        cur.close()

        # Displaying sold artworks in past auctions page
        cur = mysqldb.cursor()
        cur.execute('SELECT * from finalbid')
        final = cur.fetchall()
        return render_template('artworks.html',final = final)
# Finalbid ends


# Artworkbids page starts
@app.route('/artworkbids/<string:id>', methods = ['GET','POST'])
def artworkbids(id):
    cur = mysqldb.cursor()
    cur.execute('SELECT * FROM addart WHERE id = %s', [id])
    res = cur.fetchone()
    cur = mysqldb.cursor()
    return render_template('artworkbids.html', res = res)
# Artworkbids page ends


# Consign page starts
@app.route('/consign', methods = ['GET','POST'])
@login_required
def consign():
    return render_template('consign.html')
# Consign page ends


# Addart page starts
@app.route('/addart', methods = ['GET','POST'])
@login_required
def addart():
    if request.method == 'POST':
        sellername = request.form['sellername']
        artistname = request.form['artistname']
        artworktitle = request.form['artworktitle']
        category = request.form['category']
        year = request.form['year']
        height = request.form['height']
        width = request.form['width']
        sign = request.form['sign']
        certificate = request.form['certificate']
        acquire = request.form['acquire']
        city = request.form['city']
        minprice = request.form['minprice']
        date = request.form['date']
        time = request.form['time']
        res = date +" "+time

        phone = request.form['phone']
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'],filename))

        cur = mysqldb.cursor()
        cur.execute('INSERT INTO addart(sellername, artistname, artworktitle, category, year, height, width, sign, certificate, acquire, city, minprice, date, phone, file) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)',(sellername, artistname, artworktitle, category, year, height, width, sign, certificate, acquire, city, minprice, res, phone, filename))
        mysqldb.commit()
        cur.close()
        flash(u'Artwork Submitted Succesfully!','success')
        return redirect(url_for('home'))
    return render_template('addart.html')
# Addart page ends

# Profile page starts
@app.route('/profile/<string:id>', methods = ['GET','POST'])
@login_required
def profile(id):
    cur = mysqldb.cursor()
    cur.execute('SELECT * FROM register where id=%s ',[id])
    res = cur.fetchone()
    return render_template('profile.html', res = res)


# Profile edit page starts
@app.route('/profileedit/<string:id>', methods = ['GET','POST'])
def profileedit(id):
    cur = mysqldb.cursor()
    cur.execute('SELECT * FROM register WHERE id = %s', [id])
    res = cur.fetchone()
    return render_template('profileedit.html', res = res)

@app.route('/updateinformation/<string:id>', methods = ['GET','POST'])
def updateinformation(id):
    cur = mysqldb.cursor()
    cur.execute('SELECT * FROM register WHERE id = %s', [id])
    res = cur.fetchone()
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        address = request.form['address']

        cur = mysqldb.cursor()
        cur.execute('UPDATE register SET name = %s, email = %s, phone = %s, address = %s WHERE id = %s', (name, email, phone, address, id))
        mysqldb.commit()
        flash(u'Information Updated Succesfully','success')
        cur = mysqldb.cursor()
        cur.execute('SELECT * FROM register WHERE id = %s', [id])
        res = cur.fetchone()
        return render_template('profileedit.html', res = res)
    return render_template('profileedit.html', res = res)

# Settings page ends


# Admin Module starts

# Admin login required function
def login_required1(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            return redirect(url_for('adminlogin'))
    return wrap

# Admin Login page starts
@app.route('/adminlogin', methods = ['GET','POST'])
def adminlogin():
    if request.method == 'POST':
        name = request.form['name']
        password = request.form['password']
        cur = mysqldb.cursor()
        cur.execute('SELECT * FROM admin WHERE id = 1')
        res = cur.fetchone()
        if name == res[1] and password == res[4]:
            session['logged_in'] = True
            return redirect(url_for('adminhome'))
        else:
            flash(u,'Invalid Credentials','error')
            return redirect(url_for('adminlogin'))
    return render_template('adminlogin.html')
# Admin Login page ends

# Admin log out starts
@app.route('/adminlogout')
@login_required1
def adminlogout():
    session.clear()
    return redirect(url_for('index'))
# Admin Log out ends

# Adminhome page starts
@app.route('/adminhome', methods = ['GET','POST'])
@login_required1
def adminhome():
    return render_template('adminhome.html')
# Adminhome page ends


# Adminusers page starts
@app.route('/adminusers', methods = ['GET','POST'])
@login_required1
def adminusers():
    cur = mysqldb.cursor()
    cur.execute('SELECT * FROM register')
    res = cur.fetchall()
    return render_template('adminusers.html', res = res)
# Adminusers page ends

# Admin edituser page starts
@app.route('/adminedituser/<string:id>', methods = ['GET','POST'])
@login_required1
def adminuserdetails(id):
    cur = mysqldb.cursor()
    cur.execute('SELECT * FROM register WHERE id = %s', [id])
    res = cur.fetchone()
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        address = request.form['address']
        cur.execute('UPDATE buyer SET name = %s, email = %s, phone = %s, address = %s WHERE id = %s', (name, email, phone, address, id))
        mysqldb.commit()
        cur.close()
        return redirect(url_for('adminusers'))
    else:
        flash(u'Error!', 'warning')
    return render_template('adminedituser.html', res = res)
# Admin edituser page ends

# Admin delete user starts
@app.route('/admindeleteuser/<string:id>', methods = ['GET','POST'])
@login_required1
def deleteuser(id):
    cur = mysqldb.cursor()
    cur.execute('DELETE FROM register WHERE id = %s', [id])
    mysqldb.commit()
    return redirect(url_for('adminusers'))
# Admin delete user ends


# Admin auctions page starts
@app.route('/adminauctions', methods = ['GET','POST'])
@login_required1
def adminauctions():
    cur = mysqldb.cursor()
    cur.execute('SELECT * FROM addart')
    res = cur.fetchall()
    cur.close()
    return render_template('adminauctions.html', res = res)
# Admin auctions page ends

#Adminart page starts
@app.route('/adminart/<string:id>', methods = ['GET','POST'])
def adminart(id):
    cur = mysqldb.cursor()
    cur.execute('SELECT * FROM addart WHERE id = %s',[id])
    res = cur.fetchone()
    if request.method == 'POST':
        name = request.form['fullname']
        bidamount = request.form['bidamount']
        cur = mysqldb.cursor()
        id = id
        cur.execute('INSERT INTO bidding (name, bidamount, paint_id) VALUES(%s,%s,%s)',(name, bidamount, id))
        mysqldb.commit()
        cur.close()
    cur = mysqldb.cursor()
    cur.execute('SELECT * FROM bidding WHERE paint_id=%s ORDER BY bidamount DESC',[id])
    rest = cur.fetchall()
    return render_template("adminart.html",res = res,rest = rest)
#Adminart page ends

# Adminauctions page delete artwork starts
@app.route('/deleteartwork/<string:id>', methods = ['GET','POST'])
@login_required1
def deleteartwork(id):
    cur = mysqldb.cursor()
    cur.execute('DELETE FROM addart WHERE id = %s', [id])
    mysqldb.commit()
    return redirect(url_for('adminauctions'))
# Adminauctions page delete artwork ends


#adminpastauctions page starts
@app.route('/adminpastauctions', methods = ['GET','POST'])
def adminpastauctions():
    cur = mysqldb.cursor()
    cur.execute('SELECT * FROM finalbid')
    winner = cur.fetchall()
    return render_template('adminpastauctions.html', winner = winner)
#adminpastauctions page ends

# Admin Moudle ends


if __name__ == '__main__':
    app.secret_key='123'
    app.run()
