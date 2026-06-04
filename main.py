# Пример для MySQL
from database import Database

db = Database()


# Проверка наполненности таблицы
print("\n--- НАПОЛНЕННОСТЬ ТАБЛИЦЫ ---")
all_users = db.read("users")
print(f"Всего пользователей в таблице: {len(all_users)}")
if all_users:
    print(f"Пример записи: {all_users[0]}")

# 1. Получить столбец "name" по возрастанию
print("\n--- 1. СТОЛБЕЦ NAME ПО ВОЗРАСТАНИЮ ---")
result = db.get_column_ordered("users", "name", "ASC")
print(f"Имена по алфавиту: {result}")

# 2. Получить столбец "name" по убыванию
print("\n--- 2. СТОЛБЕЦ NAME ПО УБЫВАНИЮ ---")
result = db.get_column_ordered("users", "name", "DESC")
print(f"Имена в обратном порядке: {result}")

# 3. Посмотреть структуру таблицы
print("\n--- 3. СТРУКТУРА ТАБЛИЦЫ USERS ---")
structure = db.get_table_structure("users")
print("Структура таблицы:")
for col in structure:
    print(f"  {col}")

# 4. Если есть данные, получим диапазон по реальным ID
print("\n--- 4. ДИАПАЗОН СТРОК ПО ID ---")
if all_users:
    # Получаем минимальный и максимальный ID из реальных данных
    min_id = min(user['id'] for user in all_users)
    max_id = max(user['id'] for user in all_users)
    print(f"ID в таблице: от {min_id} до {max_id}")

    result = db.get_range_by_id("users", "id", min_id, min_id + 2)
    print(f"Строки с id от {min_id} до {min_id + 2}: {result}")
else:
    print("Таблица пуста, добавляем тестовые данные...")
    db.create("users", {"name": "Иван", "email": "ivan@test.com"})
    db.create("users", {"name": "Мария", "email": "maria@test.com"})
    db.create("users", {"name": "Петр", "email": "petr@test.com"})
    all_users = db.read("users")
    min_id = min(user['id'] for user in all_users)
    result = db.get_range_by_id("users", "id", min_id, min_id + 1)
    print(f"Строки с id от {min_id} до {min_id + 1}: {result}")

# 5. Найти пользователя по реальному email
print("\n--- 5. ПОИСК ПОЛЬЗОВАТЕЛЯ ПО EMAIL ---")
if all_users:
    # Берем email из первой записи
    test_email = all_users[0]['email']
    print(f"Ищем пользователя с email: {test_email}")
    result = db.get_row_by_value("users", "email", test_email)
    print(f"Найден: {result}")
else:
    print("Нет данных для поиска")

# 6. Экспорт в CSV
print("\n--- 6. ЭКСПОРТ В CSV ---")
db.export_to_csv("users", "users_export.csv")

# 7. Добавить столбец
print("\n--- 7. ДОБАВЛЕНИЕ СТОЛБЦА ---")
db.add_column("users", "phone", "VARCHAR(20)")
print("Добавлен столбец 'phone' типа VARCHAR(20)")
structure = db.get_table_structure("users")
print("Структура после добавления:")
for col in structure:
    print(f"  {col}")

# 8. Удалить столбец
print("\n--- 8. УДАЛЕНИЕ СТОЛБЦА ---")
db.drop_column("users", "phone")
print("Удален столбец 'phone'")
structure = db.get_table_structure("users")
print("Структура после удаления:")
for col in structure:
    print(f"  {col}")

# 9. Удаление диапазона строк
print("\n--- 9. УДАЛЕНИЕ ДИАПАЗОНА СТРОК ---")
all_users = db.read("users")
if all_users and len(all_users) > 3:
    min_id = min(user['id'] for user in all_users)
    # Удаляем 2 записи
    count = db.delete_range_by_id("users", "id", min_id, min_id + 1)
    print(f"Удалено строк: {count}")

    # Проверяем результат
    remaining = db.read("users")
    print(f"Осталось записей: {len(remaining)}")
else:
    print("Недостаточно данных для удаления диапазона")

# 10. Импорт из CSV
print("\n--- 10. ИМПОРТ ИЗ CSV ---")
db.import_from_csv("users", "users_import.csv")

# 11. Удаление таблицы (тестовой)
print("\n--- 11. УДАЛЕНИЕ ТАБЛИЦЫ ---")
db.drop_table("temp_table")
print("Таблица 'temp_table' удалена (если существовала)")


db.close()