import pymysql

def gethost():
    return "localhost"
def getuser():
    return "root"
def getpasswd():
    return ""
def getdb():
    return "amajon"
def getport():
    return 3306

def check_photo_admin(email):
    conn = pymysql.connect(host=gethost(),
                           port=getport(),
                           user=getuser(),
                           passwd=getpasswd(),
                           db=getdb())
    cur=conn.cursor()
    sql="SELECT * FROM photodata_admin where email='"+email+"'"
    cur.execute(sql)
    n=cur.rowcount
    photo="no"
    if n>0:
        row=cur.fetchone()
        photo=row[1]
    return photo

def check_photo_seller(email):
    conn = pymysql.connect(host=gethost(),
                           port=getport(),
                           user=getuser(),
                           passwd=getpasswd(),
                           db=getdb())
    cur=conn.cursor()
    sql="SELECT * FROM photodata_seller where email='"+email+"'"
    cur.execute(sql)
    n=cur.rowcount
    photo="no"
    if n>0:
        row=cur.fetchone()
        photo=row[1]
    return photo

def check_photo_user(email):
    conn = pymysql.connect(host=gethost(),
                           port=getport(),
                           user=getuser(),
                           passwd=getpasswd(),
                           db=getdb())
    cur=conn.cursor()
    sql="SELECT * FROM photodata_user where email='"+email+"'"
    cur.execute(sql)
    n=cur.rowcount
    photo="no"
    if n>0:
        row=cur.fetchone()
        photo=row[1]
    return photo


def get_admin_name(email):
    conn = pymysql.connect(host=gethost(),
                           port=getport(),
                           user=getuser(),
                           passwd=getpasswd(),
                           db=getdb())
    cur=conn.cursor()
    sql="SELECT * FROM admindata where email='"+email+"'"
    cur.execute(sql)
    n=cur.rowcount
    name="no"
    if n>0:
        row = cur.fetchone()
        name = row[0]
    return name

def get_seller_name(email):
    conn = pymysql.connect(host=gethost(),
                           port=getport(),
                           user=getuser(),
                           passwd=getpasswd(),
                           db=getdb())
    cur=conn.cursor()
    sql="SELECT * FROM sellerdata where email='"+email+"'"
    cur.execute(sql)
    n=cur.rowcount
    name="no"
    if n>0:
        row = cur.fetchone()
        name = row[0]
    return name

def get_user_name(email):
    conn = pymysql.connect(host=gethost(),
                           port=getport(),
                           user=getuser(),
                           passwd=getpasswd(),
                           db=getdb())
    cur=conn.cursor()
    sql="SELECT * FROM userdata where email='"+email+"'"
    cur.execute(sql)
    n=cur.rowcount
    name="no"
    if n>0:
        row = cur.fetchone()
        name = row[0]
    return name