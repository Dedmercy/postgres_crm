
/* Drop Tables */

DROP TABLE IF EXISTS Review;
DROP TABLE IF EXISTS Service;
DROP TABLE IF EXISTS Editing;
DROP TABLE IF EXISTS Task_status;
DROP TABLE IF EXISTS Task;
DROP TABLE IF EXISTS User_Personal_data;
DROP TABLE IF EXISTS Account;
DROP TABLE IF EXISTS Perk;
DROP TABLE IF EXISTS Role;
DROP TABLE IF EXISTS Spezialization;




/* Create Tables */

CREATE TABLE Account
(
	-- Идентификатор аккаунта
	account_id int NOT NULL,
	-- Логин
	login varchar(12) NOT NULL UNIQUE,
	-- Захешированный пароль
	hash_password varchar(256) NOT NULL,
	-- Идентификатор роли
	role_id int NOT NULL,
	PRIMARY KEY (account_id)
) WITHOUT OIDS;


CREATE TABLE Editing
(
	-- Идентификатор задания
	task_id int NOT NULL,
	-- Идентификатор правки
	editing_id int NOT NULL,
	-- Заголовок правки
	editing_header varchar(50) NOT NULL,
	-- Описание правки
	editing_description text NOT NULL,
	-- Дата создания правки.
	editing_date timestamp NOT NULL,
	PRIMARY KEY (task_id, editing_id)
) WITHOUT OIDS;


CREATE TABLE Perk
(
	-- Идентификатор типа задания
	perk_id serial NOT NULL,
	perk_name varchar(50) NOT NULL,
	-- Идентификатор специализации
	-- 
	sp_id int NOT NULL,
	PRIMARY KEY (perk_id)
) WITHOUT OIDS;


CREATE TABLE Review
(
	-- Идентификационный номер отзыва
	review_number int NOT NULL,
	-- Заголовок отзыва
	review_header varchar(25),
	-- Содержание отзыва
	review_text text,
	-- Оценка. (От 1 до 10).
	review_mark smallint NOT NULL,
	-- Идентификатор аккаунта
	account_id int NOT NULL,
	PRIMARY KEY (review_number)
) WITHOUT OIDS;


CREATE TABLE Role
(
	-- Идентификатор роли
	role_id int NOT NULL,
	role_name varchar(20) NOT NULL,
	PRIMARY KEY (role_id)
) WITHOUT OIDS;


CREATE TABLE Service
(
	-- Идентификатор типа задания
	perk_id int NOT NULL,
	-- Идентификатор аккаунта
	account_id int NOT NULL,
	-- Цена за которую, конкретный пользователь готов выполнить услугу.
	price money,
	-- Описание от контретного пользователя, для услуги которую он может выполнять.
	description text
) WITHOUT OIDS;


CREATE TABLE Spezialization
(
	-- Идентификатор специализации
	-- 
	sp_id int NOT NULL,
	-- Категория специализации
	sp_name varchar(50),
	PRIMARY KEY (sp_id)
) WITHOUT OIDS;


CREATE TABLE Task
(
	-- Идентификатор задания
	task_id int NOT NULL,
	-- Описания задания
	task_description text,
	-- Время добавления задания
	-- 
	time_adding_time timestamp NOT NULL,
	-- Дедлайн для задания
	task_deadline_time timestamp,
	-- Идентификатор аккаунта
	account_id int NOT NULL,
	PRIMARY KEY (task_id)
) WITHOUT OIDS;


CREATE TABLE Task_status
(
	-- Идентификатор задания
	task_id int NOT NULL,
	-- Время окончания выполнения задания
	task_complete_time timestamp,
	task_status varchar(3) NOT NULL,
	PRIMARY KEY (task_id)
) WITHOUT OIDS;


CREATE TABLE User_Personal_data
(
	-- Идентификационный номер пользователя
	user_id  int NOT NULL,
	-- Имя пользователя
	user_first_name varchar(50) NOT NULL,
	-- Отчество/Второе имя. (Если есть)
	user_middle_name varchar(50),
	-- Фамилия пользователя
	user_last_name varchar(50) NOT NULL,
	user_email varchar(50) NOT NULL,
	-- Номер телефона
	user_phone bigint NOT NULL,
	-- Дата регистрации пользователя
	-- 
	user_registration_date timestamp NOT NULL,
	-- Идентификатор аккаунта
	account_id int NOT NULL,
	PRIMARY KEY (user_id )
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
	ADD FOREIGN KEY (account_id)
	REFERENCES Account (account_id)
	ON UPDATE RESTRICT
	ON DELETE RESTRICT
;


ALTER TABLE User_Personal_data
	ADD FOREIGN KEY (account_id)
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



/* Comments */

COMMENT ON COLUMN Account.account_id IS 'Идентификатор аккаунта';
COMMENT ON COLUMN Account.login IS 'Логин';
COMMENT ON COLUMN Account.hash_password IS 'Захешированный пароль';
COMMENT ON COLUMN Account.role_id IS 'Идентификатор роли';
COMMENT ON COLUMN Editing.task_id IS 'Идентификатор задания';
COMMENT ON COLUMN Editing.editing_id IS 'Идентификатор правки';
COMMENT ON COLUMN Editing.editing_header IS 'Заголовок правки';
COMMENT ON COLUMN Editing.editing_description IS 'Описание правки';
COMMENT ON COLUMN Editing.editing_date IS 'Дата создания правки.';
COMMENT ON COLUMN Perk.perk_id IS 'Идентификатор типа задания';
COMMENT ON COLUMN Perk.sp_id IS 'Идентификатор специализации
';
COMMENT ON COLUMN Review.review_number IS 'Идентификационный номер отзыва';
COMMENT ON COLUMN Review.review_header IS 'Заголовок отзыва';
COMMENT ON COLUMN Review.review_text IS 'Содержание отзыва';
COMMENT ON COLUMN Review.review_mark IS 'Оценка. (От 1 до 10).';
COMMENT ON COLUMN Review.account_id IS 'Идентификатор аккаунта';
COMMENT ON COLUMN Role.role_id IS 'Идентификатор роли';
COMMENT ON COLUMN Service.perk_id IS 'Идентификатор типа задания';
COMMENT ON COLUMN Service.account_id IS 'Идентификатор аккаунта';
COMMENT ON COLUMN Service.price IS 'Цена за которую, конкретный пользователь готов выполнить услугу.';
COMMENT ON COLUMN Service.description IS 'Описание от контретного пользователя, для услуги которую он может выполнять.';
COMMENT ON COLUMN Spezialization.sp_id IS 'Идентификатор специализации
';
COMMENT ON COLUMN Spezialization.sp_name IS 'Категория специализации';
COMMENT ON COLUMN Task.task_id IS 'Идентификатор задания';
COMMENT ON COLUMN Task.task_description IS 'Описания задания';
COMMENT ON COLUMN Task.time_adding_time IS 'Время добавления задания
';
COMMENT ON COLUMN Task.task_deadline_time IS 'Дедлайн для задания';
COMMENT ON COLUMN Task.account_id IS 'Идентификатор аккаунта';
COMMENT ON COLUMN Task_status.task_id IS 'Идентификатор задания';
COMMENT ON COLUMN Task_status.task_complete_time IS 'Время окончания выполнения задания';
COMMENT ON COLUMN User_Personal_data.user_id  IS 'Идентификационный номер пользователя';
COMMENT ON COLUMN User_Personal_data.user_first_name IS 'Имя пользователя';
COMMENT ON COLUMN User_Personal_data.user_middle_name IS 'Отчество/Второе имя. (Если есть)';
COMMENT ON COLUMN User_Personal_data.user_last_name IS 'Фамилия пользователя';
COMMENT ON COLUMN User_Personal_data.user_phone IS 'Номер телефона';
COMMENT ON COLUMN User_Personal_data.user_registration_date IS 'Дата регистрации пользователя
';
COMMENT ON COLUMN User_Personal_data.account_id IS 'Идентификатор аккаунта';



