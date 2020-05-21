from flask import Blueprint, render_template, flash, redirect, url_for, current_app
from sqlalchemy import or_

from App.forms import SendPosts, Comment, Catgs  # 导入发表博客与发表评论的表单类
from App.models import Posts,Categorys,User # 导入博客模型类和标签模型类
from flask_login import current_user, login_required

from datetime import datetime
from flask import jsonify, request
from App.extensions import qiniu_store, csrf
import os, base64
from App.extensions import file
from PIL import Image

posts = Blueprint('posts', __name__)


# 使用uuid扩展库生成唯一的名称
def random_filename(suffix):
    import uuid
    u = uuid.uuid4()
    return str(u) + '.' + suffix


# 图片缩放处理
def img_zoom(path, width=1000, height=250):
    # 打开文件
    img = Image.open(path)
    # 重新设计尺寸
    # img.thumbnail((width, height))
    # 保存缩放后的图片 保留原图片
    # 保存缩放
    img.save(path)


@posts.route('/send_posts/', methods=['GET', 'POST'])
def send_posts():
    form = SendPosts()
    ctgs = Categorys.query.all()
    # 判断登录后在进行发表
    if not current_user.is_authenticated:
        flash('您还没有登录  请登录后再发表')
    if current_user.id==1:
        if form.validate_on_submit():
            # md格式
            article = request.form['article']
            ctgs = request.form['ctgs']
            tags = Categorys.query.filter_by(categorys=ctgs).first()
            # 图片上传
            img = request.files.get('img')  # 获取上传对象
            ex = os.path.splitext(img.filename)[1]
            filename = datetime.now().strftime('%Y%m%d%H%M%S') + ex
            file = img.stream.read()
            qiniu_store.save(file, filename)
            post = Posts(title=form.title.data, user=current_user, article=article, img=qiniu_store.url(filename),tags=[tags])
            post.save()
            flash('博客发表成功')
            return redirect(url_for('main.index'))
    else:
        flash('您没有发表博客的权限！')
        return redirect(url_for('main.index'))
    return render_template('posts/send_posts.html', form=form, ctgs=ctgs)


# 增加分类
@posts.route('/add_catgs/', methods=['GET', 'POST'])
def add_catgs():
    form = Catgs()
    ctgs = Categorys.query.all()
    if not current_user.is_authenticated:
        flash('您还没有登录  请登录后再操作')
    elif form.validate_on_submit():
        catgs = Categorys(categorys=form.categorys.data)
        catgs.save()
        print(form.categorys.data)
        flash('分类添加成功')
        return redirect(url_for('posts.send_posts'))
    return render_template('posts/add_categorys.html', form=form, ctgs=ctgs)


# 删除分类
@posts.route('/delete_catgs/', methods=['GET', 'POST'])
def delete_catgs():
    ctgs = Categorys.query.all()
    form = Catgs()
    if not current_user.is_authenticated:
        flash('您还没有登录  请登录后再操作')
    elif form.validate_on_submit():
        cs = request.form['ctgs']
        d = Categorys.query.filter_by(categorys=cs)[0]
        d.delete()
        flash('分类删除成功')
        return redirect(url_for('posts.send_posts'))
    return render_template('posts/delete_categorys.html', form=form, ctgs=ctgs)


# 搜索
@posts.route('/search/', methods=['GET', 'POST'])
@csrf.exempt
def search():
    try:
        page = int(request.args.get('page'))
    except:
        page = 1
    # 获取搜索的关键字
    if request.method == 'POST':
        keyword = request.form.get('keyword', '')
    else:
        keyword = request.args.get('keyword', '')
    # 查询pid为0（是博客内容，不为0则是评论或回复内容），statue为0（所有人可见），按照时间降序显示
    # 搜索功能，搜索内容为：标题或正文
    pagination = Posts.query.filter(or_(Posts.title.contains(keyword), Posts.article.contains(keyword)), Posts.pid == 0,
                                    Posts.state == 0) \
        .order_by(Posts.timestamp.desc()) \
        .paginate(page, current_app.config['PAGE_NUM'], False)  # False 为不抛出异常
    data = pagination.items  # 获取page页面的数据
    # 将文章(pid=0)对应的的id查询出来，
    art = Posts.query.filter(Posts.pid==0).count()
    # 按照访问量排行降序查询，拿出前五
    visit = Posts.query.filter(Posts.pid == 0, Posts.state == 0).order_by(-Posts.visit)[:5]
    # 拿到文章对象，进行遍历，然后将访问量放进数组，进行求和
    article_list = Posts.query.filter(Posts.pid==0)
    list = []
    for i in article_list:
        list.append(i.visit)
    v=sum(list)

    cs = Categorys.query.all()
    comments_five = Posts.query.filter(Posts.pid!=0)[0:5]
    return render_template('posts/search_detail.html', pagination=pagination, posts=data, keyword=keyword,art = art, visit=visit, v=v, ctgs=cs,comments_five=comments_five)


# 博客分类
@posts.route('posts_ctgs',methods=['GET','POST'])
def posts_ctgs():
    try:
        page = int(request.args.get('page'))
    except:
        page = 1
    cid = request.args.get('pid')
    global pagination,data
    posts = Categorys.query.get(cid)
    for i in posts.posts:
        pagination = Posts.query.filter(Posts.title==i.title).order_by(Posts.timestamp.desc()).paginate(page, current_app.config['PAGE_NUM'], False)  # False 为不抛出异常
        data = pagination.items  # 获取page页面的数据
    category = Categorys.query.get(cid)
    # 将文章(pid=0)对应的的id查询出来，
    art = Posts.query.filter(Posts.pid==0).count()
    # 按照访问量排行降序查询，拿出前五
    visit = Posts.query.filter(Posts.pid == 0, Posts.state == 0).order_by(-Posts.visit)[:5]
    # 拿到文章对象，进行遍历，然后将访问量放进数组，进行求和
    article_list = Posts.query.filter(Posts.pid==0)
    list = []
    for i in article_list:
        list.append(i.visit)
    v=sum(list)

    cs = Categorys.query.all()
    comments_five = Posts.query.filter(Posts.pid!=0)[0:5]

    return render_template('posts/posts_ctgs.html',pagination=pagination,posts=data,category=category,art = art, visit=visit, v=v, ctgs=cs,comments_five=comments_five)


# 博客详情
@posts.route('/posts_detail/<int:pid>/')
def posts_detail(pid):
    # 查询当前博客的内容 pid为博客的自增id 并不是博客模型字段的pid
    p = Posts.query.get(pid)
    p.visit += 1  # 博客的访问量
    p.save()
    form = Comment()  # 发表评论和回复的表单类
    # 查询出博客的评论内容和回复，按照博客内容和回复在一起的排序顺序，
    # 过滤条件为博客path中包含博客id的，这样博客就将博客的内容过滤出去，只查询评论和留言
    comment = Posts.query.filter(Posts.path.contains(str(pid))).order_by(Posts.path.concat(Posts.id))
    ctgs = Categorys.query.all()
    comment_nums = Posts.query.filter(Posts.path.contains(str(pid))).count()

    return render_template('posts/posts_detail.html', posts=p, form=form, comment=comment, ctgs=ctgs, comment_nums=comment_nums)


# 评论和回复
@posts.route('/comment/', methods=['GET', 'POST'])
@login_required
def comment():
    pid = request.form.get('pid')
    rid = request.form.get('rid')
    # 判断当前是评论还是回复，如果为评论则为假，否则为真
    if rid:
        id = rid
    else:
        id = pid
    p = Posts.query.get(int(id))
    Posts(article=request.form.get('article'), pid=id, path=p.path + id + ',', user=current_user).save()

    return redirect(url_for('posts.posts_detail', pid=pid))


# editor.md的图片上传
@posts.route('/upload_image/', methods=['POST'])
@login_required
@csrf.exempt
def upload_image():
    data = request.files.get('editormd-image-file')
    if not data:
        res = {
            'success': 0,
            'message': '图片失败请重试'
        }
    else:
        ex = os.path.splitext(data.filename)[1]
        filename = datetime.now().strftime('%Y%m%d%H%M%S') + ex
        file = data.stream.read()
        qiniu_store.save(file, filename)
        res = {
            'success': 1,
            'message': '图片上传成功',
            'url': qiniu_store.url(filename)
        }
    return jsonify(res)
