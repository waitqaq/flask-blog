from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Length
from flask_wtf.file import FileAllowed, FileRequired, FileField
from App.extensions import file  # 导入文件上传配置对象


# 发表博客的表单类
class SendPosts(FlaskForm):
    title = StringField('标题', validators=[DataRequired('标题内容不能为空'),
                                          Length(min=3,max=20,message='标题内容在3-20字之间')],render_kw={'placeholder':'请输入标题'})
    article = TextAreaField('博客内容', validators=[DataRequired('博客内容不能为空')],render_kw={'placeholder':'请输入博客内容'})

    submit = SubmitField('发表博客')


# 发表评论和回复的表单类
class Comment(FlaskForm):
    article = TextAreaField('评论内容', validators=[DataRequired('评论内容不能为空')])
    submit = SubmitField('发表评论')


# 添加分类的表单
class Catgs(FlaskForm):
    categorys = StringField('分类专栏', validators=[DataRequired('分类专栏不能为空'),
                                                Length(min=2, max=20, message='分类内容在2-15字之间')],
                            render_kw={'placeholder': '请输入分类'})