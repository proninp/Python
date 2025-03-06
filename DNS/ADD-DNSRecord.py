import csv
import subprocess

# Функция для создания DNS-записи
def create_dns_record(name, ip, record_type):
    try:
        if record_type.upper() == "A":
            # Создание A-записи
            command = f"Add-DnsServerResourceRecordA -Name '{name}' -ZoneName 'example.com' -IPv4Address '{ip}'"
        elif record_type.upper() == "PTR":
            # Создание PTR-записи
            command = f"Add-DnsServerResourceRecordPtr -Name '{name}' -ZoneName '1.168.192.in-addr.arpa' -PtrDomainName '{ip}'"
        elif record_type.upper() == "CNAME":
            # Создание CNAME-записи
            command = f"Add-DnsServerResourceRecordCName -Name '{name}' -ZoneName 'example.com' -HostNameAlias '{ip}'"
        else:
            print(f"Неизвестный тип записи: {record_type}")
            return

        # Выполнение команды PowerShell
        result = subprocess.run(["powershell", "-Command", command], capture_output=True, text=True)
        
        if result.returncode == 0:
            print(f"Запись {record_type} для {name} создана успешно.")
        else:
            print(f"Ошибка при создании записи {record_type} для {name}: {result.stderr}")
    except Exception as e:
        print(f"Ошибка: {e}")

# Чтение CSV-файла
def read_csv_and_create_records(file_path):
    with open(file_path, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file, delimiter=';')
        for row in reader:
            name = row['Имя']
            ip = row['IP']
            record_type = row['Тип']
            
            # Создание DNS-записи
            create_dns_record(name, ip, record_type)

# Путь к CSV-файлу
csv_file_path = "dns_records.csv"

# Запуск процесса
read_csv_and_create_records(csv_file_path)
