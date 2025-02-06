from ldap3 import Server, Connection, ALL, MODIFY_REPLACE
import generate_pass

LDAP_SERVER = "ldap://192.168.10.25"
ADMIN_DN = "CN=api,OU=aues,DC=aues,DC=kz"  # Указал admin DN
ADMIN_PASSWORD = "f5e878db0aA"  # Пароль из конфига

def reset_user_password(user_dn, new_password):
    try:
        server = Server(LDAP_SERVER, get_info=ALL)
        conn = Connection(server, user=ADMIN_DN, password=ADMIN_PASSWORD, auto_bind=True)

        # Обновляем пароль пользователя
        conn.modify(user_dn, {'unicodePwd': [(MODIFY_REPLACE, [f'"{new_password}"'.encode('utf-16-le')])]})

        if conn.result['result'] == 0:
            print("Пароль успешно сброшен:", new_password)
            return True
        else:
            print("Ошибка при смене пароля:", conn.result)
            return False

        conn.unbind()
    except Exception as e:
        print("Ошибка:", e)
        return False

# Пример вызова
user_dn = "CN=a.bakdaulet,OU=users,OU=DIT,OU=Сотрудники,OU=aues,DC=aues,DC=kz"
new_password = "NewSecurePass123!"
# new_password = generate_pass.generate_password()
if reset_user_password(user_dn, new_password):
    print("Пароль изменен на:", new_password)
