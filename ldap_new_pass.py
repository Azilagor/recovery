import random
import string
from ldap3 import Server, Connection, MODIFY_REPLACE


# 🔹 Конфиг AD (замени на свои данные)
LDAP_SERVER = "ldaps://192.168.10.25"
ADMIN_DN = "api@aues.kz"  # Логин сервисного аккаунта
ADMIN_PASSWORD = "f5e878db0aA"
BASE_DN = "OU=aues,DC=aues,DC=kz"  # Базовый DN

# 🔹 Генерация нового пароля
def generate_password(length=6):
    chars = string.ascii_letters + string.digits + "!@#$%^&*"
    return ''.join(random.choice(chars) for _ in range(length))

# 🔹 Смена пароля в AD
def reset_user_password(username):
    try:
        server = Server(LDAP_SERVER)
        conn = Connection(server, user=ADMIN_DN, password=ADMIN_PASSWORD, auto_bind=True)

       # Ищем пользователя в AD
        search_filter = f"(sAMAccountName={username})"
        conn.search(BASE_DN, search_filter, attributes=["distinguishedName"])
        
        if not conn.entries:
            print(f"❌ Пользователь {username} не найден в AD")
            return None
        
        user_dn = conn.entries[0].distinguishedName.value
        new_password = generate_password()

        # Изменяем пароль
        conn.modify(user_dn, {'unicodePwd': [(MODIFY_REPLACE, [f'"{new_password}"'.encode('utf-16-le')])]})

        if conn.result['result'] == 0:
            print(f"✅ Пароль успешно сброшен для {username}: {new_password}")
            return new_password
        else:
            print(f"❌ Ошибка при смене пароля: {conn.result}")
            return None

    except Exception as e:
        print(f"❌ Ошибка: {e}")
        return None





# 🔹 Основной процесс
username = "d.nurlubay"  # Укажи логин пользователя в AD


new_password = reset_user_password(username)

if new_password:
    message = f"Ваш новый пароль: {new_password}"
