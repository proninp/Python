from ldap3 import Server, Connection, ALL, MODIFY_ADD, MODIFY_REPLACE
import logging

def add_ad_subnet(subnet, site_name, description=None, location=None):
    """
    Добавляет подсеть в Active Directory.

    :param subnet: Имя подсети (например, "192.168.10.0/24")
    :param site_name: Имя сайта, к которому будет привязана подсеть
    :param description: Описание подсети (опционально)
    :param location: Местоположение подсети (опционально)
    """
    try:
        # Настройка логирования
        logging.basicConfig(level=logging.INFO)
        logger = logging.getLogger(__name__)

        # Подключение к серверу LDAP
        server = Server('ldap://your_domain_controller', get_info=ALL)
        conn = Connection(server, user='your_username', password='your_password', auto_bind=True)

        # Получение конфигурационного контекста
        conn.search('', '(objectClass=*)', attributes=['configurationNamingContext'])
        configuration_naming_context = conn.entries[0].configurationNamingContext.value

        # Путь к контейнеру подсетей
        subnets_container_dn = f'CN=Subnets,CN=Sites,{configuration_naming_context}'

        # Создание объекта подсети
        subnet_dn = f'CN={subnet},{subnets_container_dn}'
        conn.add(subnet_dn, ['top', 'subnet'])

        # Привязка подсети к сайту
        site_dn = f'CN={site_name},CN=Sites,{configuration_naming_context}'
        conn.modify(subnet_dn, {'siteObject': [(MODIFY_ADD, [site_dn])]})

        # Добавление описания, если указано
        if description:
            conn.modify(subnet_dn, {'description': [(MODIFY_ADD, [description])]})

        # Добавление местоположения, если указано
        if location:
            conn.modify(subnet_dn, {'location': [(MODIFY_ADD, [location])]})

        logger.info(f"Подсеть {subnet} успешно добавлена.")

    except Exception as e:
        logger.error(f"Ошибка при добавлении подсети: {e}")
    finally:
        conn.unbind()

if __name__ == "__main__":
    # Пример использования функции
    add_ad_subnet(
        subnet="192.168.10.0/24",
        site_name="MTL1",
        description="Workstations VLAN 110",
        location="Montreal, Canada"
    )
