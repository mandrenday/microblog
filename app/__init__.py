#-*-coding:utf-8 -*-
#是app包的初始化文件
from flask import Flask
import os
from flask.ext.login import LoginManager
from flask.ext.openid import OpenID
import pymysql
from flask.ext.mail import Mail
from config import basedir,ADMINS,MAIL_SERVER,MAIL_PORT,MAIL_USERNAME,MAIL_PASSWORD


db=pymysql.connect(host='localhost',user='root',passwd='qrupfkcm753',db='microblog',charset='utf8');
cur=db.cursor();

app=Flask(__name__)
#加载配置文件
app.config.from_object('config')
lm=LoginManager()
lm.init_app(app)
lm.login_view='login'
#Flask-OpenID扩展需要一个存储文件的临时文件夹的路径
oid=OpenID(app,os.path.join(basedir,'tmp'))
mail=Mail(app);


#若程序不是以调试的方式打开，就发送错误到邮件。是否以调试程序打开得看run.py中的设置
if not app.debug:
	import logging
	from logging.handlers import SMTPHandler
	credentials = None
	if MAIL_USERNAME or MAIL_PASSWORD:
		credentials=(MAIL_USERNAME,MAIL_PASSWORD)
	mail_handler=SMTPHandler((MAIL_SERVER,MAIL_PORT),'no_reply@' + MAIL_SERVER,ADMINS,'microblog failure',credentials)
	mail_handler.setLevel(logging.ERROR)
	app.logger.addHandler(mail_handler)
#若程序不是以调试方式打开，就在日志文件中记录信息，记录信息的类型通过设置日志的级别来确定

if not app.debug:
	import logging
	from logging.handlers import RotatingFileHandler
	file_handler = RotatingFileHandler('/tmp/microblg.log','a',10*1024*1024,50)
	#上面的语句是将日志文件的大小限制为10M，且只保留最后50个日志文件。
	file_handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
	#上面的语句定制信息显示的格式，保留时间戳，日志记录以及消息的起源，日志消息和堆栈跟踪的文件和行号
	app.logger.setLevel(logging.INFO)
	file_handler.setLevel(logging.INFO)
	app.logger.addHandler(file_handler)
	app.logger.info('microblog startup')
	
	
	

#导入视图与模型
from app import views,models
