from flask import Flask
from flask_script import Manager
# 导入创建App，并加载整个项目的方法
from App import create_app
from flask_migrate import MigrateCommand


# 调用
app = create_app()
manager = Manager(app)
manager.add_command('db', MigrateCommand)


if __name__ == '__main__':
    manager.run()