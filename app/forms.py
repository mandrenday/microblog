#-*-coding:utf-8 -*-
#forms.py为表单文件
#在flask-wtf中，表单表示成对象，是Form类的子类。
from flask.ext.wtf import Form
from wtforms import StringField , BooleanField,TextAreaField
from wtforms.validators import DataRequired,Length

class LoginForm(Form):
#其中的stringField定义了一个可以输入的文本框，并赋予文本框中的字段以标志符
#第二个参数用来检查提交的数据是否为空
#第二个则用来生成一个选中按钮，表示是否记住登录情况，默认为不记住
	openid=StringField('openid',validators=[DataRequired()])
	remember_me = BooleanField('remember_me',default=False)

#个人信息编辑	
class EditForm(Form):
	nickname=StringField('nickname',validators=[DataRequired()])
	about_me=TextAreaField('about_me',validators=[Length(min=0,max=140)])

#post编辑
class PostForm(Form):
	post=StringField('post',validators=[DataRequired()])

#搜索post	
class SearchForm(Form):
	search=StringField('search',validators=[DataRequired()])
