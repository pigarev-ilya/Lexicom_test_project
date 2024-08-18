# Тестовое задание в компанию "Lexicom"
## Задание №1

RESTful сервис с использованием Fast API и Redis, который принимает и отдает данные по номеру телефона. 

## Задание №2

Перенос данных о статусе с таблицы short_names в full_names.

### Решение

#### Решение 1 (Python)

```python
import psycopg2
import time

conn = psycopg2.connect("dbname=db_name user=db_user password=db_password")

start_time = time.time()

full_name_exts = {}
update_values = []

cur = conn.cursor()

cur.execute("SELECT * FROM full_names")

for i in cur.fetchall():
    name, ext = i[0].split('.')
    full_name_exts[name] = ext

cur.execute("SELECT * FROM short_names")

for item in cur.fetchall():
    if ext := full_name_exts.get(item[0]):
        update_values.append(f"('{item[0]}.{ext}', {item[1]})")


cur.execute(f"""UPDATE FULL_NAMES AS FN
                SET
                    STATUS = V.STATUS
                FROM
                    (
                        VALUES {','.join(update_values)}
                    ) AS V (NAME, STATUS)
                WHERE
                    V.NAME = FN.NAME;
                        """)

conn.commit()

end_time = time.time()

execution_time = end_time - start_time

print(f"Время выполнения: {execution_time} секунд")
```

#### Решение 2 (SQL)

```sql
    UPDATE FULL_NAMES
SET
	STATUS = V.STATUS
FROM
	(
		SELECT
			FULL_NAMES.NAME AS F_NAME,
			SHORT_NAMES.STATUS AS S_STATUS
		FROM
			PUBLIC.FULL_NAMES
			JOIN PUBLIC.SHORT_NAMES ON SPLIT_PART(FULL_NAMES.NAME, '.', 1) = SHORT_NAMES.NAME
	) AS V (NAME, STATUS)
WHERE
	V.NAME = FULL_NAMES.NAME;
```