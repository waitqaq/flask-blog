from flask import Blueprint,render_template, request,current_app

from App.models import Posts,Categorys
from sqlalchemy import func

main = Blueprint('main', __name__)


# 首页视图
@main.route('/')
@main.route('/index/')
def index():
    try:
        page = int(request.args.get('page',1))
    except:
        page = 1
    # 查询pid为0（是博客内容，不为0则是评论或回复内容），statue为0（所有人可见），按照时间降序显示
    pagination = Posts.query.filter(Posts.pid==0, Posts.state==0).order_by(Posts.timestamp.desc())\
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


    return render_template('main/index.html', posts=data, pagination=pagination, art = art, visit=visit, v=v, ctgs=cs,comments_five=comments_five)
