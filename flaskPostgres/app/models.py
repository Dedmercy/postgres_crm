import copy
import datetime
import json
from dataclasses import dataclass

from app import db
from sqlalchemy.dialects.postgresql import TIMESTAMP, SMALLINT
from flask_login import UserMixin
# from app import login
from werkzeug.security import check_password_hash, generate_password_hash


# # Должности работников
# class Post(db.Model):
#     post_id = db.Column(db.INTEGER, primary_key=True, nullable=False)
#     post_name = db.Column(db.VARCHAR(), nullable=False)
#     employees = db.relationship('Employee', backref='employee_post', lazy='dynamic')
#
#     def __repr__(self):
#         return f'<Group role id:{self.post_id} name:{self.post_name}>'
#
#
# class Company(db.Model):
#     company_reg_num = db.Column(db.BIGINT, index=True, primary_key=True)
#     company_name = db.Column(db.VARCHAR(100), nullable=False)
#     work_status = db.Column(db.BOOLEAN, nullable=False)
#     company_post_index = db.Column(db.VARCHAR(20), nullable=False)
#     company_address = db.Column(db.TEXT, nullable=False)
#     contact_persons = db.relationship("ContactPerson", backref='company_contact_person', lazy='dynamic')
#
#     def __repr__(self):
#         return f'Company {self.company_name}'
#
#
# class ContactPerson(db.Model):
#     c_p_id = db.Column(db.INTEGER, index=True, primary_key=True)
#     c_p_phone_number = db.Column(db.BIGINT, nullable=False)
#     c_p_email = db.Column(db.VARCHAR(100), nullable=False)
#     c_p_first_name = db.Column(db.VARCHAR(50), nullable=False)
#     c_p_middle_name = db.Column(db.VARCHAR(50), nullable=False)
#     c_p_last_name = db.Column(db.VARCHAR(50), nullable=False)
#     company_reg_num = db.Column(db.BIGINT, db.ForeignKey('company.company_reg_num'))
#
#     def __init__(self):
#         pass
#
#     def __int__(self):
#         return f'Contact person\n' \
#                f' name:{self.c_p_first_name} last name:{self.c_p_last_name}'
#
#
# class Task(db.Model):
#     task_id = db.Column(db.INTEGER, index=True, primary_key=True)
#     task_decription = db.Column(db.TEXT, nullable=False)
#     task_create_datetime = db.Column(TIMESTAMP(timezone=False), nullable=False)
#     task_deadline_datetime = db.Column(TIMESTAMP(timezone=False), nullable=True)
#     c_p_id = db.Column(db.INTEGER, db.ForeignKey('contact_person.c_p_id'))
#     creator = db.Column(db.INTEGER, db.ForeignKey('employee.employee_id'))
#     executor = db.Column(db.INTEGER, db.ForeignKey('employee.employee_id'))
#
#     def __init__(self):
#         pass
#
#     def __int__(self):
#         return f'Task №{self.contract_num}'
#
#
# class Account(UserMixin, db.Model):
#     account_id = db.Column(db.INTEGER, primary_key=True, index=True)
#     login = db.Column(db.VARCHAR(12), nullable=False)
#     hash_password = db.Column(db.VARCHAR(256), nullable=False)
#     role_id = db.Column(db.INTEGER, db.ForeignKey('role.role_id'))
#     user_data_id = db.Column(db.INTEGER, db.ForeignKey('user_personal_data.user_data_id'))
#     account_registration_date = db.Column(db.DATE, nullable=False)
#     last_seen_datetime = db.Column(db.TIMESTAMP, nullable=False)
#
#     def get_id(self):
#         return str(self.employee_id)
#
#     #
#     # def set_password(self, password):
#     #     self.e_password = generate_password_hash(password)
#     #
#     # def check_password(self, password):
#     #     return check_password_hash(self.e_password, password)
#
#     def __repr__(self):
#         return f'Employee name:{self.e_first_name},  last name:{self.e_last_name}'
#
#
# # @login.user_loader
# # def load_user(employee_id):
# #     return Account.query.get(int(employee_id))
#
#
# class Contract(db.Model):
#     contract_num = db.Column(db.BIGINT, index=True, primary_key=True)
#     contract_description = db.Column(db.TEXT, nullable=True)
#     goods = db.relationship("Goods", backref='goods_contract', lazy='dynamic')
#
#     def __init__(self):
#         pass
#
#     def __repr__(self):
#         return f'Contract №{self.contract_num}'
#
#
# class Goods(db.Model):
#     goods_num = db.Column(db.INTEGER, index=True, primary_key=True)
#     goods_name = db.Column(db.VARCHAR(100), nullable=False)
#     goods_description = db.Column(db.TEXT, nullable=False)
#     contract_num = db.Column(db.BIGINT, db.ForeignKey('contract.contract_num'))
#
#     def __init__(self):
#         pass
#
#     def __repr__(self):
#         return f'Good №{self.goods_num}\n' \
#                f'name:{self.goods_name}'
#
#
# class GoodsTask(db.Model):
#     task_id = db.Column(db.INTEGER, db.ForeignKey('task.task_id'), index=True, primary_key=True)
#     goods_num = db.Column(db.INTEGER, db.ForeignKey('goods.goods_num'), index=True, primary_key=True)
#     remark = db.Column(db.VARCHAR, nullable=True)
#
#
# class TaskStatus(db.Model):
#     task_id = db.Column(db.INTEGER, db.ForeignKey('task.task_id'), index=True, primary_key=True)
#     task_status_name = db.Column(db.VARCHAR(50), nullable=False)
#     task_completed_datetime = db.Column(TIMESTAMP(timezone=False), nullable=True)
#     task_priority = db.Column(SMALLINT, nullable=False)
#
#     def __repr__(self):
#         return f'Status for Task№{self.contract_num}\n' \
#                f'name: {self.task_status_name}\n' \
#                f'priority: {self.task_priority}\n' \
#                f'deadline: {self.task_completed_datetime}'


@dataclass
class UserModel:
    id: int
    username: str
    hash_password: str
    role_id: int
    user_data_id: int
    registration_date: datetime.datetime
    last_seen: datetime.datetime
    first_name: str
    middle_name: str
    last_name: str
    email: str
    number: int

    @classmethod
    def parse_from_query(cls, request_query: list) -> list:
        user_list = []
        for v in request_query:
            id_: int = v[0]
            username: str = v[1]
            hash_password: str = v[2]
            role_id: int = v[3]
            user_data_id: int = v[4]
            registration_date: datetime.datetime = v[5]
            last_seen: datetime.datetime = v[6]
            first_name: str = v[8]
            middle_name: str = v[9]
            last_name: str = v[10]
            email: str = v[11]
            number: int = v[12]

            user_model = UserModel(id_,
                                   username,
                                   hash_password,
                                   role_id,
                                   user_data_id,
                                   registration_date,
                                   last_seen,
                                   first_name,
                                   middle_name,
                                   last_name,
                                   email,
                                   number)

            user_list.append(user_model)
        return user_list

    def to_simple_formats(self):
        dict_to_json = copy.copy(self.__dict__)
        dict_to_json['registration_date'] = dict_to_json['registration_date'].strftime('%Y-%m-%d %H:%M:%S')
        dict_to_json['last_seen'] = dict_to_json['last_seen'].strftime('%Y-%m-%d %H:%M:%S')
        # return json.dumps(dict_to_json)
        return dict_to_json

    @classmethod
    # def from_json(cls, json_str):
    def from_simple_formats(cls, params_dict):
        # params_dict = json.loads(json_str)

        params_dict['registration_date'] = datetime.datetime.strptime(params_dict['registration_date'],
                                                                      '%Y-%m-%d %H:%M:%S')
        params_dict['last_seen'] = datetime.datetime.strptime(params_dict['last_seen'],
                                                              '%Y-%m-%d %H:%M:%S')

        user_model = UserModel(**params_dict)
        return user_model


@dataclass
class TaskModel:
    id: int
    description: str
    client: int
    creation_date: datetime.datetime
    deadline_date: datetime.datetime
    status: str
    complete_date: datetime.datetime | None

    @classmethod
    def parse_from_query(cls, request_query: list) -> list:
        task_list = []
        for v in request_query:
            id_: int = v[0]
            description: str = v[1]
            client: int = v[2]
            creation_date: datetime.datetime = v[3]
            deadline_date: datetime.datetime = v[4]
            status: str = v[5]
            complete_date: datetime.datetime | None = v[6]

            task_model = TaskModel(id_,
                                   description,
                                   client,
                                   creation_date,
                                   deadline_date,
                                   status,
                                   complete_date)

            task_list.append(task_model)
        return task_list

    def to_json(self):
        return json.dumps(self.__dict__)

    @classmethod
    def from_json(cls, json_str):
        params_dict = json.loads(json_str)
        task_model = TaskModel(**params_dict)
        return task_model
