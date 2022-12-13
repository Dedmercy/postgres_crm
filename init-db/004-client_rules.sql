


-- CREATE TASK

CREATE PROCEDURE create_task (	
	id INT, 
	descr TEXT, 
	executor INT, 
	deadline TIMESTAMP WITHOUT TIME ZONE, 
	perk INT)
LANGUAGE 'sql'
AS $$
	INSERT INTO task (
		task_id,
		task_description,
		executor,
		client,
		task_creating_datetime,
		task_deadline_datetime,
		perk_id
		)
	VALUES (
		id,
		descr,
		executor,
		to_regrole(CURRENT_USER),
		CURRENT_TIMESTAMP,
		deadline,
		perk);
	 INSERT INTO task_status (
		task_id,
		task_status
		)
	VALUES (
		id,
		'NEW');
$$;
 	
REVOKE ALL ON PROCEDURE create_task FROM PUBLIC;
GRANT EXECUTE ON PROCEDURE create_task TO client;

GRANT SELECT, INSERT ON task TO client; 
GRANT SELECT, INSERT ON task_status TO client;



-- DELETE TASK

CREATE PROCEDURE delete_task (id INT)
LANGUAGE 'sql'
AS $$
	DELETE FROM task 
	WHERE task_id = id;

	DELETE FROM task_status 
	WHERE task_id = id;
$$;
 	
REVOKE ALL ON PROCEDURE delete_task FROM PUBLIC;
GRANT EXECUTE ON PROCEDURE delete_task TO client;

GRANT SELECT, DELETE ON task TO client; 
GRANT SELECT, DELETE ON task_status TO client;



-- CONFIRM EXECUTOR

CREATE PROCEDURE confirm_executor(	
	potential_executor INT,
	selected_task INT)
LANGUAGE 'sql'
AS $$
	UPDATE task
	SET executor = potential_executor
	WHERE task_id = selected_task;

	UPDATE task_status
	SET task_status = 'WORK'
	WHERE task_id = selected_task;
$$;
 	
REVOKE ALL ON PROCEDURE confirm_executor FROM PUBLIC;
GRANT EXECUTE ON PROCEDURE confirm_executor TO client;

GRANT SELECT, UPDATE ON task TO client; 
GRANT SELECT, UPDATE ON task_status TO client;



-- ADD EDITING

CREATE PROCEDURE add_editing(	
	task INT,
	num INT,
	header VARCHAR(50),
	descr TEXT)

LANGUAGE 'sql'
AS $$
	INSERT INTO editing (
		task_id,
		editing_num,
		editing_header,
		editing_text,
		editing_date
		)
	VALUES (
		task,
		num,
		header,
		descr,
		CURRENT_TIMESTAMP);
$$;
 	
REVOKE ALL ON PROCEDURE add_editing FROM PUBLIC;
GRANT EXECUTE ON PROCEDURE add_editing TO client;

GRANT SELECT, INSERT ON editing TO client; 



-- MARK TASK AS COMPLETED

CREATE PROCEDURE mark_complete (	task INT)
LANGUAGE 'sql'
AS $$
	UPDATE task_status
	SET task_status = 'DONE'
	WHERE task_id = task;
$$;
 	
REVOKE ALL ON PROCEDURE mark_complete FROM PUBLIC;
GRANT EXECUTE ON PROCEDURE mark_complete TO client;

GRANT SELECT, UPDATE ON task_status TO client;
