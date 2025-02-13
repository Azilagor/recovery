from django.shortcuts import render, redirect
from django.contrib import messages
from django.conf import settings
import random
import string
from datetime import datetime
from ldap3 import Server, Connection, MODIFY_REPLACE, ALL

def generate_password(length=12):
    """Генерирует случайный пароль"""
    chars = string.ascii_letters + string.digits + "!@#$%^&*"
    return ''.join(random.choice(chars) for _ in range(length))

def password_reset(request):
    if request.method == 'POST':
        # Получаем данные из формы
        user_input  = request.POST.get('user', '').strip()
        mail_input  = request.POST.get('mail', '').strip().lower()
        phone_input = request.POST.get('phone', '').strip()
        
        # Подключение к AD
        LDAP_SERVER    = settings.LDAP_SERVER
        ADMIN_DN       = settings.ADMIN_DN
        ADMIN_PASSWORD = settings.ADMIN_PASSWORD
        BASE_DN        = settings.BASE_DN
        
        try:
            server = Server(LDAP_SERVER, get_info=ALL)
            conn = Connection(server, user=ADMIN_DN, password=ADMIN_PASSWORD, auto_bind=True)
        except Exception as e:
            messages.error(request, f"Ошибка подключения к AD: {e}")
            return redirect('password_reset')
        
        # Поиск пользователя по samaccountname
        search_filter = f"(samaccountname={user_input})"
        attributes = ["samaccountname", "mail", "TelService", "DateService"]
        conn.search(BASE_DN, search_filter, attributes=attributes)
        
        if not conn.entries:
            messages.error(request, "Введённая информация неверна!")
            conn.unbind()
            return redirect('password_reset')
        
        entry = conn.entries[0]
        ldap_user  = entry.samaccountname.value if 'samaccountname' in entry else ""
        ldap_mail  = entry.mail.value if 'mail' in entry else ""
        ldap_phone = entry.TelService.value if 'TelService' in entry else ""
        ldap_date  = entry.DateService.value if 'DateService' in entry else ""
        
        # Если каких-либо обязательных данных нет — выдаём ошибку
        if not ldap_user or not ldap_mail or not ldap_phone:
            messages.error(request, "Введённая информация неверна!")
            conn.unbind()
            return redirect('password_reset')
        
        # Сравниваем введённые данные с данными AD (без учета регистра для email и логина)
        if (user_input.lower() != ldap_user.lower() or 
            mail_input != ldap_mail.lower() or 
            phone_input != ldap_phone):
            messages.error(request, "Введённая информация неверна!")
            conn.unbind()
            return redirect('password_reset')
        
        # Проверяем, менялся ли пароль сегодня (DateService)
        today = datetime.today().strftime("%Y-%m-%d")
        if ldap_date == today:
            messages.error(request, "Нельзя менять пароль больше 1 раза в день!")
            conn.unbind()
            return redirect('password_reset')
        
        # Всё совпало — сбрасываем пароль
        new_password = generate_password()
        # Для изменения пароля AD требует, чтобы значение было в двойных кавычках и закодировано в UTF-16LE
        unicode_password = f'"{new_password}"'.encode('utf-16-le')
        modify_result = conn.modify(entry.entry_dn, {'unicodePwd': [(MODIFY_REPLACE, [unicode_password])]})
        if not modify_result:
            messages.error(request, f"Ошибка при смене пароля: {conn.result}")
            conn.unbind()
            return redirect('password_reset')
        
        # Обновляем атрибут DateService на сегодняшнюю дату
        conn.modify(entry.entry_dn, {'DateService': [(MODIFY_REPLACE, [today])]})
        
        # Здесь можно добавить функцию отправки SMS с новым паролем на номер ldap_phone
        
        messages.success(request, f"Ваш пароль сброшен. Новый пароль: {new_password} отправлен на телефон {ldap_phone}")
        conn.unbind()
        return redirect('password_reset')
    
    # GET-запрос — просто отображаем форму
    return render(request, 'accounts/password_reset_form.html')
