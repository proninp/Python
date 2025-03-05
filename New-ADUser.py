import csv
import random
import string
from pyad import aduser, adcontainer

# Функция для генерации сложного пароля
def generate_password(length=12):
    # Символы, из которых будет состоять пароль
    characters = string.ascii_letters + string.digits + string.punctuation
    # Генерация пароля
    password = ''.join(random.choice(characters) for _ in range(length))
    return password

# Функция для генерации логина
def generate_login(first_name, middle_name, last_name):
    # Берем первую букву имени, первую букву отчества и фамилию
    login = f"{first_name[0]}{middle_name[0]}-{last_name}"
    return login.lower()  # Приводим к нижнему регистру

# Функция для создания пользователя в Active Directory
def create_ad_user(first_name, middle_name, last_name, login):
    # Указываем контейнер, в котором будет создан пользователь (например, "OU=Users,DC=example,DC=com")
    container = adcontainer.ADContainer.from_dn("OU=Users,DC=example,DC=com")
    
    # Генерация пароля
    password = generate_password()
    
    # Создаем пользователя
    new_user = aduser.ADUser.create(
        name=login,  # Логин пользователя
        container=container,
        password=password,  # Используем сгенерированный пароль
        upn_suffix="example.com",  # Суффикс UPN (User Principal Name)
        enabled=True  # Активируем учетную запись
    )
    
    # Устанавливаем дополнительные атрибуты
    new_user.update_attribute("givenName", first_name)  # Имя
    new_user.update_attribute("initials", middle_name[0])  # Инициал отчества
    new_user.update_attribute("sn", last_name)  # Фамилия
    new_user.update_attribute("displayName", f"{first_name} {last_name}")  # Отображаемое имя
    new_user.update_attribute("mail", f"{login}@example.com")  # Электронная почта
    
    print(f"Пользователь {login} создан успешно. Пароль: {password}")

# Чтение CSV-файла
def read_csv_and_create_users(file_path):
    with open(file_path, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file, delimiter=';')
        for row in reader:
            first_name = row['Имя']
            middle_name = row['Отчество']
            last_name = row['Фамилия']
            
            # Генерация логина
            login = generate_login(first_name, middle_name, last_name)
            
            # Создание пользователя в Active Directory
            create_ad_user(first_name, middle_name, last_name, login)

# Путь к CSV-файлу
csv_file_path = "users.csv"

# Запуск процесса
read_csv_and_create_users(csv_file_path)
