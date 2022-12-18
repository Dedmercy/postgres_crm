import logging as log

import sqlalchemy.engine

from app import app, my_render_template
# from app.models import Employee
from forms import RegistrationForm, LoginForm, CreationTaskForm, TimeReportForm
from app import Config

from sqlalchemy import text, create_engine
from flask import render_template, redirect, url_for, flash, request, session
from sqlalchemy.exc import OperationalError
# from flask_login import current_user, login_user, logout_user, login_required
import psycopg2
from psycopg2.extensions import connection as psycopg_connection
from cryptography.fernet import Fernet

from models import UserModel, TaskModel

backend_connection: psycopg_connection = psycopg2.connect(
    database=Config.database,
    user='postgres',
    password='VupsenPupsen228',
    host=Config.host,
    port=Config.port)

user_connections = {}

logger = log.getLogger()

key = b'1acBq-wC927AUid7vfOHm3ldjybC_SihEZqCuTrws-c='



@app.route('/index', methods=['GET', 'POST'])
@app.route('/', methods=['GET', 'POST'])
def index():
    if 'username' not in session:
        return redirect(url_for('login'))

    username = session['username']

    if username not in user_connections.keys():
        return redirect(url_for('login'))

    if request.method == "POST":
        query = f'''
        CALL complete_task({request.form.get('task-select')});'''
        res = query_executor(user_connections[username], query)
        return redirect(url_for('index'))

    query = f'''
    SELECT *
    FROM current_user_tasks_information
    '''
    tasks_query = query_executor(user_connections[username], query)
    tasks_models = TaskModel.parse_from_query(tasks_query)

    return my_render_template('index.html', title='Home', tasks=list(tasks_models))



@app.route('/login', methods=['GET', 'POST'])
def login():
    method_prefix = 'login'

    # если юзер авторизирован, то перебрасывает на главную страницу
    if 'username' in session:
        username = session['username']
        if username in user_connections.keys():
            log.debug(f'[{method_prefix}] {username} user authenticated')
            return redirect(url_for('index'))

    log.debug(f'[{method_prefix}] user not authenticated')

    # если была заполнена форма, то проверяет форму
    form = LoginForm()
    if form.validate_on_submit():
        log.debug(f'[{method_prefix}] form is valid')

        # проверяет наличие юзера с таким логином
        query_find_user_by_login = f'''
        SELECT *
        FROM account
        WHERE login = '{form.username.data}'
        '''

        res = query_executor(backend_connection, query_find_user_by_login)
        if len(res) == 0:
            flash('Invalid username or password!')
            log.debug(f'[{method_prefix}] Invalid username or password')
            return redirect(url_for('login'))

        # выполняет аунтефикацию для юзера
        try:
            # создаёт коннект для юзера
            user_connection: psycopg_connection = psycopg2.connect(
                database=Config.database,
                user=form.username.data,
                password=form.password.data,
                host=Config.host,
                port=Config.port)

            user_connections[form.username.data] = user_connection
            username = form.username.data
            session['username'] = username

            #  получает инфу для юзера
            query_account_info = f'''
            SELECT *
            FROM account
            JOIN user_personal_data 
            ON account.user_data_id = user_personal_data.user_data_id
            WHERE account_id = to_regrole('{username}') '''

            # сохраняет в куки
            account_info = query_executor(backend_connection, query_account_info)
            account_model: UserModel = UserModel.parse_from_query(account_info)[0]
            session['account_model'] = account_model.to_simple_formats()
            session.modified = True
        except OperationalError as e:
            log.debug(f'[{method_prefix}] Invalid username or password')
            flash('Invalid username or password')
            return redirect(url_for('login'))
        return redirect(url_for('index'))
    return render_template('login.html', title='Login', form=form)


@app.route('/logout', methods=['GET', 'POST'])
# @login_required
def logout():
    session.pop('username')
    return redirect(url_for('index'))


# @app.route('/registration', methods=['GET', 'POST'])
# @login_required
# def registration():
#     form = RegistrationForm()
#     if form.validate_on_submit():
#         with backend_connection.connect() as connection:
#             connection.execution_options(isolation_level="AUTOCOMMIT")
#             connection.execute(text(f"CALL add_employee("
#                                     f" '{form.post.data}',"
#                                     f" '{form.first_name.data}',"
#                                     f" '{form.middle_name.data}',"
#                                     f" '{form.last_name.data}',"
#                                     f" '{form.email.data}',"
#                                     f" {form.phone.data},"
#                                     f" '{form.username.data}',"
#                                     f" '{form.password.data}');"))
#
#         return redirect(url_for('index'))
#
#     return render_template('registration.html', title='Registration', form=form)


# @app.route('/create', methods=['GET', 'POST'])
# @login_required
# def create_task():
#     form = CreationTaskForm()
#     with create_engine(Config.SQLALCHEMY_DATABASE_URI).connect() as connection:
#         connection.execution_options(isolation_level="AUTOCOMMIT")
#         contact_persons = connection.execute(text("SELECT c_p_id, c_p_first_name, c_p_last_name"
#                                                   " FROM contact_person"))
#         employees = connection.execute((text("SELECT employee_id, e_first_name, e_last_name "
#                                              "FROM employee")))
#         goods = connection.execute(text("SELECT goods_num, goods_name "
#                                         "FROM goods"))
#
#     contact_persons = [(item[0], f'{item[1] + " " + item[2]}') for item in contact_persons]
#     form.contact_person.choices = contact_persons
#     employees = [(item[0], f'{item[1] + " " + item[2]}') for item in employees]
#     form.employee.choices = employees
#     goods = [(item[0], f'{item[1]}') for item in goods]
#     form.good.choices = goods
#
#     if form.validate_on_submit():
#         with backend_connection.connect() as connection:
#             connection.execution_options(isolation_level="AUTOCOMMIT")
#             connection.execute(text(f"CALL create_task("
#                                     f"{int(form.id.data)},"
#                                     f"{int(form.contact_person.data)},"
#                                     f"{int(form.employee.data)},"
#                                     f"'{str(form.description.data)}'::TEXT,"
#                                     f"'{form.deadline.data}'::TIMESTAMP WITHOUT TIME ZONE,"
#                                     f"{form.priority.data}::SMALLINT,"
#                                     f"{int(form.good.data)}"
#                                     f");"))
#         return redirect(url_for('index'))
#
#     return render_template('creation_task.html', title='Creation Task', form=form)
#
#
# @app.route('/reporting', methods=['GET', 'POST'])
# @login_required
# def reports():
#     form = TimeReportForm()
#     result = []
#
#     with create_engine(Config.SQLALCHEMY_DATABASE_URI).connect() as connection:
#         connection.execution_options(isolation_level="AUTOCOMMIT")
#         employees = connection.execute((text("SELECT employee_id, e_first_name, e_last_name "
#                                              "FROM employee")))
#
#     employees = [(item[0], f'{item[1] + " " + item[2]}') for item in employees]
#     form.id.choices = employees
#
#     if form.validate_on_submit():
#         with backend_connection.connect() as connection:
#             connection.execution_options(isolation_level="AUTOCOMMIT")
#             result = connection.execute(text(f"SELECT * FROM export("
#                                              f"{form.id.data},"
#                                              f"'{form.time_start.data}'::TIMESTAMP WITHOUT TIME ZONE,"
#                                              f"'{form.time_end.data}'::TIMESTAMP WITHOUT TIME ZONE);"))
#     return render_template('main_reports.html', title='Time reporting', form=form, data=list(result))


def query_executor(connection, query: str):
    with connection.cursor() as cursor:
        try:
            cursor.execute(query)
            if cursor.pgresult_ptr is not None:
                result = cursor.fetchall()
        except Exception as e:
            log.warning(f'cannot process query, e: {e}, query: {query}')
            return None

    log.debug(f'processed query: {query}')

    return result


def get_user_connection(user: str):
    if user not in user_connections.keys():
        raise Exception('user isnt logged')
    else:
        return user_connections[user]
