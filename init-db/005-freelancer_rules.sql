GRANT SELECT, INSERT, DELETE ON service to freelancer;

-- Добавление навыка пользователю.
CREATE PROCEDURE add_perk(
	perk_id INTEGER,
	price MONEY,
	descr TEXT)	
AS $$
BEGIN 
	-- Добавить запись о навыке исполнителя.
	INSERT INTO service(
		perk_id,
		account_id,
		price,
		description)
	VALUES(
		perk_id,
		to_regrole(CURRENT_USER),
		price,
		descr
	);
END;
$$	
LANGUAGE plpgsql;

 	
REVOKE ALL ON PROCEDURE add_perk FROM PUBLIC;
GRANT EXECUTE ON PROCEDURE add_perk TO freelancer;


-- Просмотр навыков пользователя
CREATE FUNCTION check_perks(
	checked_account_id INTEGER)
RETURNS TABLE(
	perk_id INTEGER,
	perk_name CHARACTER VARYING(50),
	price MONEY,
	descr TEXT)
AS $$
BEGIN 
	-- Поиск по текущему пользователю
	RETURN QUERY 
		SELECT 
			perk.perk_id,
			perk.perk_name,
			service.price,
			service.description
		FROM service
		JOIN perk
		ON perk.perk_id = service.perk_id
		WHERE service.account_id = checked_account_id;
	 
END;
$$
LANGUAGE plpgsql;

GRANT SELECT ON perk TO freelancer;

REVOKE ALL ON FUNCTION check_perks FROM PUBLIC;
GRANT EXECUTE ON FUNCTION check_perks TO freelancer;


-- Просмотр текущих заданий фрилансером
CREATE VIEW current_freelanser_tasks_information AS
	SELECT
		task.task_id,
		task.task_description,
		task.client,
		task.task_creating_datetime,
		task.task_deadline_datetime,
		task_status.task_status,
		task_status.task_complete_datetime
	FROM task
	JOIN task_status 
	ON task.task_id = task_status.task_id
	WHERE executor = to_regrole(CURRENT_USER);
	

GRANT SELECT ON current_freelanser_tasks_information to freelancer;


