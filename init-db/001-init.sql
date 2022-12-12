
/* Drop Tables */

DROP TABLE IF EXISTS Review;
DROP TABLE IF EXISTS Service;
DROP TABLE IF EXISTS Editing;
DROP TABLE IF EXISTS Task_status;
DROP TABLE IF EXISTS Task;
DROP TABLE IF EXISTS Account;
DROP TABLE IF EXISTS Perk;
DROP TABLE IF EXISTS Role;
DROP TABLE IF EXISTS Spezialization;
DROP TABLE IF EXISTS User_Personal_Data;




/* Create Tables */

-- Таблица для хранения данных учетных записей.
CREATE TABLE Account
(
	-- Идентификационный номер аккаунта
	account_id int NOT NULL,
	-- Логин учетной записи.
	login varchar(12) NOT NULL UNIQUE,
	-- Захешированный пароль
	hash_password varchar(256) NOT NULL,
	-- Идентификатор роли
	role_id int NOT NULL,
	-- Идентификационный номер пользователя
	user_data_id  int NOT NULL,
	-- Дата регистрации
	-- 
	account_registration_date date NOT NULL,
	-- Дата и время последнего входа в систему.
	last_seen_datetime timestamp,
	-- Является ли аккаунт исполнителем или клиентом.
	is_executor boolean NOT NULL,
	PRIMARY KEY (account_id)
) WITHOUT OIDS;


CREATE TABLE Editing
(
	-- Идентификатор задания
	task_id int NOT NULL,
	-- Идентификатор правки
	editing_num int NOT NULL,
	-- Заголовок правки
	editing_header varchar(50) NOT NULL,
	-- Комментарий к правке
	editing_text text NOT NULL,
	-- Дата правки
	editing_date timestamp NOT NULL,
	PRIMARY KEY (task_id, editing_num)
) WITHOUT OIDS;


-- Таблица, хранящая данные о навыках.
CREATE TABLE Perk
(
	-- Идентификатор навыка
	perk_id int NOT NULL,
	-- Название навыка
	perk_name varchar(50) NOT NULL UNIQUE,
	-- Идентификатор специализации
	sp_id int NOT NULL,
	PRIMARY KEY (perk_id)
) WITHOUT OIDS;


-- Таблица, хранящая данные об отзывах на пользователей.
CREATE TABLE Review
(
	-- Идентификационный номер аккаунта
	account_id int NOT NULL,
	-- Идентификационный номер отзыва
	review_num int NOT NULL,
	-- Заголовок отзыва
	review_header varchar(25),
	-- Содержание отзыва
	review_text text,
	-- Оценка. (От 1 до 10).
	review_mark smallint NOT NULL,
	PRIMARY KEY (account_id, review_num)
) WITHOUT OIDS;


-- Таблица, хранящая данные о групповых ролях.
CREATE TABLE Role
(
	-- Идентификатор роли
	role_id int NOT NULL,
	-- Наименование роли
	role_name varchar(20) NOT NULL,
	PRIMARY KEY (role_id)
) WITHOUT OIDS;


-- Таблица, хранящая данные о том, какие пользователи предостовляют некоторые услуги.
CREATE TABLE Service
(
	-- Идентификатор навыка
	perk_id int NOT NULL,
	-- Идентификационный номер аккаунта
	account_id int NOT NULL,
	-- Цена за услугу
	-- 
	price money NOT NULL,
	-- Дополнительная информация
	description text
) WITHOUT OIDS;


-- Таблица, хранящая данные о направлениях предлагаемых услуг.
CREATE TABLE Spezialization
(
	-- Идентификатор специализации
	sp_id int NOT NULL,
	-- Наименование специализации
	sp_name varchar(50) NOT NULL UNIQUE,
	PRIMARY KEY (sp_id)
) WITHOUT OIDS;


-- Таблица, хранящая данные о оформленных заданиях.
CREATE TABLE Task
(
	-- Идентификатор задания
	task_id int NOT NULL,
	-- Описания задания
	task_description text,
	-- Идентификационный номер аккаунта исполнителя.
	executor int NOT NULL,
	-- Идентификационный номер аккаунта клиента.
	client int NOT NULL,
	-- Время создания задания
	task_creating_datetime timestamp NOT NULL,
	-- Время дедлайна задания
	task_deadline_datetime timestamp NOT NULL,
	PRIMARY KEY (task_id)
) WITHOUT OIDS;


-- Таблица, хранящая данные о статусе заданий
CREATE TABLE Task_status
(
	-- Идентификатор задания
	task_id int NOT NULL,
	-- Время и дата, когда задание стало выполненным задания.
	task_complete_datetime timestamp,
	-- Статус задания (NEW - новый, DONE - выполненный)
	task_status varchar(4) NOT NULL,
	PRIMARY KEY (task_id)
) WITHOUT OIDS;


-- Таблица, хранящая личные данные пользователя
CREATE TABLE User_Personal_Data
(
	-- Идентификационный номер пользователя
	user_data_id  int NOT NULL,
	-- Имя пользователя
	user_first_name varchar(50) NOT NULL,
	-- Отчество/Второе имя. (Если есть)
	user_middle_name varchar(50),
	-- Фамилия пользователя
	user_last_name varchar(50) NOT NULL,
	user_email varchar(50) NOT NULL,
	-- Номер телефона
	user_phone bigint NOT NULL,
	PRIMARY KEY (user_data_id )
) WITHOUT OIDS;



/* Create Foreign Keys */

ALTER TABLE Review
	ADD FOREIGN KEY (account_id)
	REFERENCES Account (account_id)
	ON UPDATE RESTRICT
	ON DELETE RESTRICT
;


ALTER TABLE Service
	ADD FOREIGN KEY (account_id)
	REFERENCES Account (account_id)
	ON UPDATE RESTRICT
	ON DELETE RESTRICT
;


ALTER TABLE Task
	ADD FOREIGN KEY (executor)
	REFERENCES Account (account_id)
	ON UPDATE RESTRICT
	ON DELETE RESTRICT
;


ALTER TABLE Task
	ADD FOREIGN KEY (client)
	REFERENCES Account (account_id)
	ON UPDATE RESTRICT
	ON DELETE RESTRICT
;


ALTER TABLE Service
	ADD FOREIGN KEY (perk_id)
	REFERENCES Perk (perk_id)
	ON UPDATE RESTRICT
	ON DELETE RESTRICT
;


ALTER TABLE Account
	ADD FOREIGN KEY (role_id)
	REFERENCES Role (role_id)
	ON UPDATE RESTRICT
	ON DELETE RESTRICT
;


ALTER TABLE Perk
	ADD FOREIGN KEY (sp_id)
	REFERENCES Spezialization (sp_id)
	ON UPDATE RESTRICT
	ON DELETE RESTRICT
;


ALTER TABLE Editing
	ADD FOREIGN KEY (task_id)
	REFERENCES Task (task_id)
	ON UPDATE RESTRICT
	ON DELETE RESTRICT
;


ALTER TABLE Task_status
	ADD FOREIGN KEY (task_id)
	REFERENCES Task (task_id)
	ON UPDATE RESTRICT
	ON DELETE RESTRICT
;


ALTER TABLE Account
	ADD FOREIGN KEY (user_data_id )
	REFERENCES User_Personal_Data (user_data_id )
	ON UPDATE RESTRICT
	ON DELETE RESTRICT
;



/* Comments */

COMMENT ON TABLE Account IS 'Таблица для хранения данных учетных записей.';
COMMENT ON COLUMN Account.account_id IS 'Идентификационный номер аккаунта';
COMMENT ON COLUMN Account.login IS 'Логин учетной записи.';
COMMENT ON COLUMN Account.hash_password IS 'Захешированный пароль';
COMMENT ON COLUMN Account.role_id IS 'Идентификатор роли';
COMMENT ON COLUMN Account.user_data_id  IS 'Идентификационный номер пользователя';
COMMENT ON COLUMN Account.account_registration_date IS 'Дата регистрации
';
COMMENT ON COLUMN Account.last_seen_datetime IS 'Дата и время последнего входа в систему.';
COMMENT ON COLUMN Account.is_executor IS 'Является ли аккаунт исполнителем или клиентом.';
COMMENT ON COLUMN Editing.task_id IS 'Идентификатор задания';
COMMENT ON COLUMN Editing.editing_num IS 'Идентификатор правки';
COMMENT ON COLUMN Editing.editing_header IS 'Заголовок правки';
COMMENT ON COLUMN Editing.editing_text IS 'Комментарий к правке';
COMMENT ON COLUMN Editing.editing_date IS 'Дата правки';
COMMENT ON TABLE Perk IS 'Таблица, хранящая данные о навыках.';
COMMENT ON COLUMN Perk.perk_id IS 'Идентификатор навыка';
COMMENT ON COLUMN Perk.perk_name IS 'Название навыка';
COMMENT ON COLUMN Perk.sp_id IS 'Идентификатор специализации';
COMMENT ON TABLE Review IS 'Таблица, хранящая данные об отзывах на пользователей.';
COMMENT ON COLUMN Review.account_id IS 'Идентификационный номер аккаунта';
COMMENT ON COLUMN Review.review_num IS 'Идентификационный номер отзыва';
COMMENT ON COLUMN Review.review_header IS 'Заголовок отзыва';
COMMENT ON COLUMN Review.review_text IS 'Содержание отзыва';
COMMENT ON COLUMN Review.review_mark IS 'Оценка. (От 1 до 10).';
COMMENT ON TABLE Role IS 'Таблица, хранящая данные о групповых ролях.';
COMMENT ON COLUMN Role.role_id IS 'Идентификатор роли';
COMMENT ON COLUMN Role.role_name IS 'Наименование роли';
COMMENT ON TABLE Service IS 'Таблица, хранящая данные о том, какие пользователи предостовляют некоторые услуги.';
COMMENT ON COLUMN Service.perk_id IS 'Идентификатор навыка';
COMMENT ON COLUMN Service.account_id IS 'Идентификационный номер аккаунта';
COMMENT ON COLUMN Service.price IS 'Цена за услугу
';
COMMENT ON COLUMN Service.description IS 'Дополнительная информация';
COMMENT ON TABLE Spezialization IS 'Таблица, хранящая данные о направлениях предлагаемых услуг.';
COMMENT ON COLUMN Spezialization.sp_id IS 'Идентификатор специализации';
COMMENT ON COLUMN Spezialization.sp_name IS 'Наименование специализации';
COMMENT ON TABLE Task IS 'Таблица, хранящая данные о оформленных заданиях.';
COMMENT ON COLUMN Task.task_id IS 'Идентификатор задания';
COMMENT ON COLUMN Task.task_description IS 'Описания задания';
COMMENT ON COLUMN Task.executor IS 'Идентификационный номер аккаунта исполнителя.';
COMMENT ON COLUMN Task.client IS 'Идентификационный номер аккаунта клиента.';
COMMENT ON COLUMN Task.task_creating_datetime IS 'Время создания задания';
COMMENT ON COLUMN Task.task_deadline_datetime IS 'Время дедлайна задания';
COMMENT ON TABLE Task_status IS 'Таблица, хранящая данные о статусе заданий';
COMMENT ON COLUMN Task_status.task_id IS 'Идентификатор задания';
COMMENT ON COLUMN Task_status.task_complete_datetime IS 'Время и дата, когда задание стало выполненным задания.';
COMMENT ON COLUMN Task_status.task_status IS 'Статус задания (NEW - новый, DONE - выполненный)';
COMMENT ON TABLE User_Personal_Data IS 'Таблица, хранящая личные данные пользователя';
COMMENT ON COLUMN User_Personal_Data.user_data_id  IS 'Идентификационный номер пользователя';
COMMENT ON COLUMN User_Personal_Data.user_first_name IS 'Имя пользователя';
COMMENT ON COLUMN User_Personal_Data.user_middle_name IS 'Отчество/Второе имя. (Если есть)';
COMMENT ON COLUMN User_Personal_Data.user_last_name IS 'Фамилия пользователя';
COMMENT ON COLUMN User_Personal_Data.user_phone IS 'Номер телефона';



