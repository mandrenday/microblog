#-*-coding:utf-8 -*-
#config文件为配置文件，创建配置文件一边flask扩展所需要的配置容易被编辑
#配置文件在init文件中被使用
import os
basedir = os.path.abspath(os.path.dirname(__file__))
#CSRF_ENABLED配置是用来激活跨站点请求伪造保护，激活该配置使程序更安全。
CSRF_ENABLED = True
#SECRET_KEY用来建立一个加密的令牌，用于验证表单，只有当CSRF激活时才需要
SECRET_KEY = 'qrupfkcm753'


#下面的几行用来配置邮件服务器以及管理员邮箱地址
MAIL_SERVER = 'smtp.googlemail.com'
MAIL_PORT = 465
MAIL_USE_TLS = False
MAIL_USE_SSL = True
MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')

ADMINS = ['qiumk04@gmail.com']

OPENID_PROVIDERS=[
	{ 'name': 'Google', 'url': 'https://www.google.com/accounts/o8/id' },
    { 'name': 'Yahoo', 'url': 'https://me.yahoo.com' },
    { 'name': 'AOL', 'url': 'http://openid.aol.com/<username>' },
    { 'name': 'Flickr', 'url': 'http://www.flickr.com/<username>' },
    { 'name': 'MyOpenID', 'url': 'https://www.myopenid.com' }
	]

MAX_SEARCH_RESULTS=5