from flask import Flask, request, redirect, url_for, render_template
from flask_sqlalchemy import SQLAlchemy as BaseSQLAlchemy
from flask_admin import Admin
from contextlib import contextmanager
from config import DevelopmentConfig
from werkzeug.exceptions import HTTPException
from flask_bootstrap import Bootstrap
from flask_restful import Api
from flask_login import login_user, logout_user, current_user, login_required, LoginManager, UserMixin
from enum import Enum
from werkzeug.security import generate_password_hash, check_password_hash
from utils import str_to_datetime


class SQLAlchemy(BaseSQLAlchemy):

    @contextmanager
    def auto_commit(self):
        """
        自动提交函数，使用回滚来处理 sqlalchemy 异常
        :return: 异常或者生成器
        """
        try:
            yield
            self.session.commit()
        except Exception as e:
            self.session.rollback()
            raise e


app = Flask(__name__)
app.config.from_object(DevelopmentConfig())
db = SQLAlchemy(app)

# 数据库


class User(db.Model, UserMixin):

    __tablename__ = 'User'
    user_id = db.Column('user_id', db.Integer, primary_key=True, autoincrement=True)
    gender = db.Column('gender', db.Integer, nullable=False)  # 1 is man, 2 is woman
    password_hash = db.Column('password', db.String(128), nullable=False)
    # 用户名唯一
    username = db.Column('username', db.String(64), nullable=False, unique=True)
    birthday = db.Column('birthday', db.DateTime, nullable=True)
    contact = db.Column('contact', db.String(64), nullable=False)
    # 考试情况
    # C1, C2
    subject_type = db.Column('subject_type', db.Integer, nullable=False)
    subject_1 = db.Column('subject_1', db.Boolean, nullable=False)
    subject_2 = db.Column('subject_2', db.Boolean, nullable=False)
    subject_3 = db.Column('subject_3', db.Boolean, nullable=False)
    subject_4 = db.Column('subject_4', db.Boolean, nullable=False)

    def __init__(self, gender, password, username, contact, subject_type=0, subject_1=False, subject_2=False, subject_3=False, subject_4=False, birthday=None):
        self.gender = gender
        self.password_hash = password
        self.username = username
        self.contact = contact
        self.subject_type = subject_type
        self.subject_1 = subject_1
        self.subject_2 = subject_2
        self.subject_3 = subject_3
        self.subject_4 = subject_4
        self.birthday = birthday

    def get_id(self):
        try:
            return str(self.user_id)
        except AttributeError:
            raise NotImplementedError("No `id` attribute - override `get_id`") from None

    def to_dict(self):
        return {
            'user_id': self.user_id,
            'username': self.username,
            'gender': self.gender,
            'contact': self.contact,
            'subject_type': self.subject_type,
            'subject_1': self.subject_1,
            'subject_2': self.subject_2,
            'subject_3': self.subject_3,
            'subject_4': self.subject_4,
            'birthday': self.birthday
        }


class Car(db.Model):

    __tablename__ = 'Car'
    car_id = db.Column('car_id', db.Integer, primary_key=True, autoincrement=True)
    car_name = db.Column('car_name', db.String(64), nullable=False)
    # C1, C2
    car_type = db.Column('car_type', db.Integer, nullable=False)
    is_available = db.Column('is_available', db.Boolean, nullable=False)
    user_count = db.Column('user_count', db.Integer, nullable=False)
    # 1, 2, 3, 4
    subject_type = db.Column('subject_type', db.Integer, nullable=False)

    def __init__(self, car_name, car_type, is_available=True, user_count=0, subject_type=0):
        self.car_name = car_name
        self.car_type = car_type
        self.is_available = is_available
        self.user_count = user_count
        self.subject_type = subject_type

    def get_id(self):
        try:
            return str(self.car_id)
        except AttributeError:
            raise NotImplementedError("No `id` attribute - override `get_id`") from None

    def to_dict(self):
        return {
            'car_id': self.car_id,
            'car_name': self.car_name,
            'car_type': self.car_type,
            'is_available': self.is_available,
            'user_count': self.user_count,
            'subject_type': self.subject_type
        }


class Subject(db.Model):

    __tablename__ = 'Subject'
    subject_id = db.Column('subject_id', db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column('user_id', db.Integer, db.ForeignKey('User.user_id',
                                                             ondelete='cascade', onupdate='cascade'), nullable=False)
    car_id = db.Column('car_id', db.Integer, db.ForeignKey('Car.car_id',
                                                   ondelete='cascade', onupdate='cascade'), nullable=False)
    # C1, C2
    subject_type = db.Column('subject_type', db.Integer, nullable=False)
    # 1, 2, 3, 4
    subject_number = db.Column('subject_number', db.Integer, nullable=False)

    __table_args__ = (
        db.UniqueConstraint('user_id', 'car_id', name='user_car_id'),
    )

    def __init__(self, user_id, car_id, subject_type, subject_number):
        self.user_id = user_id
        self.car_id = car_id
        self.subject_type = subject_type
        self.subject_number = subject_number

    def to_dict(self):
        return {
            'subject_id': self.subject_id,
            'user_id': self.user_id,
            'car_id': self.car_id,
            'subject_type': self.subject_type,
            'subject_number': self.subject_number
        }


class UserDAO:

    @classmethod
    def add_user(cls, database, data: dict):
        password_hash = generate_password_hash(data['password'])
        birthday = str_to_datetime(data.get('birthday'))
        new_user = User(
            gender=data['gender'],
            password=password_hash,
            username=data['username'],
            contact=data['contact'],
            subject_type=0 if data.get('subject_type') is None else data['subject_type'],
            subject_1=False if data.get('subject_1') is None else data['subject_1'],
            subject_2=False if data.get('subject_2') is None else data['subject_2'],
            subject_3=False if data.get('subject_3') is None else data['subject_3'],
            subject_4=False if data.get('subject_4') is None else data['subject_4'],
            birthday=birthday
        )
        with database.auto_commit():
            database.session.add(new_user)
        return new_user.user_id

    @classmethod
    def add_user_in_bulk(cls, database, data: list):
        user_list = []
        user_name_list = []
        user_id_list = []
        for d in data:
            password_hash = generate_password_hash(d['password'])
            birthday = str_to_datetime(d.get('birthday'))
            new_user = User(
                gender=d['gender'],
                password=password_hash,
                username=d['username'],
                contact=d['contact'],
                subject_type=0 if d.get('subject_type') is None else d['subject_type'],
                subject_1=False if d.get('subject_1') is None else d['subject_1'],
                subject_2=False if d.get('subject_2') is None else d['subject_2'],
                subject_3=False if d.get('subject_3') is None else d['subject_3'],
                subject_4=False if d.get('subject_4') is None else d['subject_4'],
                birthday=birthday
            )
            user_list.append(new_user)
            user_name_list.append(d['username'])
        with database.auto_commit():
            database.session.bulk_save_objects(user_list)
        for username in user_name_list:
            cur_user = database.session.query(User).filter_by(username=username).first()
            user_id_list.append(cur_user.user_id)
        return user_id_list

    @classmethod
    def delete_user_by_id(cls, database, user_id):
        with database.auto_commit():
            cur_user = database.session.query(User).filter_by(user_id=user_id).first()
            database.session.delete(cur_user)

    @classmethod
    def delete_user_by_name(cls, database, username):
        with database.auto_commit():
            cur_user = database.session.query(User).filter_by(username=username).first()
            database.delete(cur_user)

    @classmethod
    def delete_user_by_filter(cls, database, args):
        query_list = cls.get_user_filter(args)
        with database.auto_commit():
            database.session.query(User).filters(*query_list).delete()

    @classmethod
    def update_user_by_id(cls, database, user_id, data: dict):
        with database.auto_commit():
            for key, value in data.items():
                if value is not None:
                    if key == 'password':
                        value = generate_password_hash(value)
                    elif key == 'birthday':
                        value = str_to_datetime(value)
                    database.session.query(User).filter_by(user_id=user_id).update({key: value})

    @classmethod
    def update_user_by_name(cls, database, username, data: dict):
        query_user = database.session.query(User).filter_by(username=username).first()
        if query_user:
            user_id = query_user.user_id
            cls.update_user_by_id(database, user_id, data)

    @classmethod
    def get_user_by_id(cls, database, user_id):
        cur_user = database.session.query(User).filter_by(user_id=user_id).first()
        if cur_user:
            return cur_user.to_dict()
        return {}

    @classmethod
    def get_user_by_name(cls, database, username):
        cur_user = database.session.query(User).filter_by(username=username).first()
        if cur_user:
            return cur_user.to_dict()
        return {}

    @classmethod
    def get_user_by_filter(cls, database, args):
        query_list = cls.get_user_filter(args)
        query_result = database.session.query(User).filter(*query_list).all()
        query_data = []
        for obj in query_result:
            query_data.append(obj.to_dict())
        return query_data

    @classmethod
    def get_user_entity_by_name(cls, database, username):
        return database.session.query(User).filter_by(username=username).first()

    @classmethod
    def get_user_filter(cls, args):
        query_dict = {}
        if args.get('user_id') is not None:
            query_dict[User.user_id] = args.get('user_id')
            return query_dict
        if args.get('username') is not None:
            query_dict[User.username] = args.get('username')
            return query_dict
        if args.get('gender') is not None:
            query_dict[User.gender] = args.get('gender')
        if args.get('birthday') is not None:
            query_dict[User.birthday] = args.get('birthday')
        if args.get('contact') is not None:
            query_dict[User.contact] = args.get('contact')
        if args.get('subject_type') is not None:
            query_dict[User.subject_type] = args.get('subject_type')
        if args.get('subject_1') is not None:
            query_dict[User.subject_1] = args.get('subject_1')
        if args.get('subject_2') is not None:
            query_dict[User.subject_2] = args.get('subject_2')
        if args.get('subject_3') is not None:
            query_dict[User.subject_3] = args.get('subject_3')
        if args.get('subject_4') is not None:
            query_dict[User.subject_4] = args.get('subject_4')
        return query_dict

    @classmethod
    def check_password_by_username(cls, database, password, username):
        cur_user = database.session.query(User).filter_by(username=username).first()
        return check_password_hash(cur_user.password_hash, password)


class CarDAO:

    @classmethod
    def add_car(cls, database, data: dict):
        new_car = Car(
            car_name=data['car_name'],
            car_type=data['car_type'],
            is_available=True if data.get('is_available') is None else data['is_available'],
            user_count=0 if data.get('user_count') is None else data['user_count'],
            subject_type=0 if data.get('subject_type') is None else data['subject_type']
        )
        with database.auto_commit():
            database.session.add(new_car)
        return new_car.car_id

    @classmethod
    def delete_car_by_id(cls, database, car_id):
        with database.auto_commit():
            database.session.query(Car).filter_by(car_id=car_id).delete()

    @classmethod
    def update_car_by_id(cls, database, car_id, data: dict):
        with database.auto_commit():
            database.session.query(Car).filter_by(car_id=car_id).update(data)

    @classmethod
    def get_car_by_id(cls, database, car_id):
        result = database.session.query(Car).filter_by(car_id=car_id).first()
        if result:
            return result.to_dict()
        return {}


class SubjectDAO:

    @classmethod
    def add_subject(cls, database, data: dict):
        new_subject = Subject(
            user_id=data['user_id'],
            car_id=data['car_id'],
            subject_type=data['subject_type'],
            subject_number=data['subject_number']
        )
        with database.auto_commit():
            database.session.add(new_subject)
        return new_subject.subject_id

    @classmethod
    def delete_subject_by_id(cls, database, subject_id):
        with database.auto_commit():
            database.session.query(Subject).filter_by(subject_id=subject_id).delete()

    @classmethod
    def delete_subject_by_user_car_id(cls, database, user_id, car_id):
        with database.auto_commit():
            database.session.query(Subject).filter(Subject.user_id == user_id,
                                                   Subject.car_id == car_id).delete()

    @classmethod
    def update_subject_by_id(cls, database, subject_id, data: dict):
        with database.auto_commit():
            database.session.query(Subject).filter_by(subject_id=subject_id).update(data)

    @classmethod
    def get_subject_by_id(cls, database, subject_id):
        result = database.session.query(Subject).filter_by(subject_id=subject_id).first()
        if result:
            return result.to_dict()
        return {}


from APIException import handle_api_exception, ApiException, handle_all_exception, handle_http_exception

app.register_error_handler(HTTPException, handle_http_exception)
app.register_error_handler(ApiException, handle_api_exception)
app.register_error_handler(Exception, handle_all_exception)

from adminResource import MyModelView, UserModelView, CarModelView, SubjectModelView, LogoutView, MyAdminIndexView

admin = Admin(app, name='MyAdmin', template_mode='bootstrap3', index_view=MyAdminIndexView())
admin.add_view(UserModelView(User, db.session))
admin.add_view(CarModelView(Car, db.session))
admin.add_view(SubjectModelView(Subject, db.session))
admin.add_view(LogoutView(name='Logout'))

login_manager = LoginManager(app)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route('/', methods=['GET'])
def index():
    return redirect('/admin/login')


@app.route('/admin/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if check_password_hash(user.password_hash, password):
            login_user(user)
            return redirect(url_for('admin.index'))
    return render_template('login.html')


@app.route('/admin/logout', methods=['GET'])
def logout():
    logout_user()
    return redirect('/admin/login')


if __name__ == "__main__":
    app.run()



