import itertools
import os
from werkzeug.utils import secure_filename
from flask import Flask, flash, redirect, render_template, request
import flask
from flask_sqlalchemy import SQLAlchemy
import mysql.connector
import pymysql
import time,datetime

# from Paper import main
from call_api import askChatGPT
from diagnosis import diagnosis, suggest
from getGuideline import getExpress,getLogic

app = Flask(__name__,template_folder='templates',static_folder="static") #,static_url_path="uploadFile" 
app.debug=True

app.config['UPLOAD_FOLDER'] = 'program/uploadFile/'
# 获取数据库连接
conn = mysql.connector.connect(
    host='47.120.8.151',
    user='root',
    password='Aly123456',
    port='3306',
    database='medical_treatment',
    charset='utf8'
)

@app.route('/')
def login():  
    return render_template("login.html")

@app.route('/register')
def register(): 
    return render_template("register.html")

@app.route('/logInfo',methods=['GET','POST'])
def logInfo():
    account = flask.request.form['account']
    password = flask.request.form['password']
    try:
        cur = conn.cursor()
        sql = "SELECT username,password FROM user where user.username=%s and user.password=%s " # 不管什么数据类型，一律用%s占位
        cur.execute(sql,(account,password,))  #第二个参数一定要传入元组，哪怕一个参数
        content = cur.fetchall()
        # print(content)
    except (Exception, pymysql.Error) as error :
            conn.rollback()
            print ("Error while fetching data from mysql", error)
    if (content):
        return render_template('index.html')
    else :
        #raise ValueError("用户名或者密码输入错误")
        #flash("用户名或者密码输入错误")
        msg = "用户名或者密码输入错误，请重新输入！"
        return render_template("login.html",msg = msg)


# 注册，判断注册用户名是否已存在和两次密码是否匹配
@app.route('/registInfo',methods=['GET','POST'])
def registInfo():
    username = flask.request.form['username']
    password  = flask.request.form['password']
    deterpassword  = flask.request.form['determine-password']
    # print(password,deterpassword)
    if(password != deterpassword):
        return render_template('register.html', errmsg = "两次输入密码不匹配！")
    try:
        cur = conn.cursor()
        sql = "SELECT username FROM user where user.username=%s"
        cur.execute(sql,(username,)) 
        content = cur.fetchall()
        #print(content)
    except (Exception, pymysql.Error) as error :
            conn.rollback()
            print ("Error while fetching data from mysql", error)
    if (content):
        return render_template('register.html', errmsg = "账号已存在！")

    try:
        cur = conn.cursor()
        sql = "INSERT INTO user (username,password) VALUES (%s,%s)" 
        cur.execute(sql,(username,password,)) 
        conn.commit()  # 提交数据，不然数据库中没有记录
        content = cur.fetchall()
        # print(content)
    except (Exception, pymysql.Error) as error :
            conn.rollback()
            print ("Error while fetching data from mysql", error)
    return render_template('register.html', sucmsg = "注册成功，请登陆！")


# 从数据库读取医疗指南信息打印到前端
@app.route('/medical_guidelines',methods=['GET','POST'])
def medical_guidelines():
    try:
        cur = conn.cursor()
        sql = "SELECT gname,gtype,gtime,path FROM guideline"
        cur.execute(sql,()) 
        res = cur.fetchall()
        # print(res)
    except (Exception, pymysql.Error) as error :
            conn.rollback()
            print ("Error while fetching data from mysql", error)
    return res

# 选择医疗指南进行问答
@app.route('/questionSelect',methods=['GET','POST'])
def questionSelect():
    try:
        cur = conn.cursor()
        sql = "SELECT gname FROM guideline"
        cur.execute(sql,()) 
        res = cur.fetchall()
        #print(res)
    except (Exception, pymysql.Error) as error :
            conn.rollback()
            print ("Error while fetching data from mysql", error)
    return res

# 读取病患信息
@app.route('/patient_information',methods=['GET','POST'])
def patient_information():
    try:
        cur = conn.cursor()
        sql = "SELECT pname,page,ptype,ptime FROM patient"
        cur.execute(sql,()) 
        res = cur.fetchall()
        # print(res)
    except (Exception, pymysql.Error) as error :
            conn.rollback()
            print ("Error while fetching data from mysql", error)
    return res

# 根据医疗指南回答问题
@app.route('/Quearea',methods=['GET','POST'])
def Quearea():
    content = request.args.get('areadata')  # Get方法 获取文本域内容
    # main(content)
    content = askChatGPT(content)
    return content


@app.route('/diagnosisInfo',methods=['GET','POST'])
def diagnosisInfo():
    name = request.args.get('name')
    age = request.args.get('age')
    dias = request.args.get('dias')
    ptype = "未确诊" 
    # 保存患者信息
    try:
        cur = conn.cursor()
        sql = "INSERT INTO patient (pname,page,ptype,ptime,precord) VALUES (%s,%s,%s,%s,%s)"
        cur.execute(sql,(name,age,ptype,datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),dias,)) 
        conn.commit()
        res = cur.fetchall()
        print(res)
    except (Exception, pymysql.Error) as error :
            conn.rollback()
            print ("Error while fetching data from mysql", error)
    content = "患者年龄:" + age + ", 症状描述:" + dias
    answer = diagnosis(content)
    print(content)
    return answer

@app.route('/opinionInfo',methods=['GET','POST'])
def opinionInfo():
    name = request.args.get('name')
    age = request.args.get('age')
    dias = request.args.get('dias')
    content = "患者年龄:" + age + ", 症状描述:" + dias
    answer = suggest(content)
    #print(content)
    return answer

# 上传文件
@app.route(('/uploadfile'),methods=['GET','POST'])
def upload():
    # data = request.form
    file = request.files['file']
    # print(file)
    filename = secure_filename(file.filename)
    ltime = time.localtime()
    paths = str(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    try:
        cur = conn.cursor()
        # sql = "select * from guideline where gname = %s"
        # cur.execute(sql,(filename,))
        # if(cur.fetchall):
        #     return '已经存在该指南'
        sql = "insert into guideline(gname,gtime,path) values (%s,%s,%s)"
        cur.execute(sql,(filename,datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),paths)) 
        res = cur.fetchall()
        conn.commit()
        #print(res)
    except (Exception, pymysql.Error) as error :
            conn.rollback()
            print ("Error while fetching data from mysql", error)
    
    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    #print(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    
   # mes = '12345' #
    print(paths)
    mes = getLogic(paths)
    # 返回文件路径
    return  {'path':paths, 'mes':mes}

# 自由问答 
@app.route('/freeASK',methods=['GET','POST'])
def freeASK():
    ask = request.args.get('ask')
    #print(ask)
    answer = askChatGPT(ask)
    return answer


# 以下均by wang
# 从数据库读取诊断标准打印到前端
@app.route('/diagnosisStandard', methods=['GET', 'POST'])
def diagnosisStandard():
    try:
        cur = conn.cursor()
        sql = "SELECT diagnosisStandard FROM knowledge_base where id = 1"
        cur.execute(sql, ())
        res = cur.fetchall()
    except (Exception, pymysql.Error) as error:
        conn.rollback()
        print("Error while fetching data from mysql", error)
    return list(res)

# 从数据库读取诊疗流程打印到前端
@app.route('/diagnosisProcess', methods=['GET', 'POST'])
def diagnosisProcess():
    try:
        cur = conn.cursor()
        sql = "SELECT diagnosisProcess FROM knowledge_base where id = 1"
        cur.execute(sql, ())
        res = cur.fetchall()
    except (Exception, pymysql.Error) as error:
        conn.rollback()
        print("Error while fetching data from mysql", error)
    return list(res)

# 从数据库读取辅助检查打印到前端

@app.route('/examination', methods=['GET', 'POST'])
def examination():
    try:
        cur = conn.cursor()
        sql = "SELECT examination FROM knowledge_base where id = 1"
        cur.execute(sql, ())
        res = cur.fetchall()
    except (Exception, pymysql.Error) as error:
        conn.rollback()
        print("Error while fetching data from mysql", error)
    return list(res)

# 从数据库读取病历信息打印到前端


@app.route('/cases', methods=['GET', 'POST'])
def cases():
    try:
        cur = conn.cursor()
        sql = "SELECT cname, ctype, cage, csex, ctime FROM `case`"
        cur.execute(sql, ())
        #print(sql)
        res = cur.fetchall()
        #print(res)
    except (Exception, pymysql.Error) as error:
        conn.rollback()
        print("Error while fetching data from mysql", error)
    return list(res)

 # 关闭数据库连接
 #conn.close()

if __name__ == '__main__':
    app.run()