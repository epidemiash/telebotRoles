import sqlite3
import telebot
import time
from telebot import types
from telebot.types import ChatPermissions
import threading

bot = telebot.TeleBot('YOUR_TOKEN')


# Подключение к базе данных
conn = sqlite3.connect('roles.db', check_same_thread=False)
cursor = conn.cursor()

# Создание таблицы, если она не существует
cursor.execute('''CREATE TABLE IF NOT EXISTS user_roles
                (user_id INTEGER PRIMARY KEY, role TEXT)''')

# Функция для обновления роли пользователя в базе данных
def update_user_role(user_id, role):
    cursor.execute("REPLACE INTO user_roles (user_id, role) VALUES (?, ?)", (user_id, role))
    conn.commit()

# Функция для удаления сообщения через заданное время
def delete_message(chat_id, message_id, delay):
    time.sleep(delay)
    bot.delete_message(chat_id, message_id)

# Функция удаления пользователя из таблицы
def delete_user_by_role(role):
    try:
        cursor.execute("DELETE FROM user_roles WHERE role=?", (role,))
        conn.commit()
        print(f"Записи с ролью '{role}' успешно удалены из базы данных.")
    except sqlite3.Error as error:
        print(f"Ошибка при удалении записей: {error}")

# Функция для получения роли пользователя из базы данных
def get_user_role(user_id):
    cursor.execute("SELECT role FROM user_roles WHERE user_id=?", (user_id,))
    row = cursor.fetchone()
    if row:
        return row[0]
    return None

# Обработчик команды
@bot.message_handler(func=lambda message: True)
def process_message(message):
    user_id = message.from_user.id
    chat_id = message.chat.id
    role = get_user_role(user_id)
    # первым делом проверяем роль пользователя который пишет и если он не админ
    if role and message.from_user.id != ADMIN_ID:
        # проверяем остальные сообщения
        # если уже есть роль Т77
        member = bot.get_chat_member(chat_id, user_id)
        if member.status == 'administrator' and '!car' in message.text.lower():
            greeting_messagez = bot.send_message(chat_id, f'<b>⚠️ Вам нужно подождать некоторое время! \n\nНе пишите в чат ничего около 3х минут, после попробуйте снова ввести команду для смены роли.</b>', parse_mode='html')
            greeting_message_idz = greeting_messagez.message_id
            delete_message(message.chat.id, greeting_message_idz, 10)
            # роль имеется или выдана была повторно, удаляем ее через некоторое время
            def remove_role(chat_id, user_id):
                bot.restrict_chat_member(chat_id, user_id, can_send_messages=True)
                #greeting_messagez = bot.send_message(chat_id, f'<b>❌ Роль была удалена.</b>', parse_mode='html')
                #greeting_message_idz = greeting_messagez.message_id
                #delete_message(message.chat.id, greeting_message_idz, 10)
            t = threading.Timer(600, remove_role, args=(chat_id, user_id))
            t.start()
        elif '!car' in message.text.lower():
            # обновляем роль в БД
            if message.text.lower() == '!car t99':
                update_user_role(user_id, 't99')
                greeting_messagez = bot.send_message(chat_id, f'<b>🔁 Роль в базе обновлена на T99</b>', parse_mode='html')
                greeting_message_idz = greeting_messagez.message_id
                delete_message(message.chat.id, greeting_message_idz, 5)
                delete_message(chat_id, greeting_messagez.message_id - 1, 1)  # Удаление предыдущего сообщения
            elif message.text.lower() == '!car t77':
                update_user_role(user_id, 't77')
                greeting_messagez = bot.send_message(chat_id, f'<b>🔁 Роль в базе обновлена на T77</b>', parse_mode='html')
                greeting_message_idz = greeting_messagez.message_id
                delete_message(message.chat.id, greeting_message_idz, 5)
                delete_message(chat_id, greeting_messagez.message_id - 1, 1)  # Удаление предыдущего сообщения
            elif message.text.lower() == '!car t55':
                update_user_role(user_id, 't55')
                greeting_messagez = bot.send_message(chat_id, f'<b>🔁 Роль в базе обновлена на T55</b>', parse_mode='html')
                greeting_message_idz = greeting_messagez.message_id
                delete_message(message.chat.id, greeting_message_idz, 5)
                delete_message(chat_id, greeting_messagez.message_id - 1, 1)  # Удаление предыдущего сообщения
            elif message.text.lower() == '!car b70':
                update_user_role(user_id, 'b70')
                greeting_messagez = bot.send_message(chat_id, f'<b>🔁 Роль в базе обновлена на B70</b>', parse_mode='html')
                greeting_message_idz = greeting_messagez.message_id
                delete_message(message.chat.id, greeting_message_idz, 5)
                delete_message(chat_id, greeting_messagez.message_id - 1, 1)  # Удаление предыдущего сообщения
        else:
            # если пользователь числится в БД с ролью то выдаем повторно ему в чате роль
            bot.promote_chat_member(chat_id, user_id, can_change_info=False, can_post_messages=True, can_edit_messages=False, can_delete_messages=False, can_invite_users=False, can_restrict_members=False, can_pin_messages=True, can_promote_members=False)
            bot.set_chat_administrator_custom_title(chat_id, user_id, role)
            #greeting_messagez = bot.send_message(chat_id, f'<b>🔆 Роль выдана повторно на 30 сек.</b>', parse_mode='html')
            #greeting_message_idz = greeting_messagez.message_id
            #delete_message(message.chat.id, greeting_message_idz, 10)
            def remove_role(chat_id, user_id):
                bot.restrict_chat_member(chat_id, user_id, can_send_messages=True)
                #greeting_messagez = bot.send_message(chat_id, f'<b>❌ Роль была удалена.</b>', parse_mode='html')
                #greeting_message_idz = greeting_messagez.message_id
                #delete_message(message.chat.id, greeting_message_idz, 10)
            t = threading.Timer(120, remove_role, args=(chat_id, user_id))
            t.start()
    elif not role:
        if message.text.lower() == '!car t77':
            # Если пользователь новый делаем запись с ролью, если существующий делаем update
            update_user_role(user_id, 't77')
            try:
                # выдаем права админа и ставим заголовок т77
                bot.promote_chat_member(chat_id, user_id, can_change_info=False, can_post_messages=True, can_edit_messages=False, can_delete_messages=False, can_invite_users=False, can_restrict_members=False, can_pin_messages=True, can_promote_members=False)
                bot.set_chat_administrator_custom_title(chat_id, user_id, 't77')
                greeting_messagez = bot.send_message(chat_id, f'<b>✅ Роль t77 была добавлена.</b>', parse_mode='html')
                greeting_message_idz = greeting_messagez.message_id
                delete_message(message.chat.id, greeting_message_idz, 5)
                delete_message(chat_id, greeting_messagez.message_id - 1, 1)  # Удаление предыдущего сообщения
            except Exception as e:
                print(f"Ошибка: {e}")   
        elif message.text.lower() == '!car t99':
            # Если пользователь новый делаем запись с ролью, если существующий делаем update
            update_user_role(user_id, 't99')
            try:
                # выдаем права админа и ставим заголовок т99
                bot.promote_chat_member(chat_id, user_id, can_change_info=False, can_post_messages=True, can_edit_messages=False, can_delete_messages=False, can_invite_users=False, can_restrict_members=False, can_pin_messages=True, can_promote_members=False)
                bot.set_chat_administrator_custom_title(chat_id, user_id, 't99')
                greeting_messagez = bot.send_message(chat_id, f'<b>✅ Роль t99 была добавлена.</b>', parse_mode='html')
                greeting_message_idz = greeting_messagez.message_id
                delete_message(message.chat.id, greeting_message_idz, 5)
                delete_message(chat_id, greeting_messagez.message_id - 1, 1)  # Удаление предыдущего сообщения
            except Exception as e:
                print(f"Ошибка: {e}")   
        elif message.text.lower() == '!car t55':
                    # Если пользователь новый делаем запись с ролью, если существующий делаем update
                    update_user_role(user_id, 't55')
                    try:
                        # выдаем права админа и ставим заголовок т55
                        bot.promote_chat_member(chat_id, user_id, can_change_info=False, can_post_messages=True, can_edit_messages=False, can_delete_messages=False, can_invite_users=False, can_restrict_members=False, can_pin_messages=True, can_promote_members=False)
                        bot.set_chat_administrator_custom_title(chat_id, user_id, 't55')
                        greeting_messagez = bot.send_message(chat_id, f'<b>✅ Роль t55 была добавлена.</b>', parse_mode='html')
                        greeting_message_idz = greeting_messagez.message_id
                        delete_message(message.chat.id, greeting_message_idz, 5)
                        delete_message(chat_id, greeting_messagez.message_id - 1, 1)  # Удаление предыдущего сообщения
                    except Exception as e:
                        print(f"Ошибка: {e}")   
        elif message.text.lower() == '!car b70':
                    # Если пользователь новый делаем запись с ролью, если существующий делаем update
                    update_user_role(user_id, 'b70')
                    try:
                        # выдаем права админа и ставим заголовок b70
                        bot.promote_chat_member(chat_id, user_id, can_change_info=False, can_post_messages=True, can_edit_messages=False, can_delete_messages=False, can_invite_users=False, can_restrict_members=False, can_pin_messages=True, can_promote_members=False)
                        bot.set_chat_administrator_custom_title(chat_id, user_id, 'b70')
                        greeting_messagez = bot.send_message(chat_id, f'<b>✅ Роль b70 была добавлена.</b>', parse_mode='html')
                        greeting_message_idz = greeting_messagez.message_id
                        delete_message(message.chat.id, greeting_message_idz, 5)
                        delete_message(chat_id, greeting_messagez.message_id - 1, 1)  # Удаление предыдущего сообщения
                    except Exception as e:
                        print(f"Ошибка: {e}")   
        else:
            #greeting_messagez = bot.send_message(chat_id, f'<b>🚫 У вас еще нет ролей.</b>', parse_mode='html')
            #greeting_message_idz = greeting_messagez.message_id
            #delete_message(message.chat.id, greeting_message_idz, 10)
            # Создаем клавиатуру с кнопками
            if message.from_user.id != 621803254:
                keyboard = types.InlineKeyboardMarkup()
                button_t77 = types.InlineKeyboardButton("T77", callback_data='add_role_t77')
                button_t55 = types.InlineKeyboardButton("T55", callback_data='add_role_t55')
                button_t99 = types.InlineKeyboardButton("T99", callback_data='add_role_t99')
                button_b70 = types.InlineKeyboardButton("B70", callback_data='add_role_b70')
                button_other = types.InlineKeyboardButton("У меня нет авто или другой", callback_data='add_other')

                keyboard.add(button_t77, button_t55)
                keyboard.add(button_t99, button_b70)
                keyboard.add(button_other)
                # Отправляем сообщение с клавиатурой
                greeting_messagez = bot.send_message(chat_id, f'\n\
<b>🚫 У вас еще нет ролей в группе!</b>\n\n\
Укажите свой автомобиль FAW для получения роли.\n\n\
<i>Ваш ID: {message.from_user.id}</i>', reply_markup=keyboard, parse_mode='html')
                greeting_message_idz = greeting_messagez.message_id
                delete_message(message.chat.id, greeting_message_idz, 60)
    
# Обработчик нажатий на кнопки
@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    user_id = call.from_user.id
    message = call.message  # Получаем объект сообщения, связанного с callback_query
    chat_id = message.chat.id  # Получаем chat_id из сообщения

    if call.data == 'add_role_t77':
        update_user_role(user_id, 't77')
        greeting_messagez = bot.send_message(chat_id, f'<b>✅ Вы выбрали роль T77!</b>', parse_mode='html')
        greeting_message_idz = greeting_messagez.message_id
        delete_message(chat_id, greeting_message_idz, 5)
        delete_message(chat_id, greeting_messagez.message_id - 1, 1)  # Удаление предыдущего сообщения
    elif call.data == 'add_role_t55':
        update_user_role(user_id, 't55')
        greeting_messagez = bot.send_message(chat_id, f'<b>✅ Вы выбрали роль T55!</b>', parse_mode='html')
        greeting_message_idz = greeting_messagez.message_id
        delete_message(chat_id, greeting_message_idz, 5)
        delete_message(chat_id, greeting_messagez.message_id - 1, 1)  # Удаление предыдущего сообщения
    elif call.data == 'add_role_t99':
        update_user_role(user_id, 't99')
        greeting_messagez = bot.send_message(chat_id, f'<b>✅ Вы выбрали роль T99!</b>', parse_mode='html')
        greeting_message_idz = greeting_messagez.message_id
        delete_message(chat_id, greeting_message_idz, 5)
        delete_message(chat_id, greeting_messagez.message_id - 1, 1)  # Удаление предыдущего сообщения
    elif call.data == 'add_role_b70':
        update_user_role(user_id, 'b70')
        greeting_messagez = bot.send_message(chat_id, f'<b>✅ Вы выбрали роль B70!</b>', parse_mode='html')
        greeting_message_idz = greeting_messagez.message_id
        delete_message(chat_id, greeting_message_idz, 5)  
        delete_message(chat_id, greeting_messagez.message_id - 1, 1)  # Удаление предыдущего сообщения  
    elif call.data == 'add_other':
        update_user_role(user_id, 'гость')
        greeting_messagez = bot.send_message(chat_id, f'<b>✅ Вам выдана роль гостя.</b>', parse_mode='html')
        greeting_message_idz = greeting_messagez.message_id
        delete_message(chat_id, greeting_message_idz, 5)  
        delete_message(chat_id, greeting_messagez.message_id - 1, 1)  # Удаление предыдущего сообщения

while True: 
    try: 
        bot.polling(none_stop=True)  
    except Exception as e:  
        time.sleep(3) 
        print(e) 
