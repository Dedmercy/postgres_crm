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
    registration_date: datetime.date
    last_seen: datetime.datetime
    first_name: str
    middle_name: str
    last_name: str
    email: str
    number: int
    role: str
    second_auth: bool
    profile_image: str

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
            first_name: str = v[6]
            middle_name: str = v[7]
            last_name: str = v[8]
            email: str = v[9]
            number: int = v[10]
            role: str = v[11]
            second_auth: bool = v[12]
            profile_image: str = v[13]

            user_model = UserModel(account_id,
                                   username,
                                   hash_password,
                                   role_id,
                                   registration_date,
                                   last_seen,
                                   first_name,
                                   middle_name,
                                   last_name,
                                   email,
                                   number,
                                   role,
                                   second_auth,
                                   profile_image)

            user_list.append(user_model)
        return user_list

    def to_simple_formats(self):
        dict_to_json = copy.copy(self.__dict__)
        dict_to_json['registration_date'] = dict_to_json['registration_date'].strftime('%Y-%m-%d %H:%M:%S')
        dict_to_json['last_seen'] = dict_to_json['last_seen'].strftime('%Y-%m-%d %H:%M:%S')
        # return json.dumps(dict_to_json)
        return dict_to_json

    @classmethod
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
    login: str

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
            client_login: str = v[7]

            task_model = TaskModel(id_,
                                   description,
                                   client,
                                   creation_date,
                                   deadline_date,
                                   status,
                                   complete_date,
                                   client_login)

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
class ReviewModel:
    id: int
    num: int
    header: str
    text: str
    mark: int
    author: int
    login: str
    profile_image: str
    first_name: str
    last_name: str
    middle_name: str

    @classmethod
    def parse_from_query(cls, request_query: list) -> list:
        review_list = []
        for v in request_query:
            id_: int = v[0]
            num: int = v[1]
            header: str = v[2]
            text: str = v[3]
            mark: int = v[4]
            author: int = v[5]
            login: str = v[6]
            profile_image: str = v[7]
            first_name: str = v[8]
            last_name: str = v[9]
            middle_name: str = v[10]

            review_model = ReviewModel(id_,
                                       num,
                                       header,
                                       text,
                                       mark,
                                       author,
                                       login,
                                       profile_image,
                                       first_name,
                                       last_name,
                                       middle_name
                                       )

            review_list.append(review_model)
        return review_list

    def to_json(self):
        return json.dumps(self.__dict__)

    @classmethod
    def from_json(cls, json_str):
        params_dict = json.loads(json_str)
        review_model = ReviewModel(**params_dict)
        return review_model


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


@dataclass
class EditingModel:
    num: int
    header: str
    text: str
    creation_datetime: datetime.datetime

    @classmethod
    def parse_from_query(cls, request_query: list):
        editing_list = []
        for item in request_query:
            num: int = item[0]
            header: str = item[1]
            text: str = item[2]
            creation_datetime: datetime.datetime = item[3]
            editing_model = EditingModel(
                num,
                header,
                text,
                creation_datetime
            )
            editing_list.append(editing_model)
        return editing_list


@dataclass
class ServiceModel:
    id: int
    first_name: str
    last_name: str
    last_seen_datetime: int
    perk_id: int
    price: int
    description: str
    login: str

    @classmethod
    def parse_from_query(cls, request_query: list) -> list:
        service_list = []
        for item in request_query:
            account_id: int = item[0]
            user_first_name: str = item[1]
            user_last_name: str = item[2]
            last_seen_datetime: int = item[3]
            perk_id: int = item[4]
            price: int = item[5]
            description: str = item[6]
            login: str = item[7]

            service_model = ServiceModel(
                account_id,
                user_first_name,
                user_last_name,
                last_seen_datetime,
                perk_id,
                price,
                description,
                login
            )

            service_list.append(service_model)
        return service_list
