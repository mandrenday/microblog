#-*-coding:utf-8 -*-
#forms.pyΪ���ļ�
#��flask-wtf�У�����ʾ�ɶ�����Form������ࡣ
from flask.ext.wtf import Form
from wtforms import StringField , BooleanField,TextAreaField
from wtforms.validators import DataRequired,Length

class LoginForm(Form):
#���е�stringField������һ������������ı��򣬲������ı����е��ֶ��Ա�־��
#�ڶ���������������ύ�������Ƿ�Ϊ��
#�ڶ�������������һ��ѡ�а�ť����ʾ�Ƿ��ס��¼�����Ĭ��Ϊ����ס
	openid=StringField('openid',validators=[DataRequired()])
	remember_me = BooleanField('remember_me',default=False)

#������Ϣ�༭	
class EditForm(Form):
	nickname=StringField('nickname',validators=[DataRequired()])
	about_me=TextAreaField('about_me',validators=[Length(min=0,max=140)])

#post�༭
class PostForm(Form):
	post=StringField('post',validators=[DataRequired()])

#����post	
class SearchForm(Form):
	search=StringField('search',validators=[DataRequired()])
