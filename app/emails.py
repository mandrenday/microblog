from flask.ext.mail import Message
from flask import render_template
from app import mail,app
from config import ADMINS
from .decorators import async

def send_email(subject,sender,recipients,text_body,html_body):
	msg = Message(subject, sender = sender, recipients = recipients)
	msg.body = text_body
	msg.html = html_body
	send_async_email(app,msg);
	
#在follower_email.txt中重定向页面使用到_external是由于重定向只是生成
#/index。但是在邮件中应该有加上前面的域名，而_external则是用来完成这一个
	
def follower_notification(followed,follower):
	send_email("[microblog] %s is now following you!" % follower.nickname,ADMINS[0],[followed.email],\
		render_template("follower_email.txt",user = followed, follower = follower),render_template("follower_email.html",user = followed, follower = follower))

@async
def send_async_email(app,msg):
	with app.app_context():
		mail.send(msg);