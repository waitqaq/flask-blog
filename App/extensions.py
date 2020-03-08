from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy  # ORM模型扩展库
from flask_migrate import Migrate # 模型迁移
from flask_mail import Mail  # 邮件发送扩展库
from flask_login import LoginManager  # 处理用户登录的扩展库
from flask_moment import Moment  # 格式化时间显示的扩展库
from flask_uploads import IMAGES, UploadSet,configure_uploads,patch_request_class  # 导入头像上传
from flask_qiniustorage import Qiniu  # 七牛云上传
from flask_wtf.csrf import CSRFProtect

# 实例化
bootstrap = Bootstrap()  # bootstrap扩展库
db = SQLAlchemy()  # ORM模型
migrate = Migrate()  # 模型迁移
mail = Mail()  # 邮件发送
login_manager = LoginManager()  # 处理登录的库
moment = Moment()  # 格式化时间显示的扩展库
file = UploadSet('photos',IMAGES)  # 上传头像的
qiniu_store = Qiniu()
csrf = CSRFProtect()


# 加载app
def init_app(app):
    bootstrap.init_app(app)
    db.init_app(app)
    migrate.init_app(app=app, db=db)
    mail.init_app(app)
    moment.init_app(app)
    login_manager.init_app(app)
    qiniu_store.init_app(app)
    csrf.init_app(app)

    login_manager.login_view = 'user.login'  # 当未登陆时，访问了需要登录的路由时，进行登录的端点
    login_manager.session_protection = 'strong'  # 设置session的保护级别

    # 配置文件上传（头像）
    configure_uploads(app,file)
    patch_request_class(app, size=None)




