
-- Создание Отзыва о пользователе
CREATE PROCEDURE create_review (	
	account INT,
	num INT,
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
		review_mark
		)
	VALUES (
		account,
		num,
		header,
		descr,
		mark);
$$;

-- Разрешить всем категориям пользователей оставлять отзывы
REVOKE ALL ON PROCEDURE create_review FROM PUBLIC;
GRANT EXECUTE ON PROCEDURE create_review TO client, freelancer;
-- Разрешить доступ к таблице review
GRANT SELECT, INSERT ON review TO client, freelancer;



-- WATCH REVIEWS

--CREATE TYPE review AS (name character varying(50), gen INT, in_time INT, out_time INT, not_time INT, in_process INT);

CREATE FUNCTION watch_reviews (id_user INT)
RETURNS review
LANGUAGE 'sql'
AS $$
	SELECT *
	FROM review
	WHERE account_id = id_user
	ORDER BY review_num;
$$;
 	
REVOKE ALL ON FUNCTION watch_reviews FROM PUBLIC;
GRANT EXECUTE ON FUNCTION watch_reviews TO client, freelancer;
