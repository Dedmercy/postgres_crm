import logging as log
from app import app, Config, errors
from app.forms import RegistrationForm, LoginForm, AddPerkForm, CreationTaskForm, FindFreelancerByPerkForm
from app.models import UserModel, TaskModel

from flask import render_template, redirect, url_for, flash, request, session, abort
from sqlalchemy.exc import OperationalError
import psycopg2
from psycopg2.extensions import connection as psycopg_connection

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

    query = ''

    # Если пользователь фрилансер
    if session['account_model']['role_id'] == 16500:
        if request.method == "POST":
            query = f'''
                CALL complete_task({request.form.get('task-select')});
            '''
            query_executor(user_connections[username], query)
            return redirect(url_for('index'))

        query = f'''
            SELECT *
            FROM current_freelancer_tasks_information
        '''

    # Если пользователь заказчик
    elif session['account_model']['role_id'] == 16499:
        query = f'''
                    SELECT *
                    FROM current_client_tasks_information
                '''

    tasks_query = query_executor(user_connections[username], query)
    tasks_models = []

    if tasks_query:
        tasks_models = TaskModel.parse_from_query(tasks_query)

    return render_template('index.html', title='Home', tasks=tasks_models,
                           current_user=session['account_model'])


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
                ON account.account_id = user_personal_data.user_data_id
                WHERE account.account_id = to_regrole('{username}');
            '''

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
def logout():
    session.pop('username')
    session.pop('account_model')
    return redirect(url_for('index'))


@app.route('/registration', methods=['GET', 'POST'])
def registration():
    log_prefix = 'registration'

    if 'username' in session:
        username = session['username']
        if username in user_connections.keys():
            log.debug(f'[{log_prefix}] {username} user authenticated')
            return redirect(url_for('index'))

    form: RegistrationForm = RegistrationForm()
    if form.validate_on_submit():

        registration_query = f'''
            CALL create_user(
                '{form.first_name.data}',
                '{form.middle_name.data}',
                '{form.last_name.data}',
                '{form.email.data}',
                {form.phone.data},
                '{form.username.data}',
                '{form.password.data}',
                '{form.post.data}');
        '''
        try:
            log.debug(f'{log_prefix} try to {registration_query}')
            query_executor(backend_connection, registration_query)
        except Exception as e:
            log.debug(e)

        return redirect(url_for('index'))

    return render_template('registration.html', title='Registration', form=form, current_user={})


@app.route('/perks', methods=['GET', 'POST'])
def perks():
    if 'username' not in session:
        return redirect(url_for('login'))

    username = session['username']

    if username not in user_connections.keys():
        return redirect(url_for('login'))

    if session['account_model']['role_id'] != 16500:
        abort(403)

    form: AddPerkForm = AddPerkForm()

    query_find_all_spezializations = f'''
        SELECT * FROM spezialization;
    '''

    query_find_all_perks = f'''
        SELECT * FROM perk
        WHERE perk_id NOT IN (
                SELECT perk_id FROM service
                WHERE account_id = to_regrole('{username}')
            );
    '''

    query_current_user_perks = f'''
        SELECT 
            perk.perk_name,
            service.price,
            service.description 
        FROM service
        JOIN perk
        ON perk.perk_id = service.perk_id
        WHERE account_id = to_regrole('{username}');
    '''

    all_specializations = query_executor(backend_connection, query_find_all_spezializations)
    all_perks = query_executor(backend_connection, query_find_all_perks)
    current_user_perks = query_executor(backend_connection, query_current_user_perks)

    form.specialization.choices = all_specializations

    if request.method == 'POST':

        query_add_perk = f'''
            CALL add_perk(
            {form.perk_id.data},
            {form.money.data}::MONEY,
            '{form.description.data}'::TEXT
            );
        '''
        try:
            query_executor(user_connections[username], query_add_perk)
        except Exception as e:
            log.debug(e)
        return redirect(url_for('perks'))

    return render_template('perks.html', form=form, current_user=session['account_model'],
                           perks=all_perks, current_user_perks=current_user_perks)


@app.route('/task-reports', methods=['GET', 'POST'])
def task_reports():
    return render_template("task_reports.html", current_user=session['account_model'])


@app.route('/review', methods=['GET', 'POST'])
def review():
    return render_template("review.html", current_user=session['account_model'])


@app.route('/create-task', methods=['GET', 'POST'])
def create_task():
    if 'username' not in session:
        return redirect(url_for('login'))

    username = session['username']

    if username not in user_connections.keys():
        return redirect(url_for('login'))

    if session['account_model']['role_id'] != 16499:
        abort(403)

    creation_form = CreationTaskForm()
    find_freelancer_form = FindFreelancerByPerkForm()

    # Запрос для получения всех специализаций
    query_find_all_spezializations = f'''
            SELECT * FROM spezialization;
        '''

    # Запрос для получения всех навыков
    query_find_all_perks = f'''
            SELECT * FROM perk
        '''

    perks = query_executor(backend_connection, query_find_all_perks)
    specializations = query_executor(backend_connection, query_find_all_spezializations)

    find_freelancer_form.specialization.choices = specializations

    if request.method == 'POST':
        if request.form['submit'] == 'Choose executor':
            print(request.form)
            query_find_suitable_freelancer = f'''
                SELECT
                    kek.account_id,
                    kek.user_first_name,
                    kek.user_last_name,
                    kek.last_seen_datetime,
                    service.perk_id,
                    service.price,
                    service.description
                FROM service
                JOIN (
                    SELECT * FROM account 
                    JOIN user_personal_data 
                    ON user_data_id = account_id
                ) AS kek
                ON kek.account_id = service.account_id
                WHERE perk_id = {find_freelancer_form.perk.data};
            '''

            services = query_executor(backend_connection, query_find_suitable_freelancer)
            return render_template("creation_task.html", current_user=session['account_model'],
                                   main_form=creation_form, second_form=find_freelancer_form,
                                   perks=perks, services=services)

        if request.form['submit'] == 'Create task':
            query_create_task = f'''
                CALL create_task(
                    {creation_form.id.data},
                    '{creation_form.description.data}'::TEXT,
                    {creation_form.executor.data},
                    '{creation_form.deadline.data}'::TIMESTAMP WITHOUT TIME ZONE
                );
            '''
            try:
                query_executor(user_connections[username], query_create_task)
                print(f'done {query_create_task}')
            except Exception as e:

                print(e)
            return redirect(url_for('index'))

    return render_template("creation_task.html", current_user=session['account_model'],
                           main_form=creation_form, second_form=find_freelancer_form,
                           perks=perks, services=[])



def query_executor(connection, query: str):
    with connection.cursor() as cursor:
        try:
            connection.autocommit = True
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


def my_render_template(template, *args: tuple, **kwargs):
    kwargs['session'] = session
    args = list(args)
    args.insert(0, template)
    return render_template(*args, **kwargs)
