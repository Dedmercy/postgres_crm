import copy
import datetime
import json
from dataclasses import dataclass


@dataclass
class UserModel:
    account_id: int
    username: str
    hash_password: str
    role_id: int
    registration_date: datetime.datetime
    last_seen: datetime.datetime
    user_data_id: int
    first_name: str
    middle_name: str
    last_name: str
    email: str
    number: int

    @classmethod
    def parse_from_query(cls, request_query: list) -> list:
        user_list = []
        print(request_query)
        for v in request_query:
            account_id: int = v[0]
            username: str = v[1]
            hash_password: str = v[2]
            role_id: int = v[3]
            registration_date: datetime.datetime = v[4]
            last_seen: datetime.datetime = v[5]
            user_data_id: int = v[6]
            first_name: str = v[7]
            middle_name: str = v[8]
            last_name: str = v[9]
            email: str = v[10]
            number: int = v[11]

            user_model = UserModel(account_id,
                                   username,
                                   hash_password,
                                   role_id,
                                   registration_date,
                                   last_seen,
                                   user_data_id,
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


@dataclass
class SpecializationModel:
    sp_id: int
    sp_name: str

    @classmethod
    def parse_from_query(cls, request_query: list) -> list:
        task_list = []
        for item in request_query:
            id: int = item[0]
            name: str = item[1]

            specialization_model = SpecializationModel(
                id,
                name
            )
            task_list.append(specialization_model)
        return task_list
