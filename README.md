#首页扩展与更新说明文档

一下目录基于项目目录。

1. 在./index/templates/herald_index.html模板中的**正确位置**上{% include %}相关的模板，主要是注意模板顺序。
	
	模板要求：tab???

2. 在./index/templates/tab.html模板中添加响应的tab，注意顺序。
3. 在./index/views.py的index视图函数中：对dics字典添加在上面添加的模板中需要的映射字典，调用dics.update(your_dic)来扩充原有字典dics.
4. 下面进行数据库配置，这里涉及django的多数据使用。
	* 在./herald_index/setting.py的DATABASES中添加数据库。
	* 配置数据库路由，并安装在setting.py的DATABASE_ROUTERS中添加。
	* 注意：如果使用的是django的数据库引擎，那么在自定义的model中要注意数据库的同步、读写，原则上只有与各个模块相关的数据库只进行读操作。建议设置好app_label和自动路由。
	* 从各个模块需要的数据由各个模块开发人员提供数据库view.
	

未完待续。。。
