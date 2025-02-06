from ldap3 import Server, Connection, ALL

LDAP_SERVER = "ldap://192.168.10.25"
ADMIN_DN = "api@aues.kz"  # Попробуй UPN
ADMIN_PASSWORD = "f5e878db0aA"

try:
    server = Server(LDAP_SERVER, get_info=ALL)
    conn = Connection(server, user=ADMIN_DN, password=ADMIN_PASSWORD, auto_bind=False)

    if conn.bind():
        print("Успешно подключено!")
    else:
        print("Ошибка подключения:", conn.result)

    conn.unbind()
except Exception as e:
    print("Ошибка:", e)