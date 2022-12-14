import logging as log

from app import app
from app.models import Employee
from app.forms import RegistrationForm, LoginForm, CreationTaskForm, TimeReportForm
from app import Config

from sqlalchemy import text, create_engine
from flask import render_template, redirect, url_for, flash, request
from sqlalchemy.exc import OperationalError
from flask_login import current_user, login_user, logout_user, login_required

current_connection = {"Engine": None}

logger = log.getLogger()


@app.route('/index', methods=['GET', 'POST'])
@app.route('/', methods=['GET', 'POST'])
def index():
    tasks = []
    if current_user.is_authenticated:
        with create_engine(Config.SQLALCHEMY_DATABASE_URI).connect() as connection:
            tasks = connection.execute(text(f"SELECT "
                                            f"task.task_id as id,"
                                            f"c_p_id,"
                                            f"task_decription,"
                                            f"task_create_datetime,"
                                            f"task_deadline_datetime,"
                                            f"task_status_name,"
                                            f"task_completed_datetime,"
                                            f"task_priority "
                                            f"FROM task "
                                            f"JOIN task_status "
                                            f"ON task_status.task_id=task.task_id "
                                            f"WHERE executor={current_user.employee_id}"))
    if request.method == "POST":
        with current_connection['Engine'].connect() as connection:
            connection.execution_options(isolation_level="AUTOCOMMIT")
            connection.execute(text(f"CALL complete_task({request.form.get('task-select')});"))
        return redirect(url_for('index'))

    return render_template('index.html', title='Home', tasks=list(tasks))


@app.route('/login', methods=['GET', 'POST'])
def login():
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
                current_connection['Engine'] = create_engine(uri)
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
        with current_connection['Engine'].connect() as connection:
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
        with current_connection['Engine'].connect() as connection:
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
        with current_connection['Engine'].connect() as connection:
            connection.execution_options(isolation_level="AUTOCOMMIT")
            result = connection.execute(text(f"SELECT * FROM export("
                                             f"{form.id.data},"
                                             f"'{form.time_start.data}'::TIMESTAMP WITHOUT TIME ZONE,"
                                             f"'{form.time_end.data}'::TIMESTAMP WITHOUT TIME ZONE);"))
    return render_template('main_reports.html', title='Time reporting', form=form, data=list(result))
