#-*-coding:utf-8 -*-
#��app���ĳ�ʼ���ļ�
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
#���������ļ�
app.config.from_object('config')
lm=LoginManager()
lm.init_app(app)
lm.login_view='login'
#Flask-OpenID��չ��Ҫһ���洢�ļ�����ʱ�ļ��е�·��
oid=OpenID(app,os.path.join(basedir,'tmp'))
mail=Mail(app);


#���������Ե��Եķ�ʽ�򿪣��ͷ��ʹ����ʼ����Ƿ��Ե��Գ���򿪵ÿ�run.py�е�����
if not app.debug:
	import logging
	from logging.handlers import SMTPHandler
	credentials = None
	if MAIL_USERNAME or MAIL_PASSWORD:
		credentials=(MAIL_USERNAME,MAIL_PASSWORD)
	mail_handler=SMTPHandler((MAIL_SERVER,MAIL_PORT),'no_reply@' + MAIL_SERVER,ADMINS,'microblog failure',credentials)
	mail_handler.setLevel(logging.ERROR)
	app.logger.addHandler(mail_handler)
#���������Ե��Է�ʽ�򿪣�������־�ļ��м�¼��Ϣ����¼��Ϣ������ͨ��������־�ļ�����ȷ��

if not app.debug:
	import logging
	from logging.handlers import RotatingFileHandler
	file_handler = RotatingFileHandler('/tmp/microblg.log','a',10*1024*1024,50)
	#���������ǽ���־�ļ��Ĵ�С����Ϊ10M����ֻ�������50����־�ļ���
	file_handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
	#�������䶨����Ϣ��ʾ�ĸ�ʽ������ʱ�������־��¼�Լ���Ϣ����Դ����־��Ϣ�Ͷ�ջ���ٵ��ļ����к�
	app.logger.setLevel(logging.INFO)
	file_handler.setLevel(logging.INFO)
	app.logger.addHandler(file_handler)
	app.logger.info('microblog startup')
	
	
	

#������ͼ��ģ��
from app import views,models
