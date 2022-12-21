


-- Создание Отзыва о пользователе

CREATE PROCEDURE create_review (	
	account INT,
	header VARCHAR(25),
	descr TEXT,
	mark SMALLINT)
LANGUAGE 'sql'
AS $$
	INSERT INTO review (
		account_id,
		review_num,
		review_header,
		review_text,
		review_mark,
		author_id
		)
	VALUES (
		account,
		(SELECT count(*) FROM review WHERE account_id = account),
		header,
		descr,
		mark,
		to_regrole(CURRENT_USER)::INT);
$$;

-- Разрешить всем категориям пользователей оставлять отзывы
REVOKE ALL ON PROCEDURE create_review FROM PUBLIC;
GRANT EXECUTE ON PROCEDURE create_review TO client, freelancer;
-- Разрешить доступ к таблице review
GRANT SELECT, INSERT ON review TO client, freelancer;



-- WATCH REVIEWS

CREATE TYPE reviews_type 
AS (	
	account_id INT,
	review_num INT,
	review_header VARCHAR(25),
	review_text TEXT,
	review_mark SMALLINT,
	author_id INT,
	login VARCHAR(12),
	profile_image TEXT,
	user_first_name VARCHAR(50),
	user_last_name VARCHAR(50),
	user_middle_name VARCHAR(50));

CREATE OR REPLACE FUNCTION watch_reviews (id_user INT)
RETURNS SETOF reviews_type
LANGUAGE 'sql'
AS $$
	SELECT 
		rev.account_id,
		rev.review_num,
		rev.review_header,
		rev.review_text,
		rev.review_mark,
		rev.author_id,
		
		acc.login,
		acc.profile_image,
		upd.user_first_name,
		upd.user_last_name,
		upd.user_middle_name
	FROM review as rev
	JOIN account as acc
	ON acc.account_id = rev.author_id
	JOIN user_personal_data as upd
	ON upd.user_data_id = rev.author_id
	WHERE rev.account_id = id_user
	ORDER BY rev.review_num;
$$;
 	
REVOKE ALL ON FUNCTION watch_reviews FROM PUBLIC;
GRANT EXECUTE ON FUNCTION watch_reviews TO client, freelancer;

GRANT SELECT ON review, user_personal_data, account TO client, freelancer;
