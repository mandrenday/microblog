#!flask/bin/python
import os
import unittest

from config import basedir
from app import db,app,cur
from app.models import User,Post
from datetime import *

class TestCase(unittest.TestCase):
	def setUp(self):
		app.config['TESTING']=True;
		app.config['WTF_CSRF_ENABLED']=False
		self.app=app.test_client()
	def tearDown(self):
		pass;
	def test_follow(self):
		u1 = User(nickname = 'john', email = 'john@example.com')
		u2=User(nickname = 'susan', email = 'susan@example.com')
		u3=User(nickname = 'mary', email = 'mary@example.com')
		u4=User(nickname = 'peter', email = 'peter@example.com')
		utcnow = datetime.utcnow()
		p1 = Post(body = "post from john", user_id = u1.id, timestamp = utcnow + timedelta(seconds = 1))
		p2 = Post(body = "post from susan", user_id = u2.id, timestamp = utcnow + timedelta(seconds = 2))
		p3 = Post(body = "post from mary", user_id = u3.id, timestamp = utcnow + timedelta(seconds = 3))
		p4 = Post(body = "post from david", user_id = u4.id, timestamp = utcnow + timedelta(seconds = 4))
		u1.follow(u1);
		u1.follow(u2);
		u1.follow(u4);
		u2.follow(u2);
		u2.follow(u3);
		u3.follow(u3);
		u3.follow(u4);
		u4.follow(u4);
		f1=u1.followed_posts();
		f2=u2.followed_posts();
		f3=u3.followed_posts();
		f4=u4.followed_posts();
		assert(len(f1)==3);
		assert(len(f2)==2);
		assert(len(f3)==2);
		assert(len(f4)==1)
if __name__=='__main__':
	unittest.main();