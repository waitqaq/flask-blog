from flask import Blueprint,render_template,flash,url_for,redirect
from App.forms import Register, Login, AgainActive  # 导入表单注册类
from App.models import User  # 导入User模型类
from App.email import send_mail  # 导入发送邮件的函数
from flask_login import login_required, logout_user, login_user, current_user
from datetime import datetime


user = Blueprint('user', __name__)


@user.route('/register/', methods=['GET', 'POST'])
def register():
    # 实例化注册表单类
    form = Register()
    if form.validate_on_submit():
        # 实例化存储注册表单数据
        u = User(username=form.username.data, password=form.userpass.data,email=form.email.data)
        u.save()
        # 调用获取token的方法
        token = u.generate_token()
        # 发送邮件激活
        send_mail('账户激活', form.email.data,username=form.username.data, token=token)
        flash('注册成功，请前去邮箱激活')
        # 成功去登录
        return redirect(url_for('user.login'))
    return render_template('user/register.html', form=form)


# 进行账户激活的视图
@user.route('/active/<token>')
def active(token):
    if User.check_token(token):
        flash('激活成功，请前去登录...')
        # 激活成功跳转到登录
        return redirect(url_for('user.login'))
    else:
        flash('激活失败，请重新进行账户激活操作....')
        return redirect(url_for('user.again_active'))


# 再次激活的视图
@user.route('/again_active/',methods=['GET', 'POST'])
def again_active():
    form = AgainActive()
    if form.is_submitted():
        u = User.query.filter(User.username == form.username.data).first()
        if not u:
            flash('请输入正确的用户名或密码....')
        elif not u.check_password(form.userpass.data):
            flash('请输入正确的用户名或密码')
        elif not u.confirm:
            # 调用获取token的方法
            token = u.generate_token()
            # 发送邮件激活
            send_mail('账户再次激活', u.email,tem='again_active', username=form.username.data, token=token)
            flash('激活邮件发送成功，请前去邮箱激活')
        else:
            flash('该账户已经激活，请前去登录...')
    return render_template('user/again_active.html', form=form)


# 登录视图
@user.route('/login/', methods=['GET', 'POST'])
def login():
    form = Login()
    if form.validate_on_submit():
        u = User.query.filter(User.username == form.username.data).first()
        if not u:
            flash('请输入正确的用户名或密码')
        elif not u.confirm:
            flash('您还没有进行激活，请前去激活账户')
            return redirect(url_for('user.again_active'))
        elif not u.check_password(form.userpass.data):
            flash('请输入正确的用户名或密码')
        else:
            flash('登录成功')
            # 修改登录时间
            u.lastLogin = datetime.now()
            u.save()
            login_user(u, remember=form.remember.data)  # 使用第三方扩展库处理登录状态的维持
            return redirect(url_for('main.index'))

    return render_template('user/login.html', form=form)


# 退出登录
@user.route('logout')
def logout():
    logout_user()
    flash('退出成功')
    return redirect(url_for('main.index'))