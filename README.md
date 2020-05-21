# flask-blog

博客整体采用flask框架，mysql数据库，进行上线开发。教程会在后面陆续更新
目前已经支持的功能：
1. 个人账户的注册、激活与登录
2. markdown的博文编辑功能及图片上传功能
3. 博文详情页页面的html解析及代码高亮等
4. 文章分页以及分类与分类展示
5. 全局搜索功能

使用：

#### １、建立mysql数据库，我的库名为(alone_blog)，或者改为你们自己的库，并在项目目录下的App/config.py里面进行更改。

#### 2、删除migrations文件，然后依次执行

- python3 manage.py db init
- python3 manage.py db migrate
- python3 manage.py db upgrade

#### 3、执行命令行进行启动

```python
python3 manage.py runserver
```

这个时候打开你的本地浏览器，输入 http://127.0.0.1:5000 就可以看到博客页面啦