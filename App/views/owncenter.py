from flask import Blueprint, render_template, redirect, url_for, flash, request, current_app

from App.models import Posts,Categorys
from App.forms import UserInfo  # 导入个人信息显示user模型类和文件上传表单类
from App.forms import SendPosts,Upload  # 用于编辑博客
from flask_login import current_user, login_required
from App.extensions import db, file
import os
from App.extensions import file
from PIL import Image

owncenter = Blueprint('owncenter', __name__)


# 查看与修改个人信息
@owncenter.route('/user_info/', methods=['GET', 'POST'])
def user_info():
    form = UserInfo()
    if form.validate_on_submit():
        current_user.age = form.age.data

    form.username.data = current_user.username
    form.age.data = current_user.age
    form.sex.data = str(int(current_user.sex))
    form.email.data = current_user.email
    form.lastLogin.data = current_user.lastLogin
    form.register.data = current_user.registerTime
    return render_template('owncenter/user_info.html', form=form)


# 博客管理
@owncenter.route('/posts_manager/')
def posts_manager():
    try:
        page = int(request.args.get('page', 1))
    except:
        page = 1
    # 查询当前用户发表的所有博客，pid为0证明是博客内容，而不是评论和回复内容。state=0是所有人可见，
    # 按照时间进行降序查询
    posts = current_user.posts.filter_by(pid=0, state=0).order_by(Posts.timestamp.desc())
    # 获取page页面的数据
    pagination = Posts.query.filter(Posts.pid == 0, Posts.state == 0).order_by(Posts.timestamp.desc()) \
        .paginate(page, current_app.config['PAGE_NUM'], False)  # False 为不抛出异常
    data = pagination.items  # 获取page页面的数据

    return render_template('owncenter/posts_manager.html', posts=posts, pagination=pagination)


# 博客删除
@owncenter.route('/del_posts/<int:pid>')
@login_required
def del_posts(pid):
    # 查询博客
    p = Posts.query.get(pid)
    # 判断该博客是否存在
    if p:
        # 执行删除
        flash('删除成功')
        p.delete()  # 删除博客内容
        comment = Posts.query.filter(Posts.path.contains(str(pid)))  # 删除评论和留言的内容
        for posts in comment:
            posts.delete()
    else:
        flash('您要删除的博客不存在')
    return redirect(url_for('owncenter.posts_manager'))


# 使用uuid扩展库生成唯一的名称
def random_filename(suffix):
    import uuid
    u = uuid.uuid4()
    return str(u) + '.' + suffix


# 图片缩放处理
def img_zoom(path, width=100, height=100):
    # 打开文件
    img = Image.open(path)
    # 重新设计尺寸
    img.thumbnail((width, height))
    # 保存缩放后的图片 保留原图片
    # 保存缩放
    img.save(path)


#  头像上传
@owncenter.route('/upload/', methods=['GET', 'POST'])
@login_required
def upload():
    form = Upload()
    if form.validate_on_submit():
        icon = request.files.get('icon')  # 获取上传对象
        suffix = icon.filename.split('.')[-1]  # 获取后缀
        newName = random_filename(suffix)  # 获取新图片的名称
        # 以新名称保存图片
        file.save(icon, name=newName)
        delPath = current_app.config['UPLOADED_PHOTOS_DEST']
        # 删除之前上传的图片
        if current_user.icon != 'default.jpg':  # 如果不等于，则证明上传了头像
            os.remove(os.path.join(delPath, current_user.icon))
        current_user.icon = newName  # 更改当前对象的图片名称
        db.session.add(current_user)  # 更新到数据库中
        db.session.commit()
        # 拼接图片路径
        path = os.path.join(delPath, newName)
        # 进行缩放
        img_zoom(path)

    return render_template('owncenter/upload.html', form=form)


# 博客编辑
@owncenter.route('/edit_posts/<int:pid>', methods=['POST', 'GET'])
def edit_posts(pid):
    form = SendPosts()  # 实例化表单
    p = Posts.query.get(pid)  # 根据博客id  查询
    ctgs = Categorys.query.all()
    if not p:
        flash('该博客不存在')
        return redirect(url_for('owncenter.posts_manager'))
    if form.validate_on_submit():
        # md格式
        article = request.form['article']
        # 得到所选的分类值
        ctg = request.values.get('ctgs')
        # 将所选择的分类值在数据库中进行查找
        ctg_id = Categorys.query.filter(Categorys.categorys == ctg).first()
        # 图片上传
        img = request.files.get('img')  # 获取上传对象
        suffix = img.filename.split('.')[-1]  # 获取后缀
        newName = random_filename(suffix)  # 获取新图片的名称
        # 以新名称保存图片
        file.save(img, name=newName)
        delPath = current_app.config['UPLOADED_PHOTOS_DEST']
        # 拼接图片路径
        path = os.path.join(delPath, newName)
        # 进行缩放
        img_zoom(path)

        p.title = form.title.data
        p.article = article
        p.categorys = ctg_id
        p.img = newName
        p.save()
        flash('博客更新成功')
        return redirect(url_for('owncenter.posts_manager'))
    form.title.data = p.title
    form.article.data = p.article

    return render_template('owncenter/edit_posts.html', form=form,ctgs=ctgs)
