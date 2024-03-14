from flask_admin import AdminIndexView, BaseView, expose
from flask_admin.contrib.sqla import ModelView
from flask import redirect, url_for
from flask_login import current_user, login_required


class MyModelView(ModelView):

    def is_accessible(self):
        return current_user.is_authenticated and current_user.username == 'root'

    def inaccessible_callback(self, name, **kwargs):
        return redirect('/admin/login')


class MyAdminIndexView(AdminIndexView):

    def is_accessible(self):
        return current_user.is_authenticated and current_user.username == 'root'

    def inaccessible_callback(self, name, **kwargs):
        return redirect('/admin/login')


class UserModelView(MyModelView):

    column_list = ['user_id', 'username', 'gender', 'contact', 'subject_type',
                   'subject_1', 'subject_2', 'subject_3', 'subject_4']
    column_editable_list = ['username', 'gender', 'contact', 'subject_type',
                            'subject_1', 'subject_2', 'subject_3', 'subject_4']
    column_filters = ['user_id', 'username', 'gender', 'contact', 'subject_type',
                      'subject_1', 'subject_2', 'subject_3', 'subject_4', 'birthday']


class CarModelView(MyModelView):

    column_list = ['car_id', 'car_name', 'car_type', 'is_available', 'user_count', 'subject_type']
    column_editable_list = ['car_name', 'car_type', 'is_available', 'user_count', 'subject_type']
    column_filters = ['car_id', 'car_name', 'car_type', 'is_available', 'user_count', 'subject_type']


class SubjectModelView(MyModelView):

    column_list = ['subject_id', 'user_id', 'car_id', 'subject_type', 'subject_number']
    column_editable_list = ['user_id', 'car_id', 'subject_type', 'subject_number']
    column_filters = ['subject_id', 'user_id', 'car_id', 'subject_type', 'subject_number']


class LogoutView(BaseView):

    @expose('/')
    def index(self):
        return redirect('/admin/logout')