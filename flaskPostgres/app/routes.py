import logging as log

import psycopg2
from flask import render_template, redirect, url_for, flash, request, session, abort
from psycopg2.extensions import connection as psycopg_connection
from sqlalchemy.exc import OperationalError
from werkzeug import Response

from app import app, Config
from app.forms import RegistrationForm, LoginForm, AddPerkForm, CreationTaskForm, FindFreelancerByPerkForm,\
    AddReviewForm, ReportsForm, CreateEditingForm
from app.models import UserModel, TaskModel, ReviewModel, EditingModel

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
    logged_flag, username, response = check_user_logged()
    if logged_flag:
        return response

    query = ''

    # Если пользователь фрилансер
    if session['account_model']['role'] == 'freelancer':
        if request.method == "POST":
            task_id = request.form.get('task-select')
            query = f'''
                CALL complete_task(%s);
            '''
            res = query_executor(user_connections[username], query, (task_id,))
            return redirect(url_for('index'))

        query = f'''
            SELECT *
            FROM current_freelancer_tasks_information
        '''

    # Если пользователь заказчик
    elif session['account_model']['role_id'] == 'client':
        query = f'''
                    SELECT *
                    FROM current_client_tasks_information
                '''

    tasks_query = query_executor(user_connections[username], query, ())
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

        username = form.username.data

        # проверяет наличие юзера с таким логином
        query_find_user_by_login = f'''
            SELECT *
            FROM account
            WHERE login = %s
        '''

        res = query_executor(backend_connection, query_find_user_by_login, (username,))
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
                SELECT                 
                    acc.account_id,
                    acc.login,
                    acc.hash_password ,
                    acc.role_id ,
                    acc.account_registration_date ,
                    acc.last_seen_datetime,
                    upd.user_first_name,
                    upd.user_middle_name,
                    upd.user_last_name,
                    upd.user_email ,
                    upd.user_phone ,
                    rl.role_name
                FROM account as acc
                JOIN user_personal_data as upd
                ON acc.account_id = upd.user_data_id
                JOIN role as rl
                ON acc.role_id = rl.role_id
                WHERE acc.account_id = to_regrole('{username}');
            '''

            # сохраняет в куки
            account_info = query_executor(backend_connection, query_account_info, ())
            account_model: UserModel = UserModel.parse_from_query(account_info)[0]
            session['account_model'] = account_model.to_simple_formats()
            session.modified = True
        except OperationalError as e:
            log.debug(f'[{method_prefix}] Invalid username or password')
            flash('Invalid username or password')
            return redirect(url_for('login'))
        except Exception as e:
            flash(str(e))
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

        form_params = (form.first_name.data,
                       form.middle_name.data,
                       form.last_name.data,
                       form.email.data,
                       form.phone.data,
                       form.username.data,
                       form.password.data,
                       form.post.data)

        registration_query = f'''
            CALL create_user(%s, %s, %s, %s, %s, %s, %s, %s);
        '''
        try:
            log.debug(f'{log_prefix} try to {registration_query}')
            query_executor(backend_connection, registration_query, form_params)
        except Exception as e:
            log.debug(e)

        return redirect(url_for('index'))

    return render_template('registration.html', title='Registration', form=form, current_user={})


@app.route('/perks', methods=['GET', 'POST'])
def perks():
    logged_flag, username, response = check_user_logged()
    if logged_flag:
        return response

    if session['account_model']['role'] != 'freelancer':
        abort(403)

    form: AddPerkForm = AddPerkForm()

    query_find_all_spezializations = f'''
        SELECT * FROM spezialization;
    '''

    query_find_all_perks = f'''
        SELECT * FROM perk
        WHERE perk_id NOT IN (
                SELECT perk_id FROM service
                WHERE account_id = to_regrole(%s)
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
        WHERE account_id = to_regrole(%s);
    '''

    all_specializations = query_executor(backend_connection, query_find_all_spezializations, ())
    all_perks = query_executor(backend_connection, query_find_all_perks, (username,))
    current_user_perks = query_executor(backend_connection, query_current_user_perks, (username,))

    form.specialization.choices = all_specializations

    if request.method == 'POST':

        query_add_perk = f'''
            CALL add_perk(
            %s,
            %s::MONEY,
            %s::TEXT
            );
        '''
        perk_data = (form.perk_id.data,
                     form.money.data,
                     form.description.data)
        try:
            query_executor(user_connections[username], query_add_perk, perk_data)
        except Exception as e:
            log.debug(e)
        return redirect(url_for('perks'))

    return render_template('perks.html', form=form, current_user=session['account_model'],
                           perks=all_perks, current_user_perks=current_user_perks)


@app.route('/check-task-editing', methods=['GET', 'POST'])
def check_task_editing():
    logged_flag, username, response = check_user_logged()
    if logged_flag:
        return response

    form = ReportsForm()

    if session['account_model']['role'] != 'freelancer':
        abort(403)

    task_query = '''
        SELECT 
            task.task_id,
            task.task_description,
            task.task_creating_datetime,
            task.task_deadline_datetime
        FROM task
        JOIN task_status
        ON task_status.task_id = task.task_id
        WHERE 
            task_status = 'NEW'
            AND
            executor = %s
    '''
    task_query_params = (session['account_model']['account_id'], )
    print(task_query_params)
    tasks = query_executor(backend_connection, task_query, task_query_params)
    print(tasks)
    if tasks:
        form.task.choices = [(item[0], item[1]) for item in tasks]

    if request.method == 'POST':
        editing_query = '''
            SELECT 
                editing_num,
                editing_header,
                editing_text,
                editing_date
            FROM editing
            WHERE task_id = %s
        '''
        editing_query_params = (form.task.data, )
        editing = query_executor(backend_connection, editing_query, editing_query_params)
        editing_models = EditingModel.parse_from_query(editing)
        print(editing_models)
        return parametrized_render_template("show-task-editing.html", tasks=tasks, form=form,
                                            editing_models=editing_models)

    return parametrized_render_template("show-task-editing.html", tasks=tasks, form=form, editing_models=[])


@app.route('/create-task-editing', methods=['GET', 'POST'])
def create_task_editing():
    logged_flag, username, response = check_user_logged()
    if logged_flag:
        return response

    form = CreateEditingForm()

    if session['account_model']['role'] != 'client':
        abort(403)

    task_query = '''
        SELECT 
            task.task_id,
            task.task_description
        FROM task
        JOIN task_status
        ON task_status.task_id = task.task_id
        WHERE 
            task_status = 'NEW'
            AND
            client = %s
    '''
    task_query_params = (session['account_model']['account_id'], )
    tasks = query_executor(backend_connection, task_query, task_query_params)

    form.task.choices = tasks

    if request.method == 'POST':
        create_editing_query = '''
            CALL add_editing(%s::INTEGER, %s::INTEGER, %s::VARCHAR, %s::TEXT);
        '''

        create_editing_query_params = (
            int(form.task.data),
            form.num.data,
            form.header.data,
            form.text.data
        )
        try:
            query_executor(user_connections[username], create_editing_query, create_editing_query_params)
        except Exception as e:
            print(e)
        return redirect(url_for('index'))

    return parametrized_render_template('create-task-editing.html', form=form)


@app.route('/create-review/<user_id>', methods=['GET', 'POST'])
def create_review(user_id):
    logged_flag, username, response = check_user_logged()
    if logged_flag:
        return response

    # если была заполнена форма, то проверяет форму
    form = AddReviewForm()
    if form.validate_on_submit():
        review_header = form.review_header.data
        review_text = form.review_text.data
        review_mark = form.review_mark.data

        query_create_review = '''create_review (%s,%s,%s,%s,%s,%s)'''

        query_review_num = '''
        select count(*)
        from review
        where account_id = %s;'''

        count_reviews = query_executor(user_connections[username], query_review_num, (user_id,))
        count_reviews_int = count_reviews[0][0]

        params = (user_id,
                  count_reviews_int,
                  review_header,
                  review_text,
                  review_mark,
                  session['account_model'].account_id)

        query_executor(user_connections[username], query_create_review, params)

        return redirect(url_for(f'/check-review/{user_id}'))

    return parametrized_render_template('create_review.html')


@app.route('/check-review/<user_id>', methods=['GET', 'POST'])
def check_review(user_id):
    logged_flag, username, response = check_user_logged()
    if logged_flag:
        return response

    if request.method == "POST":
        return redirect(url_for(f'/create-review/{user_id}'))

    query = f'''
        SELECT *
        FROM watch_reviews(%s)
    '''
    reviews_query = query_executor(user_connections[username], query, (user_id,))
    reviews_models = ReviewModel.parse_from_query(reviews_query)

    return parametrized_render_template('reviews.html', title='Home', reviews=list(reviews_models))


@app.route('/create-task', methods=['GET', 'POST'])
def create_task():
    if 'username' not in session:
        return redirect(url_for('login'))

    username = session['username']

    if username not in user_connections.keys():
        return redirect(url_for('login'))

    if session['account_model']['role'] != 'client':
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

    perks = query_executor(backend_connection, query_find_all_perks, ())
    specializations = query_executor(backend_connection, query_find_all_spezializations, ())

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
                WHERE perk_id = %s;
            '''

            services = query_executor(backend_connection, query_find_suitable_freelancer,
                                      (find_freelancer_form.perk.data,))
            return render_template("creation_task.html", current_user=session['account_model'],
                                   main_form=creation_form, second_form=find_freelancer_form,
                                   perks=perks, services=services)

        if request.form['submit'] == 'Create task':
            query_create_task = f'''
                CALL create_task(
                    %s,
                    %s::TEXT,
                    %s,
                    %s::TIMESTAMP WITHOUT TIME ZONE
                );
            '''
            params = (creation_form.id.data, creation_form.description.data, creation_form.executor.data,
                      creation_form.deadline.data)

            try:
                query_executor(user_connections[username], query_create_task, params)
                print(f'done {query_create_task}')
            except Exception as e:

                print(e)
            return redirect(url_for('index'))

    return render_template("creation_task.html", current_user=session['account_model'],
                           main_form=creation_form, second_form=find_freelancer_form,
                           perks=perks, services=[])


def query_executor(connection, query: str, params: tuple):
    with connection.cursor() as cursor:
        try:
            connection.autocommit = True
            cursor.execute(query, params)
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


def parametrized_render_template(template, *args: tuple, **kwargs):
    kwargs['session'] = session
    kwargs['current_user'] = session['account_model']
    args = list(args)
    args.insert(0, template)
    return render_template(*args, **kwargs)


def check_user_logged() -> (bool, str, Response):
    if 'username' not in session:
        return True, None, redirect(url_for('login'))

    username = session['username']

    if username not in user_connections.keys():
        return True, None, redirect(url_for('login'))

    return False, username, None
