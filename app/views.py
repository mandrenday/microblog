#-*-coding:utf-8 -*-
#定义视图，视图用来响应来自网页的请求，每一个视图是一个函数
from app import app,db,lm,oid,cur
from flask import render_template,flash,redirect,session,url_for,request,g
from .forms import LoginForm,EditForm,PostForm,SearchForm
from .models import User,Post
from flask.ext.login import login_user,logout_user,current_user,login_required
from datetime import datetime
from config import MAX_SEARCH_RESULTS
from .emails import follower_notification


#route修饰器创建了从网址/以及/index到这个函数的映射，所以若是登录
#http://localhost:5000/或是http://localhost:5000/index就会映射到该函数
#其中render_template函数中第一个参数代表返回给浏览器的页面，后面的几个
#则是传递给页面的参数，这样可以动态的更改页面的内容。

#login_required确保这一页只被已经登录的用户看到

@app.route('/',methods=['GET','POST'])
@app.route('/index',methods=['GET','POST'])
@app.route('/index/<int:page>',methods=['GET','POST'])
@login_required
def index(page=0):
	form=PostForm();
	if form.validate_on_submit():
		post=Post(body=form.post.data,timestamp=datetime.utcnow(),user_id=g.user.id);
		flash('Your post is now live!');
		return redirect(url_for('index'))
#if中的最后一个语句之所以是重定向到该视图函数，是为了避免当用户不小心
#按到浏览器的刷新键的时候，浏览器将会发送上一次的post请求（如果之前有提交的话）
#这样会导致表单数据被重复提交，有了重定向，使得表单提交后发送的是get请求
	posts=g.user.followed_posts(page);
#返回的结果中第一个表示的是是否后面还有未显示的内容，1表示还有，0表示没有
	hasNext=posts[0];
	del posts[0];
	return render_template("index.html",
                          title="Home",
                          form=form,
                          posts=posts,
						  page_num=page,
						  hasNext=hasNext)

#用于从数据库加载用户，这个函数会被Flask_Login使用	
#且注意在Flask_Login中的用户id都是Unicode字符串，所以如果
#在数据库中id定义为整数，则应该进行类型转换				  
@lm.user_loader
def load_user(id):
	id1=int(id)
	cur.execute("select * from user where id=%d"%id1);
	for i in cur:
		user=User(nickname=i[1],email=i[2]);
		return user

#下面app.route中的method参数用来告诉视图函数接受GET和POST请求，若是
#不带参数，默认只接受GET请求。

#validate_on_submit在表单提交请求中被调用，会收集所有的数据，并对字段进行验证
#如果所有的事情都通过，就会返回True，表示数据合法。

#redirect表示告诉网页浏览器引导到一个不同的页面，该页面的查找是看
#app.route中的字符。

#oid.loginhandler告诉Flask_OpenID这是登录视图函数。

#首先检查g.user是为了若是已经登陆的用户，则不用二次登录
#Flask中的g全局变量是一个在请求生命期间用来存储和共享数据。

#flask.session也是用来存储数据，但却是比flask.g更加高级
#一旦数据存储在会话对象中，在来自统一客户端的现在和以后的请求都是可以用的

#oid.try_login是触发用户使用Flask_OpenID认证，参数分别为用户提供的
#openid以及希望得到的数据列表。若是认证
#成功则会调用一个注册了oid.after_login装饰器的函数

	
@app.route('/login',methods=['GET','POST'])
@oid.loginhandler
def login():
	if g.user is not None and g.user.is_authenticated():
		return redirect(url_for('index'));
	form=LoginForm()
	if form.validate_on_submit():
		session['remember_me']=form.remember_me.data;
		return oid.try_login(form.openid.data,ask_for=['nickname','email'])
	return render_template('login.html',title='Sign In',form=form,providers=app.config['OPENID_PROVIDERS'])
	
#resp参数包含从openID提供商返回的我们所请求的数据
#login_user用来注册有效的登录。
#最后一个redirect则是如果next页没有提供，就重定向到首页，否则定向到next页
#为了让函数内的生效，需要让Flask_login知道那个视图允许用户登录
#在init.py中使用lm.login_view = 'login'进行配置
	
@oid.after_login
def after_login(resp):
	if resp.email is None or resp.email=="":
		flash('Invalid login.Please try again.')
		return redirect(url_for('login'))
	mail=resp.email
	a=cur.execute('select * from user where email = "'+mail+'"');
	if a==0:
		nickname=resp.nickname
		if nickname is None or nickname=="":
			nickname=resp.email.split('@')[0]
		user=User(nickname=nickname,email=resp.email);
	else: 
		for each in cur:
			b=list(each);
			break;
		user=User(nickname=b[1],email=b[2]);
	remember_me=False
	user.follow(user);
	if 'remember_me' in session:
		remember_me=session['remember_me']
		session.pop('remember_me',None)
	login_user(user,remember=remember_me)
	return redirect( request.args.get('next') or url_for('index'))

#任何使用了before_request装饰器的函数都会在接受请求前运行。
#此处用来验证用户是否已经登录

#因为搜索表单是所有页面共有的，所以在before_request中创建并保存在全局变量g中。	
@app.before_request
def before_request():
	g.user=current_user
	if g.user.is_authenticated():
		a=str(datetime.utcnow());
		cur.execute('update user set last_seen = "'+a+'" where  id= %d'%(g.user.id));
		db.commit();
		g.search_form=SearchForm();
		
#用于用户的登出
@app.route('/logout')
def logout():
	logout_user();
	return redirect(url_for('index'))
	
#当客户端以URL/user/name请求的时候，视图函数会收到一个nicknam=‘name’
#参数而进行调用。
@app.route('/user/<nickname>')
@app.route('/user/<nickname>/<int:page>')
@login_required
def user(nickname,page=0):
	a=cur.execute('select * from user where nickname="'+nickname+'"');
	if a==0:
		flash('User '+nickname+' not found.')
		return redirect(url_for('index'))
	for i in cur:
		user=User(nickname=i[1],email=i[2]);
		break;
	posts=user.followed_posts(page);
#返回的结果中第一个表示的是是否后面还有未显示的内容，1表示还有，0表示没有
	hasNext=posts[0];
	del posts[0];
	return render_template('user.html',user=user,posts=posts,hasNext=hasNext,page_num=page);
	
@app.route('/edit',methods=['GET','POST'])
@login_required
def edit():
	form=EditForm();
	if form.validate_on_submit():
		a=cur.execute('select * from user where nickname="'+form.nickname.data+'"')
		if(a==0 or form.nickname.data==g.user.nickname):
			cur.execute('update user set nickname = "'+form.nickname.data+'",about_me="'+form.about_me.data+'" where  id= %d'%(g.user.id));
			db.commit();
			flash('Your changes have been saved.')
			return redirect(url_for('user',nickname=g.user.nickname))
		else:
			flash('The name you set has been used by others, please choose another name');
			return redirect(url_for('edit'));
	else:
		form.nickname.data=g.user.nickname
		form.about_me.data=g.user.about_me
	return render_template('edit.html',form=form);


#定义关注以及取消关注用户的视图函数	
@app.route('/follow/<nickname>')
@login_required
def follow(nickname):
	a=cur.execute('select * from user where nickname="'+nickname+'"');
	if a==0:
		flash('User %s not found.'% nickname);
		return redirect(url_for('index'));
	for i in cur:
		user = User(nickname=i[1],email=i[2]);
		break;
	if user==g.user:
		flash('You have already follow yourself!');
		return redirect(url_for('user',nickname=nickname));
	u=g.user.follow(user);
	if u == 0:
		flash("you have already follow"+nickname+"!");
		return redirect(url_for('user',nickname=nickname))
	flash('You are now following '+ nickname + '!')
	follower_notification(user, g.user)
	return redirect(url_for('user',nickname=nickname));

	@app.route('/unfollow/<nickname>')
	@login_required
	def unfollow(nickname):
		a=cur.execute('select * from user where nickname="'+nickname+'"');
	if a==0:
		flash('User %s not found.'% nickname);
	for i in cur:
		user = User(nickname=i[1],email=i[2]);
		break;
	if user==g.user:
		flash("You can/'t unfollow yourself!");
		return redirect(url_for('user',nickname=nickname));
	u=g.user.unfollow(user);
	if u == 0:
		flash('You should not unfollow a people that you did not follow');
		return redirect(url_for('user',nickname=nickname));
	flash('You have unfollow '+ nickname +'.');
	return redirect(url_for('user',nickname=nickname));
	

	
#用于定制错误页，下面定制HTTP 404 和500错误页

@app.errorhandler(404)
def internal_error(error):
	return render_template('404.html'),404
	
@app.errorhandler(500)
def internal_error(error):
	db.rollback()
	return render_template('500.html'),500
	
#搜索视图函数
#搜索工作不在这里做，而是重定向到另外一个函数是因为担心用户无意中触发了刷新
#这样会导致表单数据被重复提交
@app.route('/search',methods=['POST'])
@login_required
def search():
	if not g.search_form.validate_on_submit():
		return redirect(url_for('index'))
	return redirect(url_for('search_result',query=g.search_form.search.data))
@app.route('/search_results/<query>')
@login_required
def search_result(query):
	query1='%'+query+'%'
	cur.execute('select body,nickname from followers,post,user where followers.followed_id=post.user_id and followers.followed_id=user.id and post.body like "'+query1+'" and followers.follower_id=%d  order by post.timestamp limit %d'%(g.user.id,MAX_SEARCH_RESULTS));
	a=[];
	for i in cur:
		b={};
		b['body']=i[0];
		b['nickname']=i[1];
		a.append(b);
	return render_template('search_result.html',query=query,results=a);

	
	
	


	
	
	
	
	
	
	