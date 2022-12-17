import logging as log

import sqlalchemy.engine

from app import app
# from app.models import Employee
from app.forms import RegistrationForm, LoginForm, CreationTaskForm, TimeReportForm
from app import Config

from sqlalchemy import text, create_engine
from flask import render_template, redirect, url_for, flash, request, session
from sqlalchemy.exc import OperationalError
from flask_login import current_user, login_user, logout_user, login_required
import psycopg2
from psycopg2.extensions import connection as psycopg_connection

backend_connection: psycopg_connection = psycopg2.connect(
    database='postgres',
    user='postgres',
    password='VupsenPupsen228',
    host='0.0.0.0',
    port='5431')

logger = log.getLogger()


@app.route('/index', methods=['GET', 'POST'])
@app.route('/', methods=['GET', 'POST'])
def index():
    if 'username' not in session:
        return redirect(url_for('login'))
    else:
        query = f'''
        SELECT *
        FROM task
        JOIN task_status
        ON task_status.task_id=task.task_id
        WHERE executor={session['username']}
        '''
        task = query_executor(query)
    # if request.method == "POST":
    #     with backend_connection.cursor() as cursor:
    #         connection.execution_options(isolation_level="AUTOCOMMIT")
    #         connection.execute(text(f"CALL complete_task({request.form.get('task-select')});"))
    #     return redirect(url_for('index'))

    return render_template('index.html', title='Home', tasks=list(tasks))


@app.route('/login', methods=['GET', 'POST'])
def login():
    global backend_connection
    method_prefix = 'login'

    if current_user.is_authenticated:
        return redirect(url_for('index'))

    log.debug(f'[{method_prefix}] user not authenticated')

    form = LoginForm()
    if form.validate_on_submit():
        log.debug(f'[{method_prefix}] form is valid')
        employee = Employee.query.filter_by(e_nickname=form.username.data, ).first()
        if employee is None:
            flash('Invalid username or password')
            log.debug(f'[{method_prefix}] Invalid username or password')
            return redirect(url_for('login'))
        try:
            uri = f'postgresql://{form.username.data}:{form.password.data}@{Config.SQLALCHEMY_DATABASE_ADDRESS}'
            if [row[0] for row in create_engine(uri).connect().execute(text("SELECT 1"))] == [1]:
                backend_connection = create_engine(uri)
        except OperationalError as e:
            log.debug(f'[{method_prefix}] Invalid username or password')
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(employee)
        return redirect(url_for('index'))
    return render_template('login.html', title='Login', form=form)


@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/registration', methods=['GET', 'POST'])
@login_required
def registration():
    form = RegistrationForm()
    if form.validate_on_submit():
        with backend_connection.connect() as connection:
            connection.execution_options(isolation_level="AUTOCOMMIT")
            connection.execute(text(f"CALL add_employee("
                                    f" '{form.post.data}',"
                                    f" '{form.first_name.data}',"
                                    f" '{form.middle_name.data}',"
                                    f" '{form.last_name.data}',"
                                    f" '{form.email.data}',"
                                    f" {form.phone.data},"
                                    f" '{form.username.data}',"
                                    f" '{form.password.data}');"))

        return redirect(url_for('index'))

    return render_template('registration.html', title='Registration', form=form)


@app.route('/create', methods=['GET', 'POST'])
@login_required
def create_task():
    form = CreationTaskForm()
    with create_engine(Config.SQLALCHEMY_DATABASE_URI).connect() as connection:
        connection.execution_options(isolation_level="AUTOCOMMIT")
        contact_persons = connection.execute(text("SELECT c_p_id, c_p_first_name, c_p_last_name"
                                                  " FROM contact_person"))
        employees = connection.execute((text("SELECT employee_id, e_first_name, e_last_name "
                                             "FROM employee")))
        goods = connection.execute(text("SELECT goods_num, goods_name "
                                        "FROM goods"))

    contact_persons = [(item[0], f'{item[1] + " " + item[2]}') for item in contact_persons]
    form.contact_person.choices = contact_persons
    employees = [(item[0], f'{item[1] + " " + item[2]}') for item in employees]
    form.employee.choices = employees
    goods = [(item[0], f'{item[1]}') for item in goods]
    form.good.choices = goods

    if form.validate_on_submit():
        with backend_connection.connect() as connection:
            connection.execution_options(isolation_level="AUTOCOMMIT")
            connection.execute(text(f"CALL create_task("
                                    f"{int(form.id.data)},"
                                    f"{int(form.contact_person.data)},"
                                    f"{int(form.employee.data)},"
                                    f"'{str(form.description.data)}'::TEXT,"
                                    f"'{form.deadline.data}'::TIMESTAMP WITHOUT TIME ZONE,"
                                    f"{form.priority.data}::SMALLINT,"
                                    f"{int(form.good.data)}"
                                    f");"))
        return redirect(url_for('index'))

    return render_template('creation_task.html', title='Creation Task', form=form)


@app.route('/reporting', methods=['GET', 'POST'])
@login_required
def reports():
    form = TimeReportForm()
    result = []

    with create_engine(Config.SQLALCHEMY_DATABASE_URI).connect() as connection:
        connection.execution_options(isolation_level="AUTOCOMMIT")
        employees = connection.execute((text("SELECT employee_id, e_first_name, e_last_name "
                                             "FROM employee")))

    employees = [(item[0], f'{item[1] + " " + item[2]}') for item in employees]
    form.id.choices = employees

    if form.validate_on_submit():
        with backend_connection.connect() as connection:
            connection.execution_options(isolation_level="AUTOCOMMIT")
            result = connection.execute(text(f"SELECT * FROM export("
                                             f"{form.id.data},"
                                             f"'{form.time_start.data}'::TIMESTAMP WITHOUT TIME ZONE,"
                                             f"'{form.time_end.data}'::TIMESTAMP WITHOUT TIME ZONE);"))
    return render_template('main_reports.html', title='Time reporting', form=form, data=list(result))


def query_executor(query: str):
    with backend_connection.cursor() as cursor:
        try:
            cursor.execute(query)
            if cursor.pgresult_ptr is not None:
                result = cursor.fetchall()
        except Exception as e:
            log.warning(f'cannot process query, e: {e}, query: {query}')

    log.debug(f'processed query: {query}')

    return result
