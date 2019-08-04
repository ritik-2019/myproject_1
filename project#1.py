from flask import Flask, render_template, request,redirect,url_for,session
from werkzeug.utils import secure_filename
import pymysql
from mylib import *
import time
import os
from mylib import check_photo_admin



app=Flask(__name__)

app.secret_key = "super secret key"
app.config['UPLOAD_FOLDER']='./static/photos'
app.config['UPLOAD_FOLDER_PRODUCT']='./static/product_photos'


@app.route('/')
def welcome():
    return render_template('index.html',)

@app.route('/products')
def products():
    conn = pymysql.connect(
        user='root',
        passwd='',
        port=3306,
        host='localhost',
        db='amajon',
        autocommit=True
    )
    cur = conn.cursor()
    sql = "SELECT * FROM productdata"
    cur.execute(sql)
    result = cur.fetchall()
    return render_template('products.html',result=result)

@app.route('/login')
def login():
    return render_template('Login.html')

@app.route('/checklogin',methods=['GET','POST'])
def checklogin():
    if(request.method=='POST'):
        email=request.form["T1"]
        password=request.form["T2"]

        conn = pymysql.connect(
            user='root',
            passwd='',
            port=3306,
            host='localhost',
            db='amajon',
            autocommit=True
            )
        sql="SELECT * FROM logindata where email='"+email+"' and password='"+password+"'"
        cur=conn.cursor()
        cur.execute(sql)
        n=cur.rowcount
        if n>0:
            row=cur.fetchone()
            usertype=row[2]
            name=row[3]
            session["usertype"]=usertype
            session["email"]=email
            session["name"]=name
            if(usertype=="admin"):
                return redirect(url_for('adminhome'))
            elif(usertype=="seller"):
                return redirect(url_for('sellerhome'))
            elif (usertype =="user"):
                return redirect(url_for('userhome'))
        else:
            return render_template("loginerror.html")

@app.route('/logout')
def logout():
    if 'usertype' in session:
        session.pop('usertype',None)
        session.pop('email',None)
        session.pop('name',None)
        return render_template('Login.html')
    else:
        return render_template('Login.html')

@app.route('/autherror')
def autherror():
    return render_template('autherror.html')

@app.route('/adminhome')
def adminhome():
    if 'usertype' in session:
        usertype=session['usertype']
        email=session['email']
        if usertype=='admin':
            photo=check_photo_admin(email)
            name=get_admin_name(email)
            return render_template('admin_home.html',e1=email,photo=photo,name=name)
        else:
            return redirect(url_for('autherror'))
    else:
        return redirect(url_for('autherror'))

@app.route('/userhome')
def userhome():
    if 'usertype' in session:
        usertype=session['usertype']
        email=session['email']
        if usertype=='user':
            photo=check_photo_user(email)
            name=get_user_name(email)
            conn = pymysql.connect(
                user='root',
                passwd='',
                port=3306,
                host='localhost',
                db='amajon',
                autocommit=True
            )
            cur = conn.cursor()
            sql = "SELECT * FROM productdata"
            cur.execute(sql)
            result = cur.fetchall()
            return render_template('user_home.html',e1=email,photo=photo,name=name,result=result)
        else:
            return redirect(url_for('autherror'))
    else:
        return redirect(url_for('autherror'))

@app.route('/sellerhome')
def sellerhome():
    if 'usertype' in session:
        usertype=session['usertype']
        email=session['email']
        if usertype=='seller':
            photo=check_photo_seller(email)
            name=get_seller_name(email)
            return render_template('seller_home.html',e1=email,photo=photo,name=name)
        else:
            return redirect(url_for('autherror'))
    else:
        return redirect(url_for('autherror'))

@app.route('/adminreg',methods=['GET','POST'])
def adminreg():
    if 'usertype' in session:
        usertype=session['usertype']
        email=session['email']
        if usertype=='admin':
            if request.method =='POST':
                name =request.form['T1']
                address = request.form['T2']
                contact = request.form['T3']
                email = request.form['T4']
                password = request.form['T5']
                ut="admin"
                conn = pymysql.connect(
                    user='root',
                    passwd='',
                    port=3306,
                    host='localhost',
                    db='amajon',
                    autocommit=True
                        )
                cur=conn.cursor()
                sql = "insert into admindata values('" + name + "','" + address + "','" + contact + "','" + email + "')"
                sql2 = "insert into logindata values('" + email + "','" + password + "','" + ut + "','" + name + "')"
                cur.execute(sql)
                cur.execute(sql2)
                return render_template('admin_reg.html',result="Data Saved")
            else:
                return render_template('admin_reg.html')
        else:
            return redirect(url_for('autherror'))
    else:
        return redirect(url_for('autherror'))

@app.route('/sellerreg',methods=['GET','POST'])
def sellerreg():
        if request.method =='POST':
            name =request.form['T1']
            address = request.form['T2']
            contact = request.form['T3']
            email = request.form['T4']
            password = request.form['T5']
            ut="seller"
            conn = pymysql.connect(
                    user='root',
                    passwd='',
                    port=3306,
                    host='localhost',
                    db='amajon',
                    autocommit=True
            )
            cur=conn.cursor()
            sql = "insert into sellerdata values('" + name + "','" + address + "','" + contact + "','" + email + "')"
            sql2 = "insert into logindata values('" + email + "','" + password + "','" + ut + "','" + name + "')"
            cur.execute(sql)
            cur.execute(sql2)
            return render_template('seller_reg.html',result="Data Saved")
        else:
            return render_template('seller_reg.html')


@app.route('/userreg',methods=['GET','POST'])
def userreg():
        if request.method =='POST':
            name =request.form['T1']
            address = request.form['T2']
            contact = request.form['T3']
            email = request.form['T4']
            password = request.form['T5']
            ut="user"
            conn = pymysql.connect(
                    user='root',
                    passwd='',
                    port=3306,
                    host='localhost',
                    db='amajon',
                    autocommit=True
                        )
            cur=conn.cursor()
            sql = "insert into userdata values('" + name + "','" + address + "','" + contact + "','" + email + "')"
            sql2 = "insert into logindata values('" + email + "','" + password + "','" + ut + "','" + name + "')"
            cur.execute(sql)
            cur.execute(sql2)
            return render_template('user_reg.html',result="Data Saved")
        else:
            return render_template('user_reg.html')


@app.route('/showadmins')
def showadmins():
    if 'usertype' in session:
        usertype=session['usertype']
        email=session['email']
        if usertype=='admin':
            conn = pymysql.connect(
                user='root',
                passwd='',
                port=3306,
                host='localhost',
                db='doctorfinder',
                autocommit=True
            )
            cur=conn.cursor()
            sql="select * from admindata"
            cur.execute(sql)
            result=cur.fetchall()
            return render_template('show_admins.html',result=result)
        else:
            return redirect(url_for('autherror'))
    else:
        return redirect(url_for('autherror'))

@app.route('/showsellers')
def showsellers():
    if 'usertype' in session:
        usertype=session['usertype']
        email=session['email']
        if usertype=='admin':
            conn = pymysql.connect(
                user='root',
                passwd='',
                port=3306,
                host='localhost',
                db='amajon',
                autocommit=True
            )
            cur=conn.cursor()
            sql="select * from sellerdata"
            cur.execute(sql)
            result=cur.fetchall()
            return render_template('show_sellers.html',result=result)
        else:
            return redirect(url_for('autherror'))
    else:
        return redirect(url_for('autherror'))

@app.route('/adminphoto')
def adminphoto():
    return render_template('photoupload_admin.html')

@app.route('/adminphoto1',methods=['GET','POST'])
def adminphoto1():
    if 'usertype' in session:
        usertype=session['usertype']
        e1=session['email']
        if usertype=='admin':
            if request.method =='POST':
                file=request.files['F1']
                if file:
                    path = os.path.basename(file.filename)
                    file_ext =os.path.splitext(path)[1][1:]
                    filename= str(int(time.time())) + '.' + file_ext
                    filename= secure_filename(filename)
                    conn = pymysql.connect(
                        passwd='',
                        host='localhost',
                        user='root',
                        port=3306,
                        db='amajon',
                        autocommit=True
                    )
                    cur=conn.cursor()
                    sql="insert into photodata_admin values('"+e1+"','"+filename+"')"

                    try:
                        cur.execute(sql)
                        n=cur.rowcount
                        if n==1:
                            file.save(os.path.join(app.config['UPLOAD_FOLDER'],filename))
                            return render_template('photoupload_admin1.html',result="success")
                        else:
                            return render_template('photoupload_admin.html',result="failure")
                    except:
                        return render_template('photoupload_admin.html',result="duplicate")
                else:
                    return render_template('photoupload_admin.html')
            else:
                return redirect(url_for('autherror'))
        else:
            return redirect(url_for('autherror'))

@app.route('/change_adminphoto')
def change_adminphoto():
    if 'usertype' in session:
        usertype=session['usertype']
        email=session['email']
        if usertype=='admin':
            photo = check_photo_admin(email)
            conn = pymysql.connect(
                user='root',
                passwd='',
                port=3306,
                host='localhost',
                db='amajon',
                autocommit=True

            )
            cur = conn.cursor()
            sql="delete from photodata_admin where email='"+email+"'"
            cur.execute(sql)
            n=cur.rowcount
            if n>0:
                os.remove("./static/photos/"+photo)
                return render_template('change_admin_photo.html',data="success")
            else:
                return render_template('change_admin_photo.html', data="failure")
        else:
            return redirect(url_for('autherror'))
    else:
        return redirect(url_for('autherror'))

@app.route('/userphoto')
def userphoto():
    return render_template('photoupload_user.html')

@app.route('/userphoto1',methods=['GET','POST'])
def userphoto1():
    if 'usertype' in session:
        usertype=session['usertype']
        e1=session['email']
        if usertype=='user':
            if request.method =='POST':
                file=request.files['F1']
                if file:
                    path = os.path.basename(file.filename)
                    file_ext =os.path.splitext(path)[1][1:]
                    filename= str(int(time.time())) + '.' + file_ext
                    filename= secure_filename(filename)
                    conn = pymysql.connect(
                        passwd='',
                        host='localhost',
                        user='root',
                        port=3306,
                        db='amajon',
                        autocommit=True
                    )
                    cur=conn.cursor()
                    sql="insert into photodata_user values('"+e1+"','"+filename+"')"

                    try:
                        cur.execute(sql)
                        n=cur.rowcount
                        if n==1:
                            file.save(os.path.join(app.config['UPLOAD_FOLDER'],filename))
                            return render_template('photoupload_user1.html',result="success")
                        else:
                            return render_template('photoupload_user.html',result="failure")
                    except:
                        return render_template('photoupload_user.html',result="duplicate")
                else:
                    return render_template('photoupload_user.html')
            else:
                return redirect(url_for('autherror'))
        else:
            return redirect(url_for('autherror'))

@app.route('/change_userphoto')
def change_userphoto():
    if 'usertype' in session:
        usertype=session['usertype']
        email=session['email']
        if usertype=='user':
            photo = check_photo_user(email)
            conn = pymysql.connect(
                user='root',
                passwd='',
                port=3306,
                host='localhost',
                db='amajon',
                autocommit=True

            )
            cur = conn.cursor()
            sql="delete from photodata_user where email='"+email+"'"
            cur.execute(sql)
            n=cur.rowcount
            if n>0:
                os.remove("./static/photos/"+photo)
                return render_template('change_user_photo.html',data="success")
            else:
                return render_template('change_user_photo.html', data="failure")
        else:
            return redirect(url_for('autherror'))
    else:
        return redirect(url_for('autherror'))

@app.route('/sellerphoto')
def sellerphoto():
    return render_template('photoupload_seller.html')

@app.route('/sellerphoto1',methods=['GET','POST'])
def sellerphoto1():
    if 'usertype' in session:
        usertype=session['usertype']
        e1=session['email']
        if usertype=='seller':
            if request.method =='POST':
                file=request.files['F1']
                if file:
                    path = os.path.basename(file.filename)
                    file_ext =os.path.splitext(path)[1][1:]
                    filename= str(int(time.time())) + '.' + file_ext
                    filename= secure_filename(filename)
                    conn = pymysql.connect(
                        passwd='',
                        host='localhost',
                        user='root',
                        port=3306,
                        db='amajon',
                        autocommit=True
                    )
                    cur=conn.cursor()
                    sql="insert into photodata_seller values('"+e1+"','"+filename+"')"

                    try:
                        cur.execute(sql)
                        n=cur.rowcount
                        if n==1:
                            file.save(os.path.join(app.config['UPLOAD_FOLDER'],filename))
                            return render_template('photoupload_seller1.html',result="success")
                        else:
                            return render_template('photoupload_seller.html',result="failure")
                    except:
                        return render_template('photoupload_seller.html',result="duplicate")
                else:
                    return render_template('photoupload_seller.html')
            else:
                return redirect(url_for('autherror'))
        else:
            return redirect(url_for('autherror'))

@app.route('/change_sellerphoto')
def change_sellerphoto():
    if 'usertype' in session:
        usertype=session['usertype']
        email=session['email']
        if usertype=="seller":
            photo = check_photo_seller(email)
            conn = pymysql.connect(
                user='root',
                passwd='',
                port=3306,
                host='localhost',
                db='amajon',
                autocommit=True

            )
            cur = conn.cursor()
            sql="delete from photodata_seller where email='"+email+"'"
            cur.execute(sql)
            n=cur.rowcount
            if n>0:
                os.remove("./static/photos/"+photo)
                return render_template('change_seller_photo.html',data="success")
            else:
                return render_template('change_seller_photo.html', data="failure")
        else:
            return redirect(url_for('autherror'))
    else:
        return redirect(url_for('autherror'))


@app.route('/change_password_admin',methods=['GET','POST'])
def change_password_admin():
    if 'usertype' in session:
        usertype=session['usertype']
        e1=session['email']
        if usertype=='admin':
            if request.method=='POST':
                oldpass=request.form['T1']
                newpass=request.form['T2']
                conn = pymysql.connect(
                    host='localhost',
                    port=3306,
                    user='root',
                    passwd='',
                    db='amajon',
                    autocommit=True
                )
                cur = conn.cursor()
                sql="update logindata set password='"+newpass+"' where email='"+e1+"' AND password='"+oldpass+"'"
                cur.execute(sql)
                n=cur.rowcount
                msg="Incorrect old password"
                if n==1:
                    msg="Your Password Has Been Changed"
                return render_template('ChangePasswordAdmin.html',msg=msg)
            else:
                return render_template('ChangePasswordAdmin.html')
        else:
            return redirect(url_for('autherror'))
    else:
        return redirect(url_for('autherror'))

@app.route('/change_password_seller',methods=['GET','POST'])
def change_password_seller():
    if 'usertype' in session:
        usertype=session['usertype']
        e1=session['email']
        if usertype=='seller':
            if request.method=='POST':
                oldpass=request.form['T1']
                newpass=request.form['T2']
                conn = pymysql.connect(
                    host='localhost',
                    port=3306,
                    user='root',
                    passwd='',
                    db='amajon',
                    autocommit=True
                )
                cur = conn.cursor()
                sql="update logindata set password='"+newpass+"' where email='"+e1+"' AND password='"+oldpass+"'"
                cur.execute(sql)
                n=cur.rowcount
                msg="Incorrect old password"
                if n==1:
                    msg="Your Password Has Been Changed"
                return render_template('ChangePasswordSeller.html',msg=msg)
            else:
                return render_template('ChangePasswordSeller.html')
        else:
            return redirect(url_for('autherror'))
    else:
        return redirect(url_for('autherror'))

@app.route('/change_password_user',methods=['GET','POST'])
def change_password_user():
    if 'usertype' in session:
        usertype=session['usertype']
        e1=session['email']
        if usertype=='user':
            if request.method=='POST':
                oldpass=request.form['T1']
                newpass=request.form['T2']
                conn = pymysql.connect(
                    host='localhost',
                    port=3306,
                    user='root',
                    passwd='',
                    db='amajon',
                    autocommit=True
                )
                cur = conn.cursor()
                sql="update logindata set password='"+newpass+"' where email='"+e1+"' AND password='"+oldpass+"'"
                cur.execute(sql)
                n=cur.rowcount
                msg="Incorrect old password"
                if n==1:
                    msg="Your Password Has Been Changed"
                return render_template('ChangePasswordUser.html',msg=msg)
            else:
                return render_template('ChangePasswordUser.html')
        else:
            return redirect(url_for('autherror'))
    else:
        return redirect(url_for('autherror'))

@app.route('/show_sellerprofile')
def show_sellerprofile():
    if 'usertype' in session:
        usertype=session['usertype']
        email=session['email']
        if usertype=='seller':
                conn = pymysql.connect(
                user='root',
                passwd='',
                port=3306,
                host='localhost',
                db='amajon',
                autocommit=True

                )
                cur = conn.cursor()
                cur.execute("SELECT * FROM sellerdata where email='"+email+"'")
                result = cur.fetchone()
                return render_template('show_seller_profile.html',result=result)

        else:
            return redirect(url_for('autherror'))
    else:
        return redirect(url_for('autherror'))

@app.route('/edit_seller',methods=['GET','POST'])
def edit_seller():
    if 'usertype' in session:
        usertype=session['usertype']
        e1 =session['email']
        print("HELLO")
        if usertype=="seller":
            email=request.form['H1']
            conn = pymysql.connect(
                user='root',
                passwd='',
                port=3306,
                host='localhost',
                db='amajon',
                autocommit=True
                )
            cur=conn.cursor()
            print("HELLO")
            cur.execute("select * from sellerdata where email='"+email+"'")
            result=cur.fetchone()
            return render_template('EditSeller.html',result=result)
        else:
            return redirect('autherror.html')


@app.route('/edit_seller_1',methods=['GET','POST'])
def edit_seller_1():
    if 'usertype' in session:
        usertype = session['usertype']
        e1 = session['email']
        if usertype == 'seller':
            name = request.form['T1']
            address = request.form['T2']
            contact = request.form['T3']
            email= request.form['T4']
            sql = "update sellerdata set name='" + name + "',address='" + address + "',contact='" + contact + "' where email='" + email + "'"
            conn = pymysql.connect(
                user='root',
                passwd='',
                port=3306,
                host='localhost',
                db='amajon',
                autocommit=True

            )
            cur = conn.cursor()
            cur.execute(sql)
            n = cur.rowcount
            if n>0:
                return render_template('edit_seller1.html',data="Changes Saved")
            else:
                return render_template('edit_seller1.html',data="Try again")
        else:
            return redirect(url_for('show_sellerprofile'))
    else:
        return redirect(url_for('autherror'))

@app.route('/show_userprofile')
def show_userprofile():
    if 'usertype' in session:
        usertype=session['usertype']
        email=session['email']
        if usertype=='user':
                conn = pymysql.connect(
                user='root',
                passwd='',
                port=3306,
                host='localhost',
                db='amajon',
                autocommit=True

                )
                cur = conn.cursor()
                cur.execute("SELECT * FROM userdata where email='"+email+"'")
                result = cur.fetchone()
                return render_template('show_user_profile.html',result=result)
        else:
            return redirect(url_for('autherror'))
    else:
        return redirect(url_for('autherror'))

@app.route('/edit_user',methods=['GET','POST'])
def edit_user():
    if 'usertype' in session:
        usertype=session['usertype']
        e1 =session['email']
        if usertype=="user":
            email=request.form['H1']
            conn = pymysql.connect(
                user='root',
                passwd='',
                port=3306,
                host='localhost',
                db='amajon',
                autocommit=True
                )
            cur=conn.cursor()

            cur.execute("select * from userdata where email='"+email+"'")
            result=cur.fetchone()
            return render_template('EditUser.html',result=result)
        else:
            return redirect('autherror.html')


@app.route('/edit_user_1',methods=['GET','POST'])
def edit_user_1():
    if 'usertype' in session:
        usertype = session['usertype']
        e1 = session['email']
        if usertype == 'user':
            name = request.form['T1']
            address = request.form['T2']
            contact = request.form['T3']
            email= request.form['T4']
            sql = "update userdata set name='" + name + "',address='" + address + "',contact='" + contact + "' where email='" + email + "'"
            conn = pymysql.connect(
                user='root',
                passwd='',
                port=3306,
                host='localhost',
                db='amajon',
                autocommit=True

            )
            cur = conn.cursor()
            cur.execute(sql)
            n = cur.rowcount
            if n>0:
                return render_template('edit_user1.html',data="Changes Saved")
            else:
                return render_template('edit_user1.html',data="Try again")
        else:
            return redirect(url_for('show_userprofile'))
    else:
        return redirect(url_for('autherror'))

@app.route('/add_product',methods=['GET','POST'])
def add_product():
    print("hello1")
    if 'usertype' in session:
        usertype=session['usertype']
        email=session['email']

        if usertype=='seller':
            print("hello2")
            if request.method=='POST':
                file = request.files['F1']
                if file:
                    path = os.path.basename(file.filename)
                    file_ext = os.path.splitext(path)[1][1:]
                    filename = str(int(time.time())) + '.' + file_ext
                    filename = secure_filename(filename)

                    cate=request.form['T1']
                    prod_name=request.form['T2']
                    comp=request.form['T3']
                    rate=request.form['T4']

                    conn = pymysql.connect(
                    host='localhost',
                    port=3306,
                    user='root',
                    passwd='',
                    db='amajon',
                    autocommit=True
                    )
                    cur = conn.cursor()
                    sql="insert into productdata(category,name,company,rate,photo,sellers_email) values('"+cate+"','"+prod_name+"','"+comp+"','"+rate+"','"+filename+"','"+email+"')"
                    cur.execute(sql)
                    n=cur.rowcount
                    if n==1:
                        msg="Your Product Has Been Added"
                        file.save(os.path.join(app.config['UPLOAD_FOLDER_PRODUCT'], filename))
                        return render_template('AddProduct.html',msg=msg)
                    else:
                        return render_template('AddProduct.html',msg="error occured")
                else:
                    return render_template('AddProduct.html')
            else:
                return render_template('AddProduct.html')
        else:
            return redirect(url_for('autherror'))
    else:
        return redirect(url_for('autherror'))


@app.route('/show_product_sellers')
def show_product_sellers():
    if 'usertype' in session:
        usertype=session['usertype']
        email=session['email']
        if usertype=='seller':
            conn = pymysql.connect(
                user='root',
                passwd='',
                port=3306,
                host='localhost',
                db='amajon',
                autocommit=True
                )
            cur=conn.cursor()
            sql="select * from productdata where sellers_email='"+email+"'"
            cur.execute(sql)
            result=cur.fetchall()
            return render_template('showproduct_sellers.html',result=result)
        else:
            return render_template(url_for('autherror'))
    else:
        return render_template(url_for('autherror'))

@app.route('/remove_product',methods=['GET','POST'])
def remove_product():
    if 'usertype' in session:
        usertype=session['usertype']
        email=session['email']
        if usertype=='seller':
            if request.method=='POST':
                id=request.form['H1']
                conn = pymysql.connect(
                    user='root',
                    passwd='',
                    port=3306,
                    host='localhost',
                    db='amajon',
                    autocommit=True
                )
                cur = conn.cursor()
                sql="delete from productdata where Id='"+id+"'"
                cur.execute(sql)
                n=cur.rowcount
                if n==1:
                    return render_template('remove_prod.html',msg="The Product Has Been Removed Successfully")
                else:
                    return render_template('remove_prod.html',msg="Error Occurred:Try Again")
        else:
            return render_template(url_for(autherror))
    else:
        return render_template(url_for('autherror'))



@app.route('/show_product_user')
def show_product_user():
    if 'usertype' in session:
        usertype=session['usertype']
        email=session['email']
        if usertype=='user':
            conn = pymysql.connect(
                user='root',
                passwd='',
                port=3306,
                host='localhost',
                db='amajon',
                autocommit=True
                )
            cur=conn.cursor()
            sql="select * from productdata"
            cur.execute(sql)
            result=cur.fetchall()
            return render_template('showproduct_user.html',result=result)
        else:
            return render_template(url_for('autherror'))
    else:
        return render_template(url_for('autherror'))






@app.route('/addto_cart',methods=['GET','POST'])
def addto_cart():
    if 'usertype' in session:
        usertype = session['usertype']
        email = session['email']
        name=session['name']
        if usertype == 'user':
            if request.method=='POST':
                id=request.form['H6']
                name_product=request.form['H1']
                company=request.form['H2']
                price=request.form['H3']
                retailer_email=request.form['H5']
                conn = pymysql.connect(
                    user='root',
                    passwd='',
                    port=3306,
                    host='localhost',
                    db='amajon',
                    autocommit=True
                    )
                cur = conn.cursor()
                sql="insert into cart values('"+id+"','"+name_product+"','"+company+"','"+price+"','"+name+"','"+email+"','"+retailer_email+"')"
                cur.execute(sql)
                n=cur.rowcount
                if n==1:
                    return render_template('addtocart.html',msg="Added to cart")
                else:
                    return render_template('addtocart.html',msg="Error:Try Again")
        else:
            return render_template(url_for('autherror'))
    else:
        return render_template(url_for('autherror'))


@app.route('/show_cart')
def show_cart():
    if 'usertype' in session:
        usertype=session['usertype']
        email=session['email']
        if usertype=='user':
            conn = pymysql.connect(
                user='root',
                passwd='',
                port=3306,
                host='localhost',
                db='amajon',
                autocommit=True
                )
            cur=conn.cursor()
            sql="select * from cart where email_user='"+email+"'"
            cur.execute(sql)
            n=cur.rowcount
            if n>0:
                result = cur.fetchall()
                return render_template('showcart_user.html', result=result)

            else:
                return render_template('showcart_user.html', vgt="You don't have anything in your cart at present")
        else:
            return render_template(url_for('autherror'))
    else:
        return render_template(url_for('autherror'))

@app.route('/delete_cart',methods=['GET','POST'])
def delete_cart():
    if 'usertype' in session:
        usertype = session['usertype']
        email = session['email']
        if usertype == 'user':
            if request.method == 'POST':
                id=request.form['R1']
                conn = pymysql.connect(
                    user='root',
                    passwd='',
                    port=3306,
                    host='localhost',
                    db='amajon',
                    autocommit=True
                )
                cur = conn.cursor()
                sql="DELETE from cart where email_user='"+email+"' AND Id='"+id+"' "
                cur.execute(sql)
                n=cur.rowcount
                if n==1:
                    return render_template('deletecart.html',data="The Product Has Been Removed")
                else:
                    return render_template('deletecart.html',data="Error:Please Try Again")
            else:
                render_template(url_for('autherror'))
        else:
            render_template(url_for('autherror'))


@app.route('/buy_now_direct',methods=['GET','POST'])
def buy_now_direct():
    if 'usertype' in session:
        usertype = session['usertype']
        email = session['email']
        name=session['name']
        if usertype == 'user':
            if request.method=='POST':
                id=request.form['A6']
                name_product=request.form['A1']
                company=request.form['A2']
                price=request.form['A3']
                retailer_email=request.form['A5']
                conn = pymysql.connect(
                    user='root',
                    passwd='',
                    port=3306,
                    host='localhost',
                    db='amajon',
                    autocommit=True
                    )
                cur = conn.cursor()
                sql="insert into buyied_products values('"+id+"','"+name_product+"','"+company+"','"+price+"','"+email+"','"+name+"','"+retailer_email+"')"
                cur.execute(sql)
                n=cur.rowcount
                if n==1:
                    return render_template('buynow.html',msg="Congratulations,Your Request Has Been Processed.The Product Would Be Delieverd Within 2-3 Buissness Days")
                else:
                    return render_template('buynow.html',msg="Error:Please Try Again")
        else:
            return render_template(url_for('autherror'))
    else:
        return render_template(url_for('autherror'))


@app.route('/buy_now',methods=['GET','POST'])
def buy_now():
    if 'usertype' in session:
        usertype = session['usertype']
        email = session['email']
        name=session['name']
        if usertype == 'user':
            if request.method=='POST':
                id=request.form['A1']
                name_product=request.form['A2']
                company=request.form['A3']
                price=request.form['A4']
                retailer_email=request.form['A6']
                conn = pymysql.connect(
                    user='root',
                    passwd='',
                    port=3306,
                    host='localhost',
                    db='amajon',
                    autocommit=True
                    )
                cur = conn.cursor()
                sql="insert into buyied_products values('"+id+"','"+name_product+"','"+company+"','"+price+"','"+email+"','"+name+"','"+retailer_email+"')"
                cur.execute(sql)
                n=cur.rowcount
                if n==1:
                    return render_template('buynow.html',msg="Congratulations,Your Request Has Been Processed.The Product Would Be Delieverd Within 2-3 Buissness Days")
                else:
                    return render_template('buynow.html',msg="Error:Please Try Again")
        else:
            return render_template(url_for('autherror'))
    else:
        return render_template(url_for('autherror'))


@app.route('/change_productphoto',methods=['GET','POST'])
def change_productphoto():
    if 'usertype' in session:
        usertype=session['usertype']
        email=session['email']
        if usertype=='seller':
            if request.method=='POST':
                e1=request.form['H1']
                photo=request.form['H2']         #improve the change photo in the show product
                conn = pymysql.connect(
                    user='root',
                    passwd='',
                    port=3306,
                    host='localhost',
                    db='amajon',
                    autocommit=True

                )
                cur = conn.cursor()
                sql="update productdata set photo='"+photo+"' where sellers_email='"+e1+"'"
                cur.execute(sql)
                n=cur.rowcount
                if n>0:
                    os.remove("./static/product_photos/"+photo)
                    return render_template('change_product_photo.html',data="success")
                else:
                    return render_template('change_product_photo.html', data="failure")
            else:
                return render_template('show_product.html')
        else:
            return redirect(url_for('autherror'))
    else:
        return redirect(url_for('autherror'))

@app.route('/revenue_seller')
def revenue_seller():
    if 'usertype' in session:
        usertype=session['usertype']
        email=session['email']
        if usertype=='seller':
            conn = pymysql.connect(
                user='root',
                passwd='',
                port=3306,
                host='localhost',
                db='amajon',
                autocommit=True

            )
            cur = conn.cursor()
            sql="select * from buyied_products where retailers_email='"+email+"'"
            cur.execute(sql)
            n=cur.rowcount
            if n>0:
                result=cur.fetchall()
                return render_template('revenueseller.html',result=result,vgt="Your net revenue Sheet")
            else:
                return render_template('revenueseller.html',vgt="No Product Found")
        else:
            return render_template(url_for('autherror'))
    else:
        return render_template(url_for('autherror'))



if __name__== '__main__':
    app.run(debug=True)