import logging as log
from app import app, Config, errors
from app.forms import RegistrationForm, LoginForm, AddPerkForm
from app.models import UserModel, TaskModel, SpecializationModel

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
    if session['account_model']['role_id'] == 16498:
        if request.method == "POST":
            query = f'''
                CALL complete_task({request.form.get('task-select')});
            '''
            res = query_executor(user_connections[username], query)
            return redirect(url_for('index'))

        query = f'''
            SELECT *
            FROM current_user_tasks_information
        '''
        tasks_query = query_executor(user_connections[username], query)
        tasks_models = TaskModel.parse_from_query(tasks_query)

        return my_render_template('index.html', title='Home', tasks=list(tasks_models))
    else:
        return my_render_template('index.html', title='Home', tasks=[])


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

    return render_template('registration.html', title='Registration', form=form)


@app.route('/perks', methods=['GET', 'POST'])
def perks():
    if 'username' not in session:
        return redirect(url_for('login'))

    username = session['username']

    if username not in user_connections.keys():
        return redirect(url_for('login'))

    if session['account_model']['role_id'] != 16498:
        abort(403)

    form: AddPerkForm = AddPerkForm()
    print(user_connections)

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

    all_spezializations = query_executor(backend_connection, query_find_all_spezializations)
    all_perks = query_executor(backend_connection, query_find_all_perks)
    current_user_perks = query_executor(backend_connection, query_current_user_perks)

    form.specialization.choices = all_spezializations

    if request.method == 'POST':

        query_add_perk = f'''
            CALL add_perk(
            {form.perk_id.data},
            {form.money.data}::MONEY,
            '{form.description.data}'::TEXT
            );
        '''
        print(query_add_perk)
        try:
            query_executor(user_connections[username], query_add_perk)
        except Exception as e:
            print(e)

    return render_template('perks.html', form=form,  current_user=session['account_model'],
                           perks=all_perks, current_user_perks=current_user_perks)


@app.route('/create-review', methods=['GET', 'POST'])
def create_review():
    pass


@app.route('/check-review', methods=['GET', 'POST'])
def check_review():
    pass


@app.route('/create-tast', methods=['GET', 'POST'])
def create_task():
    if 'username' not in session:
        return redirect(url_for('login'))

    username = session['username']

    if username not in user_connections.keys():
        return redirect(url_for('login'))

    if session['account_model']['role_id'] != 16497:
        abort(403)

    print(session['account-model'])


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