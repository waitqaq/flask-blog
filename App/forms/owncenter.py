from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, RadioField
from wtforms.validators import DataRequired, NumberRange
from flask_wtf.file import FileAllowed, FileRequired, FileField
from App.extensions import file  # 导入文件上传配置对象


# 修改与查看个人信息的表单类
class UserInfo(FlaskForm):
    username = StringField('用户名', render_kw={'readonly': 'true'})
    sex = RadioField(label='性别', choices=[('1', '男'), ('0', '女')], validators=[DataRequired('性别必选')])
    age = IntegerField('年龄', validators=[DataRequired('年龄不能为空'), NumberRange(min=1, max=99, message='年龄在1~99之间')])
    email = StringField('邮箱', render_kw={'readonly': 'true'})
    lastLogin = StringField('上次登录时间', render_kw={'disabled': 'true'})
    register = StringField('注册时间', render_kw={'disabled': 'true'})
    submit = SubmitField('修改')


# 文件上传
class Upload(FlaskForm):
    icon = FileField('头像上传', validators=[FileRequired('您还没有选择上传的头像'),FileAllowed(file, message='该文件类型不允许上传')])
    submit = SubmitField('上传')