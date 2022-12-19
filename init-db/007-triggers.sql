


-- Триггер для проверки услуг

CREATE FUNCTION service_validate() 
RETURNS trigger 
LANGUAGE plpgsql
AS $$
    BEGIN
        -- Цена услуги должна быть больше 0
        IF CAST (NEW.price as NUMERIC) < 0 THEN
            RAISE EXCEPTION 'service cannot have a negative cost';
        END IF;
		
        RETURN NEW;
    END;
$$;

CREATE TRIGGER service_validate BEFORE INSERT OR UPDATE ON service
    FOR EACH ROW EXECUTE PROCEDURE service_validate();



-- Триггер для проверки времени дедлайна

CREATE FUNCTION deadline_check() 
RETURNS trigger 
LANGUAGE plpgsql
AS $$
    BEGIN
        -- Время дедлайна явно не должно быть меньше, чем время создания
        IF NEW.task_deadline_datetime < NEW.task_creating_datetime THEN
            RAISE EXCEPTION 'deadline must be after creating time!';
        END IF;
		
        RETURN NEW;
    END;
$$;

CREATE TRIGGER deadline_check BEFORE INSERT OR UPDATE ON task
    FOR EACH ROW EXECUTE PROCEDURE deadline_check();