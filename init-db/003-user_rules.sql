


-- CREATE REVIEW

CREATE PROCEDURE create_review (	account INT,
									num INT,
									header VARCHAR(25),
									descr TEXT,
									mark SMALLINT)
LANGUAGE 'sql'
AS $$
	INSERT INTO review (
		account_id int NOT NULL,
		review_num int NOT NULL,
		review_header varchar(25),
		review_text text,
		review_mark smallint NOT NULL
		)
	VALUES (
		account,
		num,
		header,
		descr,
		mark);
$$;
 	
REVOKE ALL ON PROCEDURE create_review FROM PUBLIC;
GRANT EXECUTE ON PROCEDURE create_review TO client, freelancer;

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
 	
REVOKE ALL ON PROCEDURE watch_reviews FROM PUBLIC;
GRANT EXECUTE ON PROCEDURE watch_reviews TO client, freelancer;

GRANT SELECT ON review TO client, freelancer;

