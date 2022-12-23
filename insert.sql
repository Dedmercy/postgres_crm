 --������� ������ role
INSERT INTO role(
	role_id,
	role_name
	)
VALUES
	(to_regrole('backend'), 'backend'),
	(to_regrole('client'), 'client'),
	(to_regrole('freelancer'), 'freelancer');
	
-- ������� ������ spezialization
INSERT INTO spezialization(
	sp_id,
	sp_name)
VALUES
	(10, '���������� ������'),
	(11, '����������� ������'),
	(12, '�������'),
	(13, '�����/�����'),
	(14, '����������'),
	(15, '����������'),
	(16, '��������'),
	(17, '���');
	
-- ������� ������  perk	
INSERT INTO perk(
	perk_id,
	perk_name,
	sp_id)
VALUES
	(101, '�������', 10),
	(102, '������ ������', 10),
	(103, '���� ��� ����', 10),
	(104, '��������', 10),
	(105, '��������-��������', 10),
	(111, '2D ��������', 11),
	(112, '3D ���������', 11),
	(113, '��������� �������', 11),
	(114, '�����������', 11),
	(115, '��������', 11),
	(121, '������� ������� ����� ��������', 12),
	(122, '������ �������', 12),
	(123, '����������� �������', 12),
	(124, '�������������� �������', 12),
	(125, '����������� ��, ���, ������', 12),
	(131, '�����������', 13),
	(132, '�����������', 13),
	(133, '�����������', 13),
	(134, '������/�����', 13),
	(135, '���������', 13),
	(141, '�������������', 14),
	(142, '�������', 14),
	(143, '���������/������������� ������', 14),
	(144, '������ ������', 14),
	(145, '������������ ������', 14),
	(151, '�������/�����', 15),
	(152, '���������', 15),
	(153, '���������', 15),
	(154, '�����������', 15),
	(155, '��������������', 15),
	(161, '���������', 16),
	(162, '�������������', 16),
	(163, '����������� ������', 16),
	(164, '������������', 16),
	(165, '�����������', 16),
	(171, '�������', 17),
	(172, '��������', 17),
	(173, '������ ��������', 17),
	(174, '�������-����', 17),
	(175, '�������-���', 17);

	
	
-- ����� ��������� create_user
CALL create_user(
	'������',
	'����������',
	'��������',
	'reznik@mail.ru',
	89661234455,
	'reznik',
	'reznikeTop1',
	'freelancer',
	FALSE,
	'1-102-128.png');
	
CALL create_user(
	'�����',
	'�����������',
	'�����������',
	'Bigmounth@mail.ru',
	89663217788,
	'kebab',
	'ParolKrutoi',
	'client',
	FALSE,
	'1-101-128.png');
	
CALL create_user(
	'���������',
	'�����',
	'��������',
	'ewasince@gmail.com',
	89151226153,
	'ewasince',
	'ParolKrutoi228!',
	'freelancer',
	TRUE,
	'1-102-128.png');
	
CALL create_user(
	'����',
	'����������',
	'�������',
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
	'������� ��������!'::CHARACTER VARYING(25),
	'���������� �����, ������� ��������'::TEXT,
	10::SMALLINT);

CALL add_perk(
            101,
            228::MONEY,
            '�����. ������. ��������.'::TEXT
            );

RESET ROLE;
	
SET ROLE dedmercy;

-- �������� �������
CALL create_review(
	to_regrole('ewasince')::INT,
	'�������� ������'::CHARACTER VARYING(25),
	'�������� ������ � ����, �������� ����������.'::TEXT,
	10::SMALLINT);
	
CALL create_review(
	to_regrole('ewasince')::INT,
	'�� �����!'::CHARACTER VARYING(25),
	'��� ����������!!.'::TEXT,
	9::SMALLINT);
	
CALL create_review(
	to_regrole('ewasince')::INT,
	'�����!'::CHARACTER VARYING(25),
	'�� ��� ������ ��� �������� ��'::TEXT,
	6::SMALLINT);
 
 -- �������� �������
CALL create_task(
	'������� ����� �� ��������', 
	to_regrole('ewasince')::INT, 
	'12.08.2023'::TIMESTAMP WITHOUT TIME ZONE);
	
	CALL create_task(
	'������� ������������', 
	to_regrole('ewasince')::INT, 
	'12.08.2023'::TIMESTAMP WITHOUT TIME ZONE);
	
RESET ROLE;


SELECT * FROM watch_reviews(to_regrole('ewasince')::INT);
	
SELECT * FROM watch_reviews(to_regrole('dedmercy')::INT);


	