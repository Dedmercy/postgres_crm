from app import db
from sqlalchemy.dialects.postgresql import TIMESTAMP, SMALLINT
from flask_login import UserMixin
# from app import login
from werkzeug.security import check_password_hash, generate_password_hash


# Должности работников
class Post(db.Model):
    post_id = db.Column(db.INTEGER, primary_key=True, nullable=False)
    post_name = db.Column(db.VARCHAR(), nullable=False)
    employees = db.relationship('Employee', backref='employee_post', lazy='dynamic')

    def __repr__(self):
        return f'<Group role id:{self.post_id} name:{self.post_name}>'


class Company(db.Model):
    company_reg_num = db.Column(db.BIGINT, index=True, primary_key=True)
    company_name = db.Column(db.VARCHAR(100), nullable=False)
    work_status = db.Column(db.BOOLEAN, nullable=False)
    company_post_index = db.Column(db.VARCHAR(20), nullable=False)
    company_address = db.Column(db.TEXT, nullable=False)
    contact_persons = db.relationship("ContactPerson", backref='company_contact_person', lazy='dynamic')

    def __repr__(self):
        return f'Company {self.company_name}'


class ContactPerson(db.Model):
    c_p_id = db.Column(db.INTEGER, index=True, primary_key=True)
    c_p_phone_number = db.Column(db.BIGINT, nullable=False)
    c_p_email = db.Column(db.VARCHAR(100), nullable=False)
    c_p_first_name = db.Column(db.VARCHAR(50), nullable=False)
    c_p_middle_name = db.Column(db.VARCHAR(50), nullable=False)
    c_p_last_name = db.Column(db.VARCHAR(50), nullable=False)
    company_reg_num = db.Column(db.BIGINT, db.ForeignKey('company.company_reg_num'))

    def __init__(self):
        pass

    def __int__(self):
        return f'Contact person\n' \
               f' name:{self.c_p_first_name} last name:{self.c_p_last_name}'


class Task(db.Model):
    task_id = db.Column(db.INTEGER, index=True, primary_key=True)
    task_decription = db.Column(db.TEXT, nullable=False)
    task_create_datetime = db.Column(TIMESTAMP(timezone=False), nullable=False)
    task_deadline_datetime = db.Column(TIMESTAMP(timezone=False), nullable=True)
    c_p_id = db.Column(db.INTEGER, db.ForeignKey('contact_person.c_p_id'))
    creator = db.Column(db.INTEGER, db.ForeignKey('employee.employee_id'))
    executor = db.Column(db.INTEGER, db.ForeignKey('employee.employee_id'))

    def __init__(self):
        pass

    def __int__(self):
        return f'Task №{self.contract_num}'


class Account(UserMixin, db.Model):
    account_id = db.Column(db.INTEGER, primary_key=True, index=True)
    login = db.Column(db.VARCHAR(12), nullable=False)
    hash_password = db.Column(db.VARCHAR(256), nullable=False)
    role_id = db.Column(db.INTEGER, db.ForeignKey('role.role_id'))
    user_data_id  = db.Column(db.INTEGER, db.ForeignKey('user_personal_data.user_data_id'))
    account_registration_date = db.Column(db.DATE, nullable=False)
    last_seen_datetime = db.Column(db.TIMESTAMP, nullable=False)

    def get_id(self):
        return str(self.employee_id)
    #
    # def set_password(self, password):
    #     self.e_password = generate_password_hash(password)
    #
    # def check_password(self, password):
    #     return check_password_hash(self.e_password, password)

    def __repr__(self):
        return f'Employee name:{self.e_first_name},  last name:{self.e_last_name}'


# @login.user_loader
# def load_user(employee_id):
#     return Account.query.get(int(employee_id))


class Contract(db.Model):
    contract_num = db.Column(db.BIGINT, index=True, primary_key=True)
    contract_description = db.Column(db.TEXT, nullable=True)
    goods = db.relationship("Goods", backref='goods_contract', lazy='dynamic')

    def __init__(self):
        pass

    def __repr__(self):
        return f'Contract №{self.contract_num}'


class Goods(db.Model):
    goods_num = db.Column(db.INTEGER, index=True, primary_key=True)
    goods_name = db.Column(db.VARCHAR(100), nullable=False)
    goods_description = db.Column(db.TEXT, nullable=False)
    contract_num = db.Column(db.BIGINT, db.ForeignKey('contract.contract_num'))

    def __init__(self):
        pass

    def __repr__(self):
        return f'Good №{self.goods_num}\n' \
               f'name:{self.goods_name}'


class GoodsTask(db.Model):
    task_id = db.Column(db.INTEGER, db.ForeignKey('task.task_id'), index=True, primary_key=True)
    goods_num = db.Column(db.INTEGER, db.ForeignKey('goods.goods_num'), index=True, primary_key=True)
    remark = db.Column(db.VARCHAR, nullable=True)


class TaskStatus(db.Model):
    task_id = db.Column(db.INTEGER, db.ForeignKey('task.task_id'), index=True, primary_key=True)
    task_status_name = db.Column(db.VARCHAR(50), nullable=False)
    task_completed_datetime = db.Column(TIMESTAMP(timezone=False), nullable=True)
    task_priority = db.Column(SMALLINT, nullable=False)

    def __repr__(self):
        return f'Status for Task№{self.contract_num}\n' \
               f'name: {self.task_status_name}\n' \
               f'priority: {self.task_priority}\n' \
               f'deadline: {self.task_completed_datetime}'
