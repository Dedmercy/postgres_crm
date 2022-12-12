-- Разрешить доступ к таблицам базы данных
GRANT SELECT, UPDATE, INSERT, DELETE ON ALL TABLES IN SCHEMA public to backend;

--УБРАТЬ 
CREATE EXTENSION IF NOT EXISTS pgcrypto;

-- Процедура создания нового пользователя.
CREATE PROCEDURE create_user(
	first_name CHARACTER VARYING(50),
	middle_name CHARACTER VARYING(50),
	last_name CHARACTER VARYING(50),
	email CHARACTER VARYING(50),
	phone BIGINT,
	user_nickname,
	)