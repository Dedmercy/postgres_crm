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
	user_nickname CHARACTER VARYING(12),
	user_password CHARACTER VARYING(20),
	role_name CHARACTER VARYING(20),
	image_path TEXT DEFAULT 'no_image.jpg'
	)
	AS $$
	BEGIN
	-- Создаём новую роль для пользователя
	EXECUTE FORMAT('CREATE ROLE %I LOGIN PASSWORD %L', user_nickname, user_password);
	--	Наследуем права от соответствующей роли
	EXECUTE FORMAT('GRANT %I TO %I', role_name, user_nickname);
	--	Заполняем таблицу с данными учетной записи
	INSERT INTO account(
		account_id,
		login,
		hash_password,
		role_id,
		account_registration_date,
		last_seen_datetime,
		profile_image)
	VALUES(
		to_regrole(user_nickname),
		user_nickname,
		crypt(user_password, gen_salt('md5')),
		to_regrole(role_name),
		CURRENT_DATE,
		CURRENT_TIMESTAMP,
		image_path);
	--	Заполняем таблицу с Персональными данными
	INSERT INTO user_personal_data(
		user_data_id,
		user_first_name,
		user_middle_name,
		user_last_name,
		user_email,
		user_phone)
	VALUES(
		to_regrole(user_nickname),
		first_name,
		middle_name,
		last_name,
		email,
		phone);
	END;
	$$
	LANGUAGE plpgsql;

REVOKE EXECUTE ON PROCEDURE create_user FROM PUBLIC;
GRANT EXECUTE ON PROCEDURE create_user TO backend;
 