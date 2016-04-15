#-*-coding:utf-8
#从app包中导入在__init__文件中创建的app变量，并调用其run方法来启动服务器。app变量中含有创建的flask实例。
from app import app
app.run(debug=True);