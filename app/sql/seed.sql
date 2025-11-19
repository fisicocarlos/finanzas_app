INSERT INTO
	TYPES (NAME)
VALUES
	('income'),
	('expense'),
	('other')
ON CONFLICT DO NOTHING;

INSERT INTO
	CATEGORIES (
		NAME,
		TYPE_ID_DEFAULT,
		COLOR,
		DESCRIPTION,
		ICON_CHAR
	)
SELECT
	V.NAME,
	T.TYPE_ID,
	V.COLOR,
	V.DESCRIPTION,
	V.ICON_CHAR
FROM
	(
		VALUES
			('Casa', 'expense', '#D1495B', '', ''),
			('Obligatorios', 'expense', '#ED6A5A', '', ''),
			('Restaurante', 'expense', '#F4A261', '', '󰡶'),
			('Gasolina', 'expense', '#E76F51', '', '󰊘'),
			('Regalos', 'expense', '#F77F00', '', ''),
			('Ropa', 'expense', '#E07A5F', '', ''),
			('Efectivo', 'expense', '#F2CC8F', '', ''),
			('Comida', 'expense', '#F4A259', '', ''),
			('Bar', 'expense', '#E36414', '', ''),
			('Multas', 'expense', '#C1121F', '', '󰦶'),
			('Videojuegos', 'expense', '#D62828', '', '󰊴'),
			('Suscripciones', 'expense', '#FF9F1C', '', ''),
			('Libros', 'expense', '#B56576', '', ''),
			('Nómina', 'income', '#2A9D8F', '', ''),
			('Música', 'income', '#38A3A5', '', ''),
			('Repaso', 'income', '#57CC99', '', ''),
			('Otros ingresos', 'income', '#80ED99', '', ''),
			('Otros gastos', 'income', '#34A0A4', '', '')
	) AS V (NAME, TYPE_NAME, COLOR, DESCRIPTION, ICON_CHAR)
	JOIN TYPES T ON T.NAME = V.TYPE_NAME
ON CONFLICT (NAME) DO UPDATE
SET
	TYPE_ID_DEFAULT = EXCLUDED.TYPE_ID_DEFAULT,
	COLOR = EXCLUDED.COLOR,
	DESCRIPTION = EXCLUDED.DESCRIPTION,
	ICON_CHAR = EXCLUDED.ICON_CHAR;

INSERT INTO
	TRIPS (NAME, DATE_START, DATE_END, COLOR)
VALUES
	('LOGROÑO', '2025-10-09', '2025-10-12', '#722f37')
ON CONFLICT (NAME) DO UPDATE
SET
	DATE_START = EXCLUDED.DATE_START,
	DATE_END = EXCLUDED.DATE_END,
	COLOR = EXCLUDED.COLOR;
