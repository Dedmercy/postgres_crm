-- Разрешить доступ к таблицам базы данных
GRANT SELECT, UPDATE, INSERT, DELETE ON ALL TABLES IN SCHEMA public to backend;

--УБРАТЬ 
CREATE EXTENSION IF NOT EXISTS pgcrypto;

-- Процедура создания нового пользователя.
CREATE PROCEDURE create_user(
	data_id INTEGER,
	first_name CHARACTER VARYING(50),
	middle_name CHARACTER VARYING(50),
	last_name CHARACTER VARYING(50),
	email CHARACTER VARYING(50),
	phone BIGINT,
	user_nickname CHARACTER VARYING(12),
	user_password CHARACTER VARYING(20),
	role_name CHARACTER VARYING(20),
	executor_status BOOLEAN,
	)
	AS $$
	BEGIN
	-- Создаём новую роль для пользователя
	EXECUTE FORMAT('CREATE ROLE %I LOGIN PASSWORD %L', user_nickname, user_password);
	--	Наследуем права от соответствующей роли
	EXECUTE FORMAT('GRANT %I TO %I', role_name, user_nickname);
	--	Заполняем таблицу с Персональными данными
	INSERT INTO user_personal_data(
		user_id,
		user_first_name,
		user_middle_name,
		user_last_name,
		user_email,
		user_phone)
	VALUES(
		id,
		first_name,
		middle_name,
		last_name,
		email,
		phone);
	--	Заполняем таблицу с данными учетной записи
	INSERT INTO account(
		login,
		hash_password,
		role_id,
		user_data_id,
		account_registration_date,
		last_seen_datetime,
		is_executor)
	VALUES(
		user_nickname,
		crypto(user_password, gen_salt('md5')),
		to_regrole(role_name),
		CURRENT_DATE,
		CURRENT_TIMESTAMP,
		executor_status);
	END;
	$$
	LANGUAGE plpgsql;

	
 