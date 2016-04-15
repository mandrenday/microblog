from app import db,cur
from hashlib import md5
class  User(object):
	def __init__(self,nickname,email):
		self.nickname=nickname;
		self.email=email;
		if(cur.execute('select * from user where nickname="'+self.nickname+'"')==0):
			cur.execute('insert into user(nickname,email) values("'+self.nickname+'","'+self.email+'")');
			db.commit();
		cur.execute('select * from user where nickname="'+self.nickname+'"')
		for a in cur:
			self.id=a[0];
			self.about_me=a[3];
			self.last_seen=a[4];
			break;
	
#下面的这几个函数都是在使用Flask_Login扩展时要求User所实现的一些特定的方法
#但对于如何实现没有什么要求
#使用Gravatar服务来提供用户上传的头像，若是没有上传，则会显示一个神秘人
	
	def is_authenticated(self):
		return True;
	def is_active(self):
		return True;
	def is_anonymous(self):
		return False;
	def get_id(self):
		return str(self.id);
	def avatar(self,size):
		return 'http://www.gravatar.com/avatar/'+ md5(self.email.encode("utf8")).hexdigest() + '?d=mm&s=' + str(size);
	def follow(self,user):
		if not self.is_following(user):
			cur.execute('insert followers (follower_id,followed_id) values (%d,%d)'%(self.id,user.id));
			db.commit();
			return self;
		else: return 0;
	def unfollow(self,user):
		if self.is_following(user):
			cur.execute('delete from followers where follower_id=%d and followed_id=%d'%(self.id,user.id));
			db.commit();
			return self;
		else: return 0; 
	def is_following(self,user):
		a=cur.execute('select * from followers where follower_id=%d and followed_id=%d'%(self.id,user.id));
		return a;
#实现分页返回post列表，且返回的列表的第一个元素若为1，则表示还有下一页，若为0，则没有下一页
	def followed_posts(self,j):
		cur.execute('select count(*) from followers,post,user where followers.followed_id=post.user_id and followers.followed_id=user.id and followers.follower_id=%d '%(self.id));
		sum=0;
		for i in cur:
			sum=i[0];
			break;
		if(sum > 5*j+5):
			cur.execute('select body,nickname from followers,post,user where followers.followed_id=post.user_id and followers.followed_id=user.id and followers.follower_id=%d order by post.timestamp  limit %d,5'%(self.id,5*int(j)));
			b=[];
			b.append(1);
			for i in cur:
				a={}
				a['nickname']=i[1]
				a['body']=i[0]
				b.append(a)
			return b;
		if (sum <= 5*j+5):
			cur.execute('select body,nickname from followers,post,user where followers.followed_id=post.user_id and followers.followed_id=user.id and followers.follower_id=%d order by post.timestamp limit %d,%d '%(self.id,5*int(j),sum-5*int(j)));
			b=[];
			b.append(0);
			for i in cur:
				a={}
				a['nickname']=i[1]
				a['body']=i[0]
				b.append(a)
			return b;
		
		
		
#返回的结果为一个列表，第一个元素为列表的数目，因为在html中无法使用Python自带的获取列表长度的函数，所以直接返回列表的数目		
	def followers(self):
		a=cur.execute('select followed_id from followers where follower_id=%d'%(self.id));
		b=[];
		for i in cur:
			b.append(i[0]);
		c=len(b);
		b.insert(0,c);
		return b;
				
			
	
		
		
		
	
		
	
	
class Post(object):
	def __init__(self,body,timestamp,user_id):
		self.body=body;
		self.timestamp=str(timestamp);
		self.user_id=user_id;
		cur.execute("insert into post(body,timestamp,user_id) values ('"+self.body+"','"+self.timestamp+"',%d)"%(self.user_id));
		db.commit();
	