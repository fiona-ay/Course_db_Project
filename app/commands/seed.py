"""
数据库初始化命令
用于初始化测试用户数据
"""
import click
from werkzeug.security import generate_password_hash
from flask.cli import with_appcontext
from app import db
from app.models.student import Student
from app.models.teacher import Teacher
from app.models.admin import Admin
from app.models.laboratory import Laboratory


@click.command('init-users')
@click.option('--password', default='123456', help='默认密码（默认：123456）')
@with_appcontext
def init_users(password):
    """
    初始化测试用户数据
    
    创建以下测试用户：
    - 学生: ID="2023001", Role="student", Lab="L1"
    - 导师: ID="T001", Role="teacher", Lab="L1"
    - 管理员: ID="admin", Role="admin"
    
    所有用户的默认密码为 123456（可通过 --password 参数修改）
    """
    try:
        click.echo('开始初始化测试用户...')
        
        # 确保实验室 L1 存在（ID=1）
        lab = Laboratory.query.filter_by(id=1).first()
        if not lab:
            click.echo('创建实验室 L1 (ID=1)...')
            lab = Laboratory(id=1, name='L1', location='实验室L1')
            db.session.add(lab)
            db.session.commit()
            click.echo('[OK] 实验室 L1 创建成功')
        else:
            click.echo('[OK] 实验室 L1 已存在')
        
        # 生成密码Hash
        password_hash = generate_password_hash(password)
        
        # 创建学生用户
        student = Student.query.filter_by(id='2023001').first()
        if not student:
            click.echo('创建学生用户: 2023001...')
            student = Student(
                id='2023001',
                name='测试学生',
                password_hash=password_hash,
                dept='计算机学院',
                lab_id=1,
                lab_name='L1'
            )
            db.session.add(student)
            click.echo('[OK] 学生用户创建成功')
        else:
            student.password_hash = password_hash
            click.echo('[OK] 学生用户已存在，已更新密码')
        
        # 创建导师用户
        teacher = Teacher.query.filter_by(id='T001').first()
        if not teacher:
            click.echo('创建导师用户: T001...')
            teacher = Teacher(
                id='T001',
                name='测试导师',
                password_hash=password_hash,
                dept='计算机学院',
                lab_id=1
            )
            db.session.add(teacher)
            click.echo('[OK] 导师用户创建成功')
        else:
            teacher.password_hash = password_hash
            click.echo('[OK] 导师用户已存在，已更新密码')
        
        # 创建管理员用户
        admin = Admin.query.filter_by(id='admin').first()
        if not admin:
            click.echo('创建管理员用户: admin...')
            admin = Admin(
                id='admin',
                name='系统管理员',
                password_hash=password_hash,
                manage_scope=1
            )
            db.session.add(admin)
            click.echo('[OK] 管理员用户创建成功')
        else:
            admin.password_hash = password_hash
            click.echo('[OK] 管理员用户已存在，已更新密码')
        
        # 提交事务
        db.session.commit()
        
        click.echo('\n[OK] 所有测试用户初始化完成！')
        click.echo(f'\n测试账号信息：')
        click.echo(f'  学生: 学号=2023001, 密码={password}')
        click.echo(f'  导师: 工号=T001, 密码={password}')
        click.echo(f'  管理员: ID=admin, 密码={password}')
        
    except Exception as e:
        db.session.rollback()
        click.echo(f'[ERROR] 初始化失败: {str(e)}', err=True)
        raise click.Abort()


def register_commands(app):
    """注册CLI命令到Flask应用"""
    app.cli.add_command(init_users)

