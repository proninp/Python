import os
import csv
from ldap3 import Server, Connection, ALL, MODIFY_ADD

# Настройки подключения к Active Directory
AD_SERVER = 'ldap://your-ad-server'
AD_USER = 'your-username'
AD_PASSWORD = 'your-password'
AD_BASE_DN = 'dc=example,dc=com'

# Путь к каталогу, где находятся файлы
current_path = os.path.dirname(os.path.realpath(__file__))
input_folder = os.path.join(current_path, 'Input')

# Функция для добавления пользователя в группу
def add_user_to_group(user, group):
    try:
        # Создаем подключение к AD
        server = Server(AD_SERVER, get_info=ALL)
        conn = Connection(server, user=AD_USER, password=AD_PASSWORD, auto_bind=True)
        
        # Формируем DN (Distinguished Name) для пользователя и группы
        user_dn = f'CN={user},CN=Users,{AD_BASE_DN}'
        group_dn = f'CN={group},CN=Users,{AD_BASE_DN}'
        
        # Добавляем пользователя в группу
        conn.modify(group_dn, {'member': [(MODIFY_ADD, [user_dn])]})
        
        if conn.result['result'] == 0:
            print(f"[SUCCESS] The account {user} has been added to the {group}")
        else:
            print(f"[ERROR] Failed to add {user} to {group}: {conn.result['description']}")
    except Exception as e:
        print(f"[ERROR] Exception occurred: {e}")

# Обрабатываем все CSV-файлы в папке Input
for filename in os.listdir(input_folder):
    if filename.endswith('.csv'):
        file_path = os.path.join(input_folder, filename)
        with open(file_path, mode='r', encoding='utf-8') as file:
            reader = csv.DictReader(file, delimiter=';')
            for row in reader:
                user = row['SamAccountName']
                group = row['Group']
                add_user_to_group(user, group)
