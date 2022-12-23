 --Вставка данных role
INSERT INTO role(
	role_id,
	role_name
	)
VALUES
	(to_regrole('backend'), 'backend'),
	(to_regrole('client'), 'client'),
	(to_regrole('freelancer'), 'freelancer');
	
-- Вставка данных spezialization
INSERT INTO spezialization(
	sp_id,
	sp_name)
VALUES
	(10, 'Разработка сайтов'),
	(11, 'Графический дизайн'),
	(12, 'Перевод'),
	(13, 'Аудио/Видео'),
	(14, 'Фотография'),
	(15, 'Инжиниринг'),
	(16, 'Интерьер'),
	(17, 'Арт');
	
-- Вставка данных  perk	
INSERT INTO perk(
	perk_id,
	perk_name,
	sp_id)
VALUES
	(101, 'Верстка', 10),
	(102, 'Дизайн сайтов', 10),
	(103, 'Сайт под ключ', 10),
	(104, 'Лендинги', 10),
	(105, 'Интернет-магазины', 10),
	(111, '2D анимация', 11),
	(112, '3D персонажи', 11),
	(113, 'Векторная графика', 11),
	(114, 'Презентации', 11),
	(115, 'Логотипы', 11),
	(121, 'Перевод текстов общей тематики', 12),
	(122, 'Устный перевод', 12),
	(123, 'Технический перевод', 12),
	(124, 'Художественный перевод', 12),
	(125, 'Локализация ПО, игр, сайтов', 12),
	(131, 'Видеомонтаж', 13),
	(132, 'Раскадровки', 13),
	(133, 'Аудиомонтаж', 13),
	(134, 'Музыка/Звуки', 13),
	(135, 'Режиссура', 13),
	(141, 'Ретуширование', 14),
	(142, 'Коллажи', 14),
	(143, 'Рекламная/Постановочная съемка', 14),
	(144, 'Съемка зданий', 14),
	(145, 'Промышленная съемка', 14),
	(151, 'Чертежи/Схемы', 15),
	(152, 'Электрика', 15),
	(153, 'Отопление', 15),
	(154, 'Конструкции', 15),
	(155, 'Машиностроение', 15),
	(161, 'Интерьеры', 16),
	(162, 'Макетирование', 16),
	(163, 'Ландшафтный дизайн', 16),
	(164, 'Вузуализация', 16),
	(165, 'Архитектура', 16),
	(171, 'Графити', 17),
	(172, 'Живопись', 17),
	(173, 'Дизайн упаковки', 17),
	(174, 'Концепт-арты', 17),
	(175, 'Пиксель-арт', 17);

	
	
-- Вызов процедуры create_user
CALL create_user(
	'Виктор',
	'Михайлович',
	'Резников',
	'reznik@mail.ru',
	89661234455,
	'reznik',
	'reznikeTop1',
	'freelancer',
	FALSE,
	'1-102-128.png');
	
CALL create_user(
	'Антон',
	'Анатольевич',
	'Большеротов',
	'Bigmounth@mail.ru',
	89663217788,
	'kebab',
	'ParolKrutoi',
	'client',
	FALSE,
	'1-101-128.png');
	
CALL create_user(
	'Владислав',
	'Ильич',
	'Лавренов',
	'ewasince@gmail.com',
	89151226153,
	'ewasince',
	'ParolKrutoi228!',
	'freelancer',
	TRUE,
	'1-102-128.png');
	
CALL create_user(
	'Артём',
	'Непомневич',
	'Аничков',
	'dedmercy@gmail.com',
	89661180398,
	'dedmercy',
	'ParolKrutoi1337!',
	'client',
	TRUE,
	'1-101-128.png');
	

SET ROLE ewasince;
	
CALL create_review(
	to_regrole('dedmercy')::INT,
	'Хороший заказчик!'::CHARACTER VARYING(25),
	'Адекватные сроки, хорошая зарплата'::TEXT,
	10::SMALLINT);

CALL add_perk(
            101,
            228::MONEY,
            'Долго. Дорого. Офигенно.'::TEXT
            );

RESET ROLE;
	
SET ROLE dedmercy;

-- Проверка отзывов
CALL create_review(
	to_regrole('ewasince')::INT,
	'Отличная работа'::CHARACTER VARYING(25),
	'Выполнил работу в срок, отличное исполнение.'::TEXT,
	10::SMALLINT);
	
CALL create_review(
	to_regrole('ewasince')::INT,
	'Всё супер!'::CHARACTER VARYING(25),
	'Без пререканий!!.'::TEXT,
	9::SMALLINT);
	
CALL create_review(
	to_regrole('ewasince')::INT,
	'Пойдёт!'::CHARACTER VARYING(25),
	'Не так быстро как хотелось бы'::TEXT,
	6::SMALLINT);
 
 -- Создание задания
CALL create_task(
	'сделать видео на утренник', 
	to_regrole('ewasince')::INT, 
	'12.08.2023'::TIMESTAMP WITHOUT TIME ZONE);
	
	CALL create_task(
	'сделать видеоподкаст', 
	to_regrole('ewasince')::INT, 
	'12.08.2023'::TIMESTAMP WITHOUT TIME ZONE);
	
RESET ROLE;


SELECT * FROM watch_reviews(to_regrole('ewasince')::INT);
	
SELECT * FROM watch_reviews(to_regrole('dedmercy')::INT);


	