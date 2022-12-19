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
	'reznikTop1',
	'freelancer');
	
CALL create_user(
	'�����',
	'�����������',
	'�����������',
	'Bigmounth@mail.ru',
	89663217788,
	'kebab',
	'ParolKrutoi',
	'client');
	
-- �������� �������
CALL create_review(
	to_regrole('reznik')::INTEGER,
	1,
	'�������� ������'::CHARACTER VARYING(25),
	'�������� ������ � ����, �������� ����������.'::TEXT,
	10::SMALLINT,
	to_regrole('kebab')::INTEGER);
	
CALL create_review(
	to_regrole('reznik')::INTEGER,
	2,
	'�����'::CHARACTER VARYING(25),
	'�� ��������.'::TEXT,
	9::SMALLINT,
	to_regrole('kebab')::INTEGER);
	
CALL create_review(
	to_regrole('reznik')::INTEGER,
	3,
	'�������� �����'::CHARACTER VARYING(25),
	'������� ��� ��������'::TEXT,
	2::SMALLINT,
	to_regrole('kebab')::INTEGER);
	
SELECT * FROM watch_reviews(16559);
 
SET ROLE kebab;
 
 -- �������� �������
CALL create_task(
	10001, 
	'������� ����� �� ��������', 
	to_regrole('reznik')::INTEGER, 
	'12.08.2023'::TIMESTAMP WITHOUT TIME ZONE, 
	131);
	
	CALL create_task(
	10002, 
	'������� ������������', 
	to_regrole('reznik')::INTEGER, 
	'12.08.2023'::TIMESTAMP WITHOUT TIME ZONE, 
	131);
	
RESET ROLE;
	