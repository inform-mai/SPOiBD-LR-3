import mysql.connector
import csv


class Database:
    def __init__(self):
        self.connection = mysql.connector.connect(
            host="mysql.65e3ab49565f.hosting.myjino.ru",
            user="j30084097_137",
            password="Gruppa137",
            database="j30084097_137",
        )
        self.cursor = self.connection.cursor(dictionary=True)

    # CREATE
    def create(self, table, data):
        columns = ", ".join(data.keys())
        values = ", ".join(["%s"] * len(data))
        query = f"INSERT INTO {table} ({columns}) VALUES ({values})"
        self.cursor.execute(query, list(data.values()))
        self.connection.commit()
        return self.cursor.lastrowid

    # READ с фильтрацией
    def read(self, table, condition=None, order_by=None, limit=None):
        query = f"SELECT * FROM {table}"
        if condition:
            query += f" WHERE {condition}"
        if order_by:
            query += f" ORDER BY {order_by}"
        if limit:
            query += f" LIMIT {limit}"
        self.cursor.execute(query)
        return self.cursor.fetchall()

    # UPDATE
    def update(self, table, data, condition):
        set_clause = ", ".join([f"{k} = %s" for k in data.keys()])
        query = f"UPDATE {table} SET {set_clause} WHERE {condition}"
        self.cursor.execute(query, list(data.values()))
        self.connection.commit()

    # DELETE
    def delete(self, table, condition):
        query = f"DELETE FROM {table} WHERE {condition}"
        self.cursor.execute(query)
        self.connection.commit()

    # INNER JOIN
    def inner_join(self, table1, table2, key1, key2, condition=None):
        query = f"SELECT * FROM {table1} INNER JOIN {table2} ON {table1}.{key1} = {table2}.{key2}"
        if condition:
            query += f" WHERE {condition}"
        self.cursor.execute(query)
        return self.cursor.fetchall()

    # LEFT JOIN
    def left_join(self, table1, table2, key1, key2, condition=None):
        query = f"SELECT * FROM {table1} LEFT JOIN {table2} ON {table1}.{key1} = {table2}.{key2}"
        if condition:
            query += f" WHERE {condition}"
        self.cursor.execute(query)
        return self.cursor.fetchall()

    # RIGHT JOIN
    def right_join(self, table1, table2, key1, key2, condition=None):
        query = f"SELECT * FROM {table1} RIGHT JOIN {table2} ON {table1}.{key1} = {table2}.{key2}"
        if condition:
            query += f" WHERE {condition}"
        self.cursor.execute(query)
        return self.cursor.fetchall()

    # UNION
    def union(self, query1, query2):
        query = f"{query1} UNION {query2}"
        self.cursor.execute(query)
        return self.cursor.fetchall()

    # Новые методы

    # 1. Вывод конкретного столбца в порядке убывания или возрастания
    def get_column_ordered(self, table, column, order="ASC"):
        query = f"SELECT {column} FROM {table} ORDER BY {column} {order}"
        self.cursor.execute(query)
        return self.cursor.fetchall()

    # 2. Вывод диапазона строк по айди
    def get_range_by_id(self, table, id_column, start_id, end_id):
        query = f"SELECT * FROM {table} WHERE {id_column} BETWEEN %s AND %s"
        self.cursor.execute(query, (start_id, end_id))
        return self.cursor.fetchall()

    # 3. Удаление диапазона строк по айди
    def delete_range_by_id(self, table, id_column, start_id, end_id):
        query = f"DELETE FROM {table} WHERE {id_column} BETWEEN %s AND %s"
        self.cursor.execute(query, (start_id, end_id))
        self.connection.commit()
        return self.cursor.rowcount

    # 4. Вывод структуры таблицы
    def get_table_structure(self, table):
        query = f"DESCRIBE {table}"
        self.cursor.execute(query)
        return self.cursor.fetchall()

    # 5. Вывод строки содержащей конкретное значение в конкретном столбце
    def get_row_by_value(self, table, column, value):
        query = f"SELECT * FROM {table} WHERE {column} = %s"
        self.cursor.execute(query, (value,))
        return self.cursor.fetchall()

    # 6. Удаление таблицы
    def drop_table(self, table):
        query = f"DROP TABLE IF EXISTS {table}"
        self.cursor.execute(query)
        self.connection.commit()

    # 7. Добавление нового столбца
    def add_column(self, table, column_name, column_type):
        query = f"ALTER TABLE {table} ADD COLUMN {column_name} {column_type}"
        self.cursor.execute(query)
        self.connection.commit()

    # 7. Удаление столбца
    def drop_column(self, table, column_name):
        query = f"ALTER TABLE {table} DROP COLUMN {column_name}"
        self.cursor.execute(query)
        self.connection.commit()

    # 8. Экспорт таблицы в CSV
    def export_to_csv(self, table, filename):
        query = f"SELECT * FROM {table}"
        self.cursor.execute(query)
        rows = self.cursor.fetchall()

        if not rows:
            print("Таблица пуста")
            return

        columns = rows[0].keys()

        with open(filename, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=columns)
            writer.writeheader()
            writer.writerows(rows)

        print(f"Данные экспортированы в {filename}")
    # Импорт таблицы из CSV
    def import_from_csv(self, table, filename):
        with open(filename, 'r', encoding='utf-8', newline='') as f:
            reader = csv.DictReader(f)
            for row in reader:
                if isinstance(row, dict):
                    data = {key: (value if value != '' else None)
                            for key, value in row.items()}
                    self.create(table, data)

        print(f"Данные импортированы из {filename}")

    def close(self):
        self.cursor.close()
        self.connection.close()
