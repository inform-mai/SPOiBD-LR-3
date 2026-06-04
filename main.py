# Пример для MySQL
from database import Database

db = Database()

# 1. Получить столбец "name" по возрастанию
result = db.get_column_ordered("users", "name", "ASC")
print(f"{result}\n")

# 2. Получить строки с id от 1 до 10
result = db.get_range_by_id("users", "id", 1, 10)
print(f"{result}\n")

# 3. Удалить строки с id от 5 до 15
count = db.delete_range_by_id("users", "id", 5, 15)
print(f"Удалено строк: {count}\n")

# 4. Посмотреть структуру таблицы
structure = db.get_table_structure("users")
print(f"{structure}\n")

# 5. Найти пользователя с email "test@example.com"
result = db.get_row_by_value("users", "email", "test@example.com")
print(f"{result}\n")

# 6. Удалить таблицу
db.drop_table("temp_table")

# 7. Добавить столбец
db.add_column("users", "phone", "VARCHAR(20)")

# 7. Удалить столбец
db.drop_column("users", "phone")

# 8. Экспорт в CSV
db.export_to_csv("users", "users_export.csv")
print()
# 9. Импорт из CSV
db.import_from_csv("users", "users_import.csv")

db.close()
