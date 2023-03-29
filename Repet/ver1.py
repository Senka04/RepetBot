# 5647455347:AAF9z0QXluG0H_PS-FBLl7Ns4KuaGIUKGdw    ---  токен основного тг бота
# 6056581598:AAE2PJh18SM2b46k8Y_VPxAHPow74jhGuhA    ---  токен тестового тг бота

#from background import keep_alive  # для деплоя
import telebot
from telebot import types

import sqlite3

flag_stud_check = 1
flag_delete_stud = 0
stud_change_mode = 0
stud_add_mode = 0
API_TOKEN = '6056581598:AAE2PJh18SM2b46k8Y_VPxAHPow74jhGuhA'
bot = telebot.TeleBot(API_TOKEN)
my_chat_id = -950145694
admin_id = 1384713698
stud_name = 'пользователь'


@bot.message_handler(commands=['start'])
def start(message):
    create_table()
    bot.send_message(message.chat.id, stud_check(message)[0], reply_markup=create_markup(message))


def create_table():
    db = sqlite3.connect('Repet/students.db')
    cursor = db.cursor()
    cursor.execute("""CREATE TABLE IF NOT EXISTS students(
    id integer,
    name text
    )""")
    db.commit()
    cursor.close()
    db.close()


def stud_print(message):
    db = sqlite3.connect('Repet/students.db')
    cursor = db.cursor()
    stud_id_int = int(message.chat.id)
    cursor.execute("SELECT * FROM students")
    items = cursor.fetchall()

    for el in items:
        bot.send_message(message.chat.id, f'name: {el[1]}, id: {el[0]}', reply_markup=create_markup(message))
    db.commit()
    cursor.close()
    db.close()


def stud_check(message):
    global flag_stud_check, stud_name, stud_add_mode
    flag_stud_check = 1
    db = sqlite3.connect('Repet/students.db')
    cursor = db.cursor()
    stud_id_int = int(message.chat.id)
    cursor.execute("SELECT * FROM students")
    items = cursor.fetchall()

    for el in items:
        if stud_id_int == int(el[0]):
            flag_stud_check = 0
            stud_name = el[1]

    if flag_stud_check == 1:
        stroka = "Напиши, пожалуйста, своё имя"
        stud_add_mode = 1
    else:
        stroka = "Привет, {name}!".format(name=stud_name)

    db.commit()
    cursor.close()
    db.close()

    return_info = [stroka, flag_stud_check]
    return return_info


def delete_stud(message):
    text = 'Ученик не найден'
    stud_id_int = int(message.text)
    db = sqlite3.connect('Repet/students.db')
    cursor = db.cursor()
    cursor.execute("SELECT * FROM students")
    items = cursor.fetchall()
    for el in items:
        if stud_id_int == int(el[0]):
            text = 'Ученик удалён'
            cursor.execute("DELETE FROM students WHERE id=(?)", [stud_id_int])

    db.commit()
    cursor.close()
    db.close()
    return text


def stud_add(message):
    global stud_name, stud_change_mode, stud_add_mode

    db = sqlite3.connect('Repet/students.db')
    cursor = db.cursor()

    stud_id_int = int(message.chat.id)
    local_stud_name = '{name}'.format(name=message.text)

    if stud_change_mode == 1:
        cursor.execute("UPDATE students SET name=(?) WHERE id=(?)", [local_stud_name, stud_id_int])
        bot.send_message(message.chat.id, 'Изменил', reply_markup=create_markup(message))

    else:
        stud = [(stud_id_int, local_stud_name)]
        cursor.executemany("INSERT INTO students VALUES (?,?)", stud)
        bot.send_message(message.chat.id, 'Записал', reply_markup=create_markup(message))

    stud_change_mode = 0
    stud_add_mode = 0

    stud_name = 'пользователь'
    db.commit()
    cursor.close()
    db.close()
    return local_stud_name


@bot.message_handler(content_types=['text'])
def name(message):
    global flag_delete_stud, stud_change_mode, stud_add_mode
    buttons = ['Перезапуск', 'Ютуб', 'Яндекс Дзен', 'Запросить ДЗ', 'Список учеников', 'Изменить имя',
               'Удалить ученика', 'ОТМЕНА']
    for items in buttons:
        if message.text == items:
            on_click(message)
            return
    else:
        if stud_add_mode == 0 and stud_change_mode == 0 and flag_delete_stud == 0:
            bot.send_message(message.chat.id, 'OK', parse_mode='html')
        elif stud_add_mode == 1 or stud_change_mode == 1:
            stud_add(message)
        elif flag_delete_stud == 1 and message.chat.id == admin_id:
            bot.send_message(admin_id, delete_stud(message))
            flag_delete_stud = 0


def on_click(message):
    global flag_delete_stud
    if message.text == 'Изменить имя':
        if (stud_check(message)[1] == 0):
            global stud_change_mode
            bot.send_message(message.chat.id, 'Напиши новое имя', reply_markup=create_markup(message))
            stud_change_mode = 1
        else:
            bot.send_message(message.chat.id, stud_check(message)[0], reply_markup=create_markup(message))

    if message.text == 'Запросить ДЗ':
        if (stud_check(message)[1] == 0):
            fileDoc = open('Repet/15(1-10).pdf', 'rb')
            bot.send_document(message.chat.id, fileDoc)
            fileDoc = open('Repet/14.jpg', 'rb')
            bot.send_photo(message.chat.id, fileDoc)


        else:
            bot.send_message(message.chat.id, stud_check(message)[0], reply_markup=create_markup(message))

    elif message.text == 'Ютуб':
        if (stud_check(message)[1] == 0):
            bot.send_message(message.chat.id,
                             'Вот ссылка: https://www.youtube.com/@ed_az/videos')
        else:
            bot.send_message(message.chat.id, stud_check(message)[0], reply_markup=create_markup(message))
    elif message.text == 'Яндекс Дзен':
        if (stud_check(message)[1] == 0):
            bot.send_message(
                message.chat.id,
                'Вот ссылка: https://dzen.ru/id/63fbaeb55003113bb618219c?share_to=link')
        else:
            bot.send_message(message.chat.id, stud_check(message)[0], reply_markup=create_markup(message))
    elif message.text == 'Перезапуск':
        start(message)
    elif message.text == '/start':
        start(message)
    elif message.text == 'Список учеников' and message.chat.id == admin_id:
        stud_print(message)
    elif message.text == 'Удалить ученика' and message.chat.id == admin_id:
        global flag_delete_stud
        flag_delete_stud = 1
        bot.send_message(admin_id,
                         'Напиши id ученика, которого надо удалить, либо ОТМЕНА, если нажал случайно')
    elif message.text == 'ОТМЕНА' and flag_delete_stud == 1 and message.chat.id == admin_id:
        flag_delete_stud = 0


@bot.message_handler(content_types=['photo'])
def get_photo(message):
    if (stud_check(message)[1] == 0):
        bot.send_photo(my_chat_id, message.photo[-1].file_id)
        bot.send_message(message.chat.id, '<b> Гуд, спасибо!</b>', parse_mode='html')
    else:
        bot.send_message(message.chat.id, stud_check(message)[0], reply_markup=create_markup(message))


@bot.message_handler(content_types=['document'])
def get_document(message):
    if (stud_check(message)[1] == 0):
        bot.send_document(my_chat_id, message.document.file_id)
        bot.send_message(message.chat.id, '<b> Гуд, спасибо!</b>', parse_mode='html')
    else:
        bot.send_message(message.chat.id, stud_check(message)[0], reply_markup=create_markup(message))


def create_markup(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    yt = types.InlineKeyboardButton('Ютуб')
    dzen = types.InlineKeyboardButton('Яндекс Дзен')
    callDZ = types.InlineKeyboardButton('Запросить ДЗ')
    restart = types.InlineKeyboardButton('Перезапуск')
    changeName = types.InlineKeyboardButton('Изменить имя')

    if message.chat.id == admin_id:
        adminBtn1 = types.InlineKeyboardButton('Список учеников')
        adminBtn2 = types.InlineKeyboardButton('Удалить ученика')
        markup.add(changeName, adminBtn1, adminBtn2, yt, dzen, callDZ, restart)
    else:
        markup.add(changeName, yt, dzen, callDZ, restart)
    return markup


#keep_alive()  # для деплоя
bot.polling(none_stop=True)
