# -*- coding: utf8 -*-

import telebot
from telebot import types
from traceback import print_exc
from io import StringIO
import random
from database import *
from tables import *
from variables import *
import re
from operator import itemgetter
# from pprint import pprint

bot = telebot.TeleBot(Token) # , threaded=False
BOT_USER = 1875045403


def f_queue(m):
    """антиспам повідомлення"""
    global queue, t_queue
    if m.from_user.id in queue:
        if t_queue > time.time():
            try:
                bot.send_message(m.chat.id, f'Занадто часто!')
            except:
                pass
            queue.append(m.from_user.id)
            del (queue[0])
            t_queue = time.time() + 0.2
            return True
        else:
            queue.append(m.from_user.id)
            del (queue[0])
            t_queue = time.time() + 0.2
    else:
        queue.append(m.from_user.id)
        del (queue[0])
        t_queue = time.time() + 0.2
    return False


def extract_unique_code(text):
    return text.split()[1] if len(text.split()) > 1 else ''


def f_queue_call(call):
    '''антиспам кнопки'''
    global queue_call, t_queue_call
    if call.from_user.id in queue_call:
        if t_queue_call > time.time():
            bot.answer_callback_query(callback_query_id=call.id, text='Занадто часто.', show_alert=True)
            queue_call.append(call.from_user.id)
            del (queue_call[0])
            t_queue_call = time.time() + 0.1
            return True
        else:
            queue_call.append(call.from_user.id)
            del (queue_call[0])
            t_queue_call = time.time() + 0.1
    else:
        queue_call.append(call.from_user.id)
        del (queue_call[0])
        t_queue_call = time.time() + 0.1
    return False


def main_menu(m, lab):
    """головне меню"""
    keyboard = types.InlineKeyboardMarkup()
    url_button = types.InlineKeyboardButton(text="💬 Основний чат Ячмінії",
                                            url='https://t.me/Yachminiya')
    keyboard.add(url_button)
    callback_button = types.InlineKeyboardButton(text="🗺 Простір Ячмінії", callback_data="prostir")
    keyboard.add(callback_button)
    callback_button = types.InlineKeyboardButton(text="🗳 Голосування", callback_data="golos")
    keyboard.add(callback_button)
    callback_button = types.InlineKeyboardButton(text="⚖️ Cуд", callback_data="sud")
    keyboard.add(callback_button)
    callback_button = types.InlineKeyboardButton(text="💡 Подати петицію", callback_data="petition")
    keyboard.add(callback_button)
    callback_button = types.InlineKeyboardButton(text="📱Спеціалізовані меню", callback_data="menus")
    keyboard.add(callback_button)
    callback_button = types.InlineKeyboardButton(text="ℹ️ Інформація", callback_data="all_info")
    keyboard.add(callback_button)
    if lab:
        bot.edit_message_text(chat_id=m.chat.id, message_id=m.message_id,
                              text='Вас вітає головне меню Системи "Ячмінія".\nТут зібрані основні функції Системи.',
                              reply_markup=keyboard)
    else:
        try:
            bot.send_message(m.chat.id,
                             'Вас вітає головне меню Системи "Ячмінія".\nТут зібрані основні функції Системи.',
                             reply_markup=keyboard)
            bot.edit_message_reply_markup(m.chat.id, m.message_id, reply_markup=None)
        except:
            pass


def timeout(u, m):
    bot.send_message(m.chat.id, get_str_passport(u.id), parse_mode='HTML')


def zhan_hour(zh_id):
    if zhan_queue[zh_id] > 0:
        zhan_queue[zh_id] -= 1


def del_doc(chat_id, message_id):
    try:
        bot.delete_message(chat_id, message_id)
    except:
        pass


def glas(am):
    last_nums = int(am) % 100
    last_num = int(am) % 10
    if 10 < last_nums < 20:
        glas = 'ячок'
    elif int(last_num) % 10 in (2, 3, 4):
        glas = 'ячки'
    elif int(last_num) % 10 in (5, 6, 7, 8, 9, 0):
        glas = 'ячок'
    else:
        glas = 'ячка'
    return glas


def aktyv_r():
    '''актив'''
    global aktyv, lakt
    passports = get_all_passports()
    if false_day:
        day = false_day
    else:
        day = datetime.today().day
    month = datetime.today().month
    day_db = get_all_meta()[0][0]
    min_day = 0
    if day_db == day:
        day_is = True
    else:
        day_is = False
        insert_day_meta(day)
        if day < day_db:
            min_day = 31 - months[month_num[month - 2]][1]
    for i in passports:
        msgs = i[23].split()
        words = i[24].split()
        try:
            if day_is:
                msgs[day - 1] = str(int(msgs[day - 1]) + aktyv[i[1]][0])
                i[23] = ' '.join(msgs)
                words[day - 1] = str(int(words[day - 1]) + aktyv[i[1]][1])
                i[24] = ' '.join(words)
            else:
                if min_day:
                    for j in range(30, 30 - min_day, -1):
                        msgs[j] = '0'
                        words[j] = '0'
                msgs[day - 1] = str(aktyv[i[1]][0])
                i[23] = ' '.join(msgs)
                words[day - 1] = str(aktyv[i[1]][1])
                i[24] = ' '.join(words)
        except Exception as e:
            if not day_is:
                if min_day:
                    for j in range(30, 30 - min_day, -1):
                        msgs[j] = '0'
                        words[j] = '0'
                msgs[day - 1] = '0'
                i[23] = ' '.join(msgs)
                words[day - 1] = '0'
                i[24] = ' '.join(words)
        insert_passport_l(i)
    insert_all_passports_g(passports)
    lakt = 0
    aktyv = {}


def commission(x, mnozh):
    x = int(x)
    if x <= 8:
        n = (2 / x)
    elif x <= 16:
        n = (4 / (x + 8))
    elif x <= 32:
        n = (8 / (x + 32))
    elif x <= 64:
        n = (16 / (x + 96))
    elif x <= 128:
        n = (32 / (x + 256))
    elif x <= 256:
        n = (64 / (x + 640))
    elif x <= 512:
        n = (128 / (x + 1536))
    elif x <= 1024:
        n = (256 / (x + 3584))
    elif x <= 2048:
        n = (512 / (x + 8192))
    else:
        n = (1024 / (x + 18432))
    n *= mnozh
    n *= 0.5
    return round(x * n)


def user_link(id, *text):
    return f'<a href="tg://user?id={id}">{" ".join(text)}</a>'


def prostir_f(m, lab=True):
    keyboard = types.InlineKeyboardMarkup()
    callback_button = types.InlineKeyboardButton(text=f"🗯 Чати Ячмінії", callback_data=f"chats")
    keyboard.add(callback_button)
    callback_button = types.InlineKeyboardButton(text=f"📺 Канали Ячмінії", callback_data=f"channels")
    keyboard.add(callback_button)
    callback_button = types.InlineKeyboardButton(text="Меню керування простором Ячмінії", callback_data="prostir_menu")
    keyboard.add(callback_button)
    callback_button = types.InlineKeyboardButton(text=f"⬅️ До головного меню", callback_data=f"menul")
    keyboard.add(callback_button)
    if lab:
        bot.edit_message_text(chat_id=m.chat.id, message_id=m.message_id,
                              text='Простір Ячмінії — всі чати та канали Ячмінії, які дотримуються '
                                   'Законодавства Ячмінії.',
                              reply_markup=keyboard)
    else:
        bot.send_message(chat_id=m.chat.id,
                         text='Простір Ячмінії — всі чати та канали Ячмінії, які дотримуються Законодавства Ячмінії.',
                         reply_markup=keyboard)


def sud_f(m, lab=True):
    keyboard = types.InlineKeyboardMarkup()
    callback_button = types.InlineKeyboardButton(text="Кримінальний суд", callback_data="krime_sud")
    keyboard.add(callback_button)
    callback_button = types.InlineKeyboardButton(text="Апеляційний суд", callback_data="apel_sud")
    keyboard.add(callback_button)
    callback_button = types.InlineKeyboardButton(text=f"⬅️ До головного меню", callback_data=f"menul")
    keyboard.add(callback_button)
    if lab:
        bot.edit_message_text(chat_id=m.chat.id, message_id=m.message_id,
                              text='Оберіть суд, в який ви хочете подати позов',
                              reply_markup=keyboard)
    else:
        bot.send_message(chat_id=m.chat.id,
                         text='Оберіть суд, в який ви хочете подати позов',
                         reply_markup=keyboard)


def all_info_f(m, u, lab=True):
    keyboard = types.InlineKeyboardMarkup()
    url_button = types.InlineKeyboardButton(text=f"📒 Посібник для новоприбулих",
                                            url='https://telegra.ph/YAchm%D1%96nnij-'
                                                'Pos%D1%96bnik-dlya-novopribulih-01-28')
    keyboard.add(url_button)
    url_button = types.InlineKeyboardButton(text=f"📋 Список команд Системи",
                                            url='https://telegra.ph/Spisok-komand-Sistemi-YAchm%D1%96n%D1%96ya-02-01')
    keyboard.add(url_button)
    passport = get_passport(u.id)
    if passport:
        callback_button = types.InlineKeyboardButton(text=f"📖 Паспорт", callback_data=f"pass_pp")
        keyboard.add(callback_button)
        callback_button = types.InlineKeyboardButton(text=f"💰 Рахунок", callback_data=f"acc_pp")
        keyboard.add(callback_button)
    callback_button = types.InlineKeyboardButton(text=f"📈 Активність", callback_data=f"aktyv_pp")
    keyboard.add(callback_button)
    callback_button = types.InlineKeyboardButton(text=f"⬅️ До головного меню", callback_data=f"menul")
    keyboard.add(callback_button)
    if lab:
        bot.edit_message_text(text='Інформація про Вас у Системі', message_id=m.message_id,
                              chat_id=m.chat.id, reply_markup=keyboard)
    else:
        bot.send_message(text='Інформація про Вас у Системі',
                         chat_id=m.chat.id, reply_markup=keyboard)


def menus_f(m, lab=True):
    keyboard = types.InlineKeyboardMarkup()
    callback_button = types.InlineKeyboardButton(text="💰Меню підприємця", callback_data="business")
    keyboard.add(callback_button)
    callback_button = types.InlineKeyboardButton(text="👥Меню роду", callback_data="rid")
    keyboard.add(callback_button)
    callback_button = types.InlineKeyboardButton(text="Меню держслужбовця", callback_data="state_menu")
    keyboard.add(callback_button)
    callback_button = types.InlineKeyboardButton(text="Меню простору Ячмінії", callback_data="prostir_menu")
    keyboard.add(callback_button)
    callback_button = types.InlineKeyboardButton(text=f"⬅️ До головного меню", callback_data=f"menul")
    keyboard.add(callback_button)
    if lab:
        bot.edit_message_text('Тут зібрані спеціалізовані меню Системи', chat_id=m.chat.id,
                              message_id=m.message_id, reply_markup=keyboard)
    else:
        bot.send_message(text='Тут зібрані спеціалізовані меню Системи', chat_id=m.chat.id, reply_markup=keyboard)


def rid_f(u, m, lab=True):
    passport = get_passport(u.id)
    if passport is None:
        keyboard = types.InlineKeyboardMarkup()
        keyboard = menu_footer(keyboard, 'menus')
        if lab:
            bot.edit_message_text(chat_id=m.chat.id, message_id=m.message_id, text=f'У вас нема громадянства Ячмінії',
                                  reply_markup=keyboard)
        else:
            bot.send_message(chat_id=m.chat.id, text=f'У вас нема громадянства Ячмінії', reply_markup=keyboard)
        return

    if passport[13] != 'Самітник':
        rid = get_rid(passport[13])
        if int(rid[2]) == u.id:
            head = True
        else:
            head = False
        keyboard = types.InlineKeyboardMarkup()
        if head:
            word = 'головою'
            callback_button = types.InlineKeyboardButton(text=f"🆕Прийняти нового члена роду",
                                                         callback_data=f"new_rid_member")
            keyboard.add(callback_button)
            callback_button = types.InlineKeyboardButton(text=f"👥Члени роду",
                                                         callback_data=f"rid_members")
            keyboard.add(callback_button)
            callback_button = types.InlineKeyboardButton(text=f"✍️Перейменувати рід",
                                                         callback_data=f"edit_rid")
            keyboard.add(callback_button)
        else:
            word = 'членом'
            callback_button = types.InlineKeyboardButton(text=f"🆕Вийти з роду",
                                                         callback_data=f"exit_rid")
            keyboard.add(callback_button)
        keyboard = menu_footer(keyboard, 'menus')
        if lab:
            bot.edit_message_text(chat_id=m.chat.id, message_id=m.message_id,
                                  text=f'Ви є {word} роду {rid[1]}',
                                  reply_markup=keyboard)
        else:
            bot.send_message(chat_id=m.chat.id,
                             text=f'Ви є {word} роду {rid[1]}',
                             reply_markup=keyboard)
    else:
        keyboard = types.InlineKeyboardMarkup()
        callback_button = types.InlineKeyboardButton(text=f"🆕Створити рід", callback_data=f"new_rid")
        keyboard.add(callback_button)
        keyboard = menu_footer(keyboard, 'menus')
        if lab:
            bot.edit_message_text(chat_id=m.chat.id, message_id=m.message_id,
                                  text=f'Ви не належите жодному з існуючих родів, проте ви можете створити свій рід',
                                  reply_markup=keyboard)
        else:
            bot.send_message(chat_id=m.chat.id,
                             text=f'Ви не належите жодному з існуючих родів, проте ви можете створити свій рід',
                             reply_markup=keyboard)


def business_f(business, m, lab=True):
    keyboard = types.InlineKeyboardMarkup()
    button = types.InlineKeyboardButton(text='✍️Редагувати інформацію підприємства', callback_data='edit_business')
    keyboard.add(button)
    button = types.InlineKeyboardButton(text='👥Працівники', callback_data='praciv')
    keyboard.add(button)
    button = types.InlineKeyboardButton(text='💵Керування фінансами',
                                        callback_data='finances')
    keyboard.add(button)
    button = types.InlineKeyboardButton(text='❌Закрити підприємство',
                                        callback_data='del_business')
    keyboard.add(button)
    keyboard = menu_footer(keyboard, 'business')
    if lab:
        bot.edit_message_text(text=f'<a href="https://t.me/businesses_yachminiya/{business[7]}">{business[2]}</a>',
                              message_id=m.message_id, chat_id=m.chat.id, reply_markup=keyboard,
                              parse_mode="HTML", disable_web_page_preview=True)
    else:
        bot.send_message(text=f'<a href="https://t.me/businesses_yachminiya/{business[7]}">{business[2]}</a>',
                         chat_id=m.chat.id, reply_markup=keyboard,
                         parse_mode="HTML", disable_web_page_preview=True)


def state_menu_f(u, m, lab=True):
    passport = get_passport(u.id)
    if passport is None:
        keyboard = menu_footer(types.InlineKeyboardMarkup(), 'menus')
        if lab:
            bot.edit_message_text(chat_id=m.chat.id, message_id=m.message_id,
                                  text=f'У вас нема громадянства Ячмінії', reply_markup=keyboard)
        else:
            bot.send_message(chat_id=m.chat.id,
                             text=f'У вас нема громадянства Ячмінії', reply_markup=keyboard)
        return
    keyboard = types.InlineKeyboardMarkup()
    if passport[8] == 'Без сану':
        button = types.InlineKeyboardButton(text='Звернутись до Голови ФТЯ', callback_data='fond_trud')
        keyboard.add(button)
        keyboard = menu_footer(keyboard, 'menus')
        if lab:
            bot.edit_message_text(chat_id=m.chat.id, message_id=m.message_id,
                                  text=f'У вас нема державного сану. Зверніться до Голови Фонду Трудоустрою Ячмінії за '
                                       f'допомогою.',
                                  reply_markup=keyboard)
        else:
            bot.send_message(chat_id=m.chat.id,
                             text=f'У вас нема державного сану. Зверніться до Голови Фонду Трудоустрою Ячмінії за '
                                  f'допомогою.',
                             reply_markup=keyboard)
        return
    sans = passport[8].split(', ')
    for i in sans:
        button = types.InlineKeyboardButton(text=i, callback_data=i)
        keyboard.add(button)
    keyboard = menu_footer(keyboard, 'menus')
    if lab:
        bot.edit_message_text(chat_id=m.chat.id, message_id=m.message_id,
                              text=f'Меню держслужбовця. Тут ви можете виконувати дії, які доступні для вашого сану.',
                              reply_markup=keyboard)
    else:
        bot.send_message(chat_id=m.chat.id,
                         text=f'Меню держслужбовця. Тут ви можете виконувати дії, які доступні для вашого сану.',
                         reply_markup=keyboard)
    return


def prostir_menu_f(u, m, lab=True):
    passport = get_passport(u.id)
    if passport is None:
        keyboard = menu_footer(types.InlineKeyboardMarkup(), 'menus')
        if lab:
            bot.edit_message_text(chat_id=m.chat.id, message_id=m.message_id,
                                  text=f'У вас нема паспорта Ячмінії', reply_markup=keyboard)
        else:
            bot.send_message(chat_id=m.chat.id,
                             text=f'У вас нема паспорта Ячмінії', reply_markup=keyboard)
        return
    keyboard = types.InlineKeyboardMarkup()
    button0 = types.InlineKeyboardButton(text='Особисті чати', callback_data='private_chats_0')
    button1 = types.InlineKeyboardButton(text='Особисті канали', callback_data='private_channels_0')
    button2 = types.InlineKeyboardButton(text='🗺 До простору Ячмінії',
                                         callback_data='prostir')
    button3 = types.InlineKeyboardButton(text='📱 До спеціалізованих меню',
                                         callback_data='menus')
    callback_button = types.InlineKeyboardButton(text=f"⬅️ До головного меню", callback_data=f"menul")
    keyboard.keyboard = [[button0], [button1], [button2, button3], [callback_button]]
    text = f'Меню керування особистими чатами та каналами.'
    if lab:
        bot.edit_message_text(text=text,
                              message_id=m.message_id, chat_id=m.chat.id, reply_markup=keyboard,
                              parse_mode="HTML", disable_web_page_preview=True)
    else:
        bot.send_message(text=text,
                         chat_id=m.chat.id, reply_markup=keyboard,
                         parse_mode="HTML", disable_web_page_preview=True)


def simplify(text):
    return re.sub(r'<(/|).*?>', '', text)


def menu_footer(keyboard, call_data, back='⬅️ Назад'):
    but0 = types.InlineKeyboardButton(text=back, callback_data=call_data)
    but1 = types.InlineKeyboardButton(text=f"⬅️ До меню", callback_data=f"menul")
    """keyboard.add(but0)
    keyboard.add(but1)"""
    keyboard.keyboard.append([but0, but1])
    return keyboard


def register_next_step_handler(m, function, *args, **kwargs):
    args = tuple([function] + list(args))
    bot.register_next_step_handler(m, reg_next, *args, **kwargs)


def reg_next(m, function, is_media=False):
    if not is_media and not m.text:
        keyboard = types.InlineKeyboardMarkup()
        keyboard.add(types.InlineKeyboardButton(text=f"⬅️ До меню", callback_data=f"menul"))
        bot.send_message(m.chat.id, 'Отримано медіа-повідомлення. Дана операція підтримує тільки текстові '
                                    'повідомлення. Спробуйте ще раз.', reply_markup=keyboard)
    else:
        function(m)


def get_str_passport(id):
    passport = get_passport(id)
    if passport is None:
        try:
            user = get_user(id)
            if user is None:
                u = bot.get_chat(id)
                return f'{name(u)} не має громадянства Ячмінії.'
            else:
                return f'{user[4]} не має громадянства Ячмінії.'
        except:
            return f'Вказаний неправильний ідентифікаційний код особи.'
    if passport[10] == 'Громадянин':
        stat = 'Громадянина'
        san = f'<b>Сан:</b> <i>{passport[8]}</i>\n'
    else:
        stat = 'Резидента'
        san = ''
    passport_out = f'<a href="passport.{id}">{chr(8205)}</a><b>Паспорт</b>\n'
    passport_out += f'<i>{stat} Ячмінії</i>\n\n'
    passport_out += f'''<b>Ім'я:</b> <i>{user_link(passport[1], passport[2], passport[3])}</i>\n'''
    passport_out += f"{san}"
    passport_out += f"<b>Стать:</b> <i>{passport[6]}</i>\n"
    passport_out += f"<b>Рід:</b> <i>{passport[13]}</i>\n"
    passport_out += f"\n<i>Дата видачі:</i>"
    passport_out += f"\n<i>{passport[7]}</i>"
    return passport_out


def get_business(id):
    business = get_business_id(id)
    if business is None:
        business = get_business_name(id)
    return business


def get_str_business(id):
    """повертає бізнес у вигляді str"""
    business = get_business(id)
    if business is None:
        return f'Вказано неправильний ідентифікатор підприємства'
    passport = get_passport(business[3])
    business_out = f'<b>Підприємство</b>\n'
    business_out += f'''<a href="https://t.me/businesses_yachminiya/{business[7]}">{business[2]}</a>\n\n'''
    business_out += f'<b>Власник:</b> <i>{user_link(passport[1], passport[2], passport[3])}</i>\n'
    business_out += f"<b>Тег:</b> <code>{business[1]}</code>\n"
    business_out += f'<b>Активи</b>: <i>{business[4]} {glas(business[4])}</i>\n'
    return business_out


def get_str_rid(id):
    """повертає рід у вигляді str"""
    rid = get_rid(id)
    if rid is None:
        return f'Рід з такою назвою не існує.'
    all_id = list(map(lambda x: int(x), rid[3].split()[2:]))
    passport = get_passport(rid[2])
    all_id.append(passport[1])
    businesses = get_business_owner(all_id)
    del (all_id[-1])
    rid_out = f'<b>Рід</b>\n'
    rid_out += f'''<a href="https://t.me/FamilyRegistry/{rid[5]}">{rid[1]}</a>\n\n'''
    rid_out += f'Голова:\n<b><a href="t.me/{passport[5]}">{passport[2]} {passport[3]}</a></b>\n'
    money = 0
    akt = 0
    if len(all_id) > 0:
        rid_out += f'\nЧлени:\n'
    for i in all_id:
        passport = get_passport(i)
        money += passport[9]
        rid_out += f'<a href="t.me/{passport[5]}">{passport[2]} {passport[3]}</a>\n'
    for i in businesses:
        akt += i[4]

    rid_out += f'\nСтатки: {money} {glas(money)}\n'
    rid_out += f'Активи: {akt} {glas(akt)}\n'
    return rid_out


def get_str_institution(name):
    """повертає установу у вигляді str"""
    inst = get_institution(name)
    if inst is None:
        return f'Вказано неправильну назва установи'
    get_employers = get_inst_func(inst[1])[0]
    emps = get_employers()
    passport = get_passport(inst[6])
    business_out = f'<b>Установа</b>\n'
    business_out += f'''<a href="https://t.me/institutions_yachminiya/{inst[8]}">{inst[1]}</a>\n\n'''
    business_out += f'<b>Голова:</b> <i>{user_link(passport[1], passport[2], passport[3])}</i>\n'
    business_out += f'<b>Активи</b>: <i>{inst[3]} {glas(inst[3])}</i>\n\n'
    if emps:
        business_out += 'Працівники:\n'
        for i in emps:
            passport = get_passport(i[1])
            business_out += f'<a href="t.me/{passport[5]}">{passport[2]} {passport[3]}</a>\n'
    return business_out


def get_str_aktives(id):
    passport = get_passport(id)
    if passport is None:
        try:
            user = get_user(id)
            if user is None:
                u = bot.get_chat(id)
                return f'{name(u)} не має громадянства Ячмінії.'
            else:
                return f'{user[4]} не має громадянства Ячмінії.'
        except:
            return f'Вказаний неправильний ідентифікаційний код особи.'
    businesses = get_business_owner((passport[1],))
    summa = 0
    aktives_out = f'<b>Активи</b>\n'
    aktives_out += f'''{user_link(passport[1], passport[2], passport[3])}\n\n'''
    for i in businesses:
        aktives_out += f'<a href="https://t.me/businesses_yachminiya/{i[7]}">{i[2]}</a> — {i[4]} {glas(i[4])}\n'
        summa += i[4]
    aktives_out += f"\nЗагалом: {summa} {glas(summa)}"
    return aktives_out


def update_channel_rid(rid_name):
    if rid_name == 'Самітник':
        return
    rid = get_rid(rid_name)
    rid_out = get_str_rid(rid[1])
    bot.edit_message_text(chat_id=-1001424413839, text=rid_out, message_id=rid[5], parse_mode='HTML',
                          disable_web_page_preview=True)


def update_channel_business(business_name):
    business = get_business(business_name)
    business_out = get_str_business(business[1])
    bot.edit_message_text(chat_id=-1001162793975, text=business_out, message_id=business[5], parse_mode='HTML',
                          disable_web_page_preview=True)


def update_channel_institution(inst_name):
    inst = get_institution(inst_name)
    inst_out = get_str_institution(inst[1])
    bot.edit_message_text(chat_id=-1001581103239, text=inst_out, message_id=inst[8], parse_mode='HTML',
                          disable_web_page_preview=True)


def get_seans_business(id, m):
    def except_bus(m):
        keyboard = menu_footer(types.InlineKeyboardMarkup(), 'business', "⬅️ До підприємств")
        bot.edit_message_text(
            'Виникла помилка у сесії вашого підприємства. Щоб відновити роботу зайдіть у меню підприємства і оберіть '
            'це підприємство.',
            message_id=m.message_id, chat_id=m.chat.id, reply_markup=keyboard)

    try:
        id = business_seans[id]
    except:
        except_bus(m)
        return None
    business = get_business(id)
    if business is None:
        except_bus(m)
        return None
    return business


def get_str_acc(id):
    """повертає рахунок"""
    passport = get_passport(id)
    if passport is None:
        try:
            user = get_user(id)
            if user is None:
                u = bot.get_chat(id)
                return f'{name(u)} не має громадянства Ячмінії.'
            else:
                return f'{user[4]} не має громадянства Ячмінії.'
        except:
            return f'Вказаний неправильний ідентифікаційний код особи.'
    id_a = passport[1]
    all_businesses = get_all_businesses()
    akt = 0
    for i in range(len(all_businesses)):
        if all_businesses[i][3] == id_a:
            akt += all_businesses[i][4]

    account = f'Державний Банк\n'
    account += f'<b>Ячмінія</b>\n\n'
    account += f'''Ім'я: {user_link(passport[1], passport[2], passport[3])}\n'''
    account += f'Код: <code>{passport[18]}</code>\n\n'
    account += f'Статки: {int(passport[9])} {glas(passport[9])}\n'
    account += f'Активи: {akt} {glas(akt)}\n'
    account += f'Зарплата: {passport[11]} {glas(passport[11])}'
    return account


def non_reg(u, m):
    keyboard = types.InlineKeyboardMarkup()
    button = types.InlineKeyboardButton(text='🤖 Пройти авторизацію', url='t.me/yachminiya_bot')
    keyboard.add(button)
    bot.send_message(m.chat.id,
                     f'{name(u)} не пройшов авторизацію у Системі.',
                     parse_mode='HTML', reply_markup=keyboard)


def html(s):
    """для нормального відображення хтмл символів"""
    return s.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')


def name(user):
    """Повертає ім'я або ім'я та прізвище. ПРІЗВИЩА САСАААААТЬ"""
    if user.last_name is not None:
        return f'{user.first_name} {user.last_name}'
    return user.first_name


def get_inst_func(inst_name):
    if inst_name == 'Жандармерія':
        return get_all_zhandarmeria, insert_zhan_l, insert_all_zhandarmeria_g, get_zhan, new_zhan, \
               del_table_zhandarmeria, table_zhandarmeria, insert_all_zhandarmeria_l, get_amount_of_zhans, del_zhan_g
    elif inst_name == 'Графство':
        return get_all_graphstvo, insert_erl_l, insert_all_graphstvo_g, get_erl, new_erl, del_table_graphstvo, \
               table_graphstvo, insert_all_graphstvo_l, get_amount_of_erls, del_erl_g
    elif inst_name == 'Державний Банк':
        return get_all_bank, insert_karb_l, insert_all_bank_g, get_karb, new_karb, del_table_bank, table_bank, \
               insert_all_bank_l, get_amount_of_karbs, del_karb_g
    elif inst_name == 'Агітаційний відділ':
        # return get_all_agit()
        pass
    return [lambda: []]


@bot.message_handler(func=lambda m: m.chat.type == 'private', commands=['start', 'menu'])
def com_start(m):
    u = m.from_user
    bot.delete_message(m.chat.id, m.message_id)
    user = get_user(m.from_user.id)
    if user is None:
        keyboard = types.InlineKeyboardMarkup()
        url_button = types.InlineKeyboardButton(text="📃 Оформити громадянство Ячмінії",
                                                url='https://t.me/Graphstvo')
        callback_button = types.InlineKeyboardButton(text=f"⬅️ До головного меню", callback_data=f"menul")
        keyboard.add(url_button)
        keyboard.add(callback_button)
        out = f'Привіт, {html(name(m.from_user))}! Схоже, що ти вперше тут, тому ти ще напевне не дуже розумієш, що ' \
              f'таке Ячмінія. Тому дуже радимо тобі прочитати ' \
              f'<a href="https://telegra.ph/YAchm%D1%96nnij-Pos%D1%96bnik-dlya-novopribulih-01-28">Ячмінний Посібник ' \
              f'для новоприбулих</a>. Далі ми тобі радимо звернутись до Графства та оформити громадянство Ячмінії ' \
              f'(кнопка нижче). Бажаємо цікавого проведення часу!'
        bot.send_message(m.chat.id, out, reply_markup=keyboard, parse_mode='HTML', disable_web_page_preview=True)
        # bot.send_message(-1001381818993, f'{user_link(u.id, html(name(u))}\n{u.id}',
        # parse_mode='HTML')
        new_user(m.from_user)
        chats = get_all_chats()
        for i in chats:
            try:
                bot.unban_chat_member(int(i[1]), m.from_user.id, True)
                bot.promote_chat_member(int(i[1]), m.from_user.id)
            except:
                pass
    else:
        code = extract_unique_code(m.text)
        spl_code = code.split('_')
        if spl_code[0] in ('zvit', 'zvitd'):
            passport = get_passport(m.from_user.id)
            if passport is None:
                keyboard = types.InlineKeyboardMarkup().add(
                    types.InlineKeyboardButton(text='До головного меню', callback_data='menul'))
                bot.send_message(m.chat.id, 'У вас нема громадянства Ячмінії', reply_markup=keyboard)
                return
            m_id = spl_code[2]
            karb = get_karb(m.from_user.id)
            keyboard = types.InlineKeyboardMarkup()
            if spl_code[0] == 'zvit':
                if karb:
                    button = types.InlineKeyboardButton(text='Фінансувати',
                                                        callback_data=f'finance_zvit_{spl_code[1]}_{spl_code[2]}')
                    keyboard.add(button)
            bot.copy_message(m.chat.id, -1001511247539, int(m_id), reply_markup=keyboard)
        elif spl_code[0] in ('finzvit', 'finzvitd'):
            passport = get_passport(m.from_user.id)
            if passport is None:
                keyboard = types.InlineKeyboardMarkup().add(
                    types.InlineKeyboardButton(text='До головного меню', callback_data='menul'))
                bot.send_message(m.chat.id, 'У вас нема громадянства Ячмінії', reply_markup=keyboard)
                return
            m_id = spl_code[2]
            keyboard = types.InlineKeyboardMarkup()
            if spl_code[0] == 'finzvit':
                mess_id = int(spl_code[1])
                msg = bot.forward_message(thrash, -1001543732225, mess_id)
                msg_id = int(msg.reply_markup.keyboard[0][0].url.split('=')[1].split('_')[2])
                zvit_text = msg.text
                inst = get_institution(inst_shorts[" ".join(zvit_text.split('\n')[0].split()[3:-3])])
                if inst[6] == m.from_user.id:
                    button = types.InlineKeyboardButton(text='Розподілити отримані кошти',
                                                        callback_data=f'finzvit_{spl_code[1]}_{spl_code[2]}_{msg_id}')
                    keyboard.add(button)
            bot.copy_message(m.chat.id, -1001511247539, int(m_id), reply_markup=keyboard)
        elif spl_code[0] == 'rozp':
            passport = get_passport(m.from_user.id)
            if passport is None:
                keyboard = types.InlineKeyboardMarkup().add(
                    types.InlineKeyboardButton(text='До головного меню', callback_data='menul'))
                bot.send_message(m.chat.id, 'У вас нема громадянства Ячмінії', reply_markup=keyboard)
                return
            m_id = spl_code[2]
            keyboard = types.InlineKeyboardMarkup()
            bot.copy_message(m.chat.id, -1001511247539, int(m_id), reply_markup=keyboard)
        elif code == 'prostir':
            prostir_f(m, False)
        elif code == 'all_info':
            all_info_f(m, u, False)
        elif code == "golos":
            pass
        elif code == 'menus':
            menus_f(m, False)
        elif code == 'sud':
            sud_f(m, False)
        else:
            main_menu(m, False)


@bot.message_handler(func=lambda m: m.chat.type == 'supergroup', commands=['start', 'menu'])
def com_start(m):
    try:
        bot.delete_message(m.chat.id, m.message_id)
    except:
        pass
    keyboard = types.InlineKeyboardMarkup()
    url_button = types.InlineKeyboardButton(text="💬 Основний чат Ячмінії",
                                            url='https://t.me/Yachminiya')
    keyboard.add(url_button)
    callback_button = types.InlineKeyboardButton(text="🗺 Простір Ячмінії",
                                                 url="t.me/yachminiya_test_bot?start=prostir")
    keyboard.add(callback_button)
    callback_button = types.InlineKeyboardButton(text="🗳 Голосування", url="t.me/yachminiya_test_bot?start=golos")
    keyboard.add(callback_button)
    callback_button = types.InlineKeyboardButton(text="⚖️ Cуд", url="t.me/yachminiya_test_bot?start=sud")
    keyboard.add(callback_button)
    callback_button = types.InlineKeyboardButton(text="📱Спеціалізовані меню",
                                                 url="t.me/yachminiya_test_bot?start=menus")
    keyboard.add(callback_button)
    callback_button = types.InlineKeyboardButton(text="ℹ️ Інформація", url="t.me/yachminiya_test_bot?start=all_info")
    keyboard.add(callback_button)
    bot.send_message(m.chat.id, 'Вас вітає групове меню Системи.\nТут зібрані головні функції Системи.',
                     reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    global voting_q, del_pass

    m = call.message
    u = call.from_user
    if f_queue_call(call):
        return

    if call.data == "pass":
        if call.from_user.id != m.reply_to_message.from_user.id:
            bot.answer_callback_query(callback_query_id=call.id, text='Ця кнопка призначена не для Вас!',
                                      show_alert=True)
            return
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=call.message.text)
        bot.send_message(chat_id=call.message.chat.id, text=pass_form, parse_mode='HTML')
        return

    if call.data == 'menu':
        main_menu(call.message, False)
        return

    if call.data == 'menul':
        main_menu(call.message, True)
        return

    if call.data == 'sud':
        sud_f(m)
        return

    if call.data == 'prostir':
        prostir_f(m)
        return

    if call.data == 'all_info':
        all_info_f(m, u)
        return

    if call.data == 'menus':
        menus_f(m)
        return

    if call.data == 'pass_pp':
        keyboard = types.InlineKeyboardMarkup()
        keyboard = menu_footer(keyboard, 'all_info')

        out = get_str_passport(u.id)
        bot.edit_message_text(out, m.chat.id, m.message_id, parse_mode='HTML', reply_markup=keyboard)
        return

    if call.data == 'acc_pp':
        keyboard = types.InlineKeyboardMarkup()
        keyboard = menu_footer(keyboard, 'all_info')

        out = get_str_acc(u.id)
        bot.edit_message_text(out, m.chat.id, m.message_id, parse_mode='HTML', reply_markup=keyboard)
        return

    if call.data == 'aktyv_pp':
        usr = get_user(u.id)
        all_users = get_all_users()
        all_messages = 0
        all_words = 0
        for i in all_users:
            all_messages += i[7]
            all_words += i[8]

        keyboard = types.InlineKeyboardMarkup()
        keyboard = menu_footer(keyboard, 'all_info')

        out = f'Активність\n{user_link(u.id, html(name(u)))}\n\n'
        out += f'Репутація: {usr[3]}\n'
        out += f'Повідомлень за весь час: {usr[7]}\n'
        out += f'Слів за весь час: {usr[8]}\n'
        out += f"Процент активу: {round(((usr[7] / all_messages) + (usr[8] / all_words)) * 50, 2)}%"
        bot.edit_message_text(out, m.chat.id, m.message_id, parse_mode='HTML', reply_markup=keyboard)
        return

    if call.data == 'chats':
        chats = get_all_chats()
        u = get_user(u.id)
        keyboard = types.InlineKeyboardMarkup()
        for i in chats:
            if str(i[0]) in u[9].split():
                try:
                    if i[4] != 'NoneURL':
                        url_button = types.InlineKeyboardButton(text=i[1], url=i[4])
                        keyboard.add(url_button)
                except:
                    pass
        keyboard = menu_footer(keyboard, 'prostir')
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text='Список чатів Ячмінії, до яких ви маєте доступ.\nЯкщо тут нема якогось чату, у '
                                   'якому ви є, введіть у тому чаті команду <code>!додати_чат</code>',
                              reply_markup=keyboard, parse_mode='HTML')
        return

    if call.data == 'channels':
        channels = get_all_channels()
        u = get_user(u.id)
        keyboard = types.InlineKeyboardMarkup()
        for i in channels:
            if str(i[0]) in u[10].split():
                try:
                    if i[3] != 'NoneURL':
                        url_button = types.InlineKeyboardButton(text=i[1], url=i[3])
                        keyboard.add(url_button)
                except:
                    pass
        keyboard = menu_footer(keyboard, 'prostir')
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text='Список каналів Ячмінії, до яких ви маєте доступ.', reply_markup=keyboard,
                              parse_mode='HTML')
        return

    if call.data[0:9] == 'krime_sud':
        def get_guilty(m0):
            if m0.text == 'СТОП':
                bot.send_message(m0.chat.id, 'Ви відмінили процедуру подання заяви')
                main_menu(m0, False)
                return

            guilty = m0.text.split(', ')
            text = f'{alg}Вкажіть статтю, за якою ви здійснюєте позов. Якщо такий статей декілька, вкажіть їх ' \
                   f'через кому. <a href="https://telegra.ph/Rozd%D1%96l-%D0%86%D0%86-Krim%D1%96naln%D1%96' \
                   f'-pravoporushennya-04-24">Розділ ІІ Карного зводу. Кримінальні правопорушення</a> '

            def get_articles(m1):
                if m1.text == 'СТОП':
                    bot.send_message(m0.chat.id, 'Ви відмінили процедуру подання заяви')
                    main_menu(m0, False)
                    return

                articles = m1.text.split(', ')
                text = f'{alg}Напишіть стислий та змістовний опис  позову. Обмеження по кількості символів — 2000.'

                def get_description(m2):
                    if m2.text == 'СТОП':
                        bot.send_message(m0.chat.id, 'Ви відмінили процедуру подання заяви')
                        main_menu(m0, False)
                        return

                    description = m2.text
                    text = f'{alg}Надішліть усі докази.'
                    messages = []

                    def get_evidence(message):
                        if message.text == 'ЗАВЕРШИТИ':
                            pass
                        else:
                            messages.append(message)
                            if len(messages)>9:
                                pass
                            else:
                                register_next_step_handler(message, get_evidence)

                    bot.send_message(text=text, chat_id=call.message.chat.id, parse_mode='HTML',
                                     disable_web_page_preview=True)
                    register_next_step_handler(m2, get_evidence)

                bot.send_message(text=text, chat_id=call.message.chat.id, parse_mode='HTML',
                                 disable_web_page_preview=True)
                register_next_step_handler(m1, get_description)

            bot.send_message(text=text, chat_id=call.message.chat.id, parse_mode='HTML', disable_web_page_preview=True)
            register_next_step_handler(m0, get_articles)

        link = '"https://telegra.ph/Algoritm-podach%D1%96-pozovu-09-23"'
        alg = f'''Подача заяви відбувається за алгоритмом вказаним у <a href={link}>цій статті</a>.\n\n'''
        text = f"{alg}" \
               f"Вкажіть нік, тег, ідентифікатор або код особи, проти якої подається позов. Якщо таких осіб " \
               f"декілька, вкажіть їх через кому (з пробілами).\n" \
               f"{stop_text}"

        if call.data == 'krime_sud_nm':
            bot.edit_message_reply_markup(m.chat.id, m.message_id, reply_markup=None)
            bot.send_message(text=text, chat_id=call.message.chat.id, parse_mode='HTML', disable_web_page_preview=True)
        else:
            bot.edit_message_text(text, call.message.chat.id, call.message.message_id, parse_mode='HTML',
                                  disable_web_page_preview=True)
        register_next_step_handler(call.message, get_guilty)
        return

    if call.data == 'apel_sud':
        def apel_sud(m):
            if m.text == 'СТОП':
                bot.send_message(m.chat.id, 'Ви відмінили процедуру подання заяви')
                main_menu(m, False)
                return
            bot.send_message(-1001203194174,
                             f'{user_link(m.from_user.id, html(name(m.from_user)))}',
                             parse_mode='HTML')
            bot.forward_message(-1001203194174, m.chat.id, m.message_id)
            bot.send_message(m.chat.id, "Ви успішно подали позов. Очікуйте, із вами скоро зв'яжуться")
            main_menu(m, False)

        text = f'''Для подачі апеляції у Апеляційний Суд опишіть її, бажано надати посилання на рішення Суду. Якщо ви 
        подаєте не апеляцію, детально опишіть ваш позов. {stop_text}'''
        bot.edit_message_text(text, call.message.chat.id, call.message.message_id, parse_mode='HTML',
                              disable_web_page_preview=True)
        register_next_step_handler(call.message, apel_sud)
        return

    if call.data == 'petition':
        passport = get_passport(u.id)
        if passport is None:
            keyboard = types.InlineKeyboardMarkup()
            callback_button = types.InlineKeyboardButton(text=f"⬅️ До головного меню", callback_data=f"menul")
            keyboard.add(callback_button)
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                  text=f'У вас нема громадянства Ячмінії', reply_markup=keyboard)
            return
        if passport[10] != 'Громадянин':
            keyboard = types.InlineKeyboardMarkup()
            callback_button = types.InlineKeyboardButton(text=f"⬅️ До головного меню", callback_data=f"menul")
            keyboard.add(callback_button)
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                  text=f'У вас недостатньо прав для створення петиції', reply_markup=keyboard)
            return

        def petition_1(m):
            if m.text == 'СТОП':
                bot.send_message(m.chat.id, 'Ви відмінили процедуру подання петиції')
                main_menu(m, False)
                return
            if len(m.text) > 100:
                bot.send_message(m.chat.id, 'Занадто довга назва, спробуйте ще раз.')
                register_next_step_handler(m, petition_1)
                return

            def petition_2(m, title):
                if m.text == 'СТОП':
                    bot.send_message(m.chat.id, 'Ви відмінили процедуру подання петиції')
                    main_menu(m, False)
                    return
                if len(m.text) > 2000:
                    bot.send_message(m.chat.id, 'Занадто довгий текст петиції, спробуйте ще раз.')
                    register_next_step_handler(m, petition_2)
                    return
                text = m.text
                num = get_petition_last()
                text_p = f'<b>{html(title)}</b>\n' \
                         f'Автор: {user_link(passport[1], passport[2], passport[3])}\n\n{html(text)}\n\n' \
                         f'<a href="https://t.me/c/1219790275/{int(num) + 1}">Підтримали петицію</a>'
                keyboard = types.InlineKeyboardMarkup()
                button = types.InlineKeyboardButton(text='Підтримати — 1', callback_data='petition_vote')
                keyboard.add(button)
                # bot.send_message(-1001403193441, text_p, reply_markup=keyboard, parse_mode='HTML',
                # disable_web_page_preview=True)
                text_p = f'<a href="https://t.me/c/1403193441/{int(num) + 1}">{html(title)}</a>\n\n' \
                         f'{user_link(passport[1], passport[2], passport[3])} id:{m.from_user.id}'
                # bot.send_message(-1001219790275, text_p, parse_mode='HTML', disable_web_page_preview=True)
                insert_petition_last(num + 1)
                bot.send_message(m.chat.id,
                                 f'Петиція успішно подана.\n'
                                 f'<a href="https://t.me/c/1403193441/{int(num) + 1}">Посилання</a>',  # TODO
                                 parse_mode='HTML')
                main_menu(m, False)

            bot.send_message(m.chat.id,
                             f'Введіть текст петиції. Максимальна довжина тексту — 2000 символів.\n{stop_text}',
                             parse_mode='HTML')
            register_next_step_handler(m, petition_2, m.text)

        text = f'''Напишіть заголовок петиції. Максимальна довжина заголовку — 100 символів.\n{stop_text}'''
        bot.edit_message_text(text, call.message.chat.id, call.message.message_id, parse_mode='HTML',
                              disable_web_page_preview=True)
        register_next_step_handler(call.message, petition_1)
        return

    if call.data == 'petition_vote':
        passport = get_passport(u.id)
        if passport is None:
            bot.answer_callback_query(callback_query_id=call.id, text='У вас нема громадянства Ячмінії',
                                      show_alert=True)
            return
        votes_m = bot.forward_message(thrash, -1001219790275, call.message.message_id)
        text = votes_m.text.split('\n')
        for i in range(2, len(text)):
            if str(call.from_user.id) == text[i].split()[-1][3:]:
                bot.answer_callback_query(callback_query_id=call.id, text='Ви вже підтримали цю петицію',
                                          show_alert=True)
                return
        text_p = f'<a href="{votes_m.entities[0].url}">{text[0]}</a>\n\n'
        for i in range(2, len(text)):
            text_p += f'<a href="tg://user?id={text[i].split()[-1][3:]}">{" ".join(text[i].split()[:-1])}</a> ' \
                      f'{text[i].split()[-1]}\n'
        text_p += f'{user_link(call.from_user.id, passport[2], passport[3])} id:{call.from_user.id}'
        bot.edit_message_text(text=text_p, chat_id=-1001219790275, message_id=call.message.message_id,
                              parse_mode='HTML', disable_web_page_preview=True)
        keyboard = types.InlineKeyboardMarkup()
        button = types.InlineKeyboardButton(text=f'Підтримати — {len(text) - 1}', callback_data='petition_vote')
        keyboard.add(button)
        bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                      reply_markup=keyboard)
        bot.answer_callback_query(callback_query_id=call.id, text='Ви підтримали цю петицію', show_alert=True)
        return

    if call.data == 'menu_changed':
        bot.edit_message_text(f"{call.message.text}", chat_id=call.message.chat.id, message_id=call.message.message_id)
        main_menu(m, False)
        return

    if call.data == 'vidmova':
        user = m.entities[0].user
        if u.id != user.id:
            bot.answer_callback_query(callback_query_id=call.id, text='Ця кнопка призначена не для Вас!',
                                      show_alert=True)
            return
        passport = get_passport(u.id)
        all_passports = get_all_passports()
        del (all_passports[passport[0] - 1])
        for i in range(len(all_passports)):
            all_passports[i][0] = i + 1
        del_table_passports()
        db.insert(table_passports)
        insert_all_passports_l(all_passports)
        amount = get_amount_of_passports()
        bot.edit_message_text(chat_id=m.chat.id, message_id=call.message.message_id,
                              text=f'{name(u)} втрачає громадянство Ячмінії!')
        del_passport_g(all_passports, amount)
        # TODO рід та бізнес

    if call.data == "kvorum":
        starshyna = get_passport(u.id)
        if starshyna is None:
            bot.answer_callback_query(callback_query_id=call.id, text='Ви не Старшина',
                                      show_alert=True)
            return
        if not int(starshyna[12].split()[1]):
            bot.answer_callback_query(callback_query_id=call.id, text='Ви не Старшина',
                                      show_alert=True)
            return

        stars = call.message.text.split('\n')[-1].split(', ')
        mess = '\n'.join(call.message.text.split('\n')[:-1])

        out = f'{mess}\n'

        if call.message.entities is not None:
            for i in call.message.entities:
                if i.user.id == call.from_user.id:
                    bot.answer_callback_query(callback_query_id=call.id, text='Ви вже проголосували',
                                              show_alert=True)
                    return

            for i in range(len(stars)):
                out += f'<a href="tg://user?id={m.entities[i].user.id}">{stars[i]}</a>, '

        out += f'<a href="tg://user?id={call.from_user.id}">{starshyna[2]} {starshyna[3]}</a>'

        keyboard = types.InlineKeyboardMarkup()
        callback_button = types.InlineKeyboardButton(text=f"Присутній - {len(stars) + 1}", callback_data="kvorum")
        keyboard.add(callback_button)
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=out,
                              reply_markup=keyboard, parse_mode='HTML')

    if call.data == 'rid':
        rid_f(u, m)
        return

    if call.data == "rid_members":
        keyboard = types.InlineKeyboardMarkup()
        passport = get_passport(call.from_user.id)
        rid = get_rid(passport[13])

        for i in range(2, len(rid[3].split())):
            employer = get_passport(int(rid[3].split()[i]))
            callback_button = types.InlineKeyboardButton(text=f"{employer[2]} {employer[3]}",
                                                         callback_data=f"rid_member{i}")
            keyboard.add(callback_button)

        keyboard = menu_footer(keyboard, 'rid')
        bot.edit_message_text(text=f'Члени роду {rid[1]}', message_id=call.message.message_id,
                              chat_id=call.message.chat.id, reply_markup=keyboard)
        return

    if call.data == "new_rid":
        def form_bus(m):
            if m.text == 'СТОП':
                bot.send_message(m.chat.id, 'Ви відмінили процедуру створення роду')
                main_menu(m, False)
                return
            mess = m.text.split('\n')
            rid_name = html(m.text)
            rid = get_rid(rid_name)
            if rid:
                bot.send_message(m.chat.id,
                                 f'Такий рід уже існує. Придумайте іншу назву і відправте знову. {stop_text}')
                register_next_step_handler(m, form_bus)
                return

            if rid_name == 'Самітник' or rid_name == 'Самітники':
                bot.send_message(m.chat.id,
                                 f'Не можна використовувати назви "Самітник" та "Самітники". '
                                 f'Спробуйте ще раз. {stop_text}')
                register_next_step_handler(m, form_bus)
                return

            business_out = f'Ваш рід матиме назву <b>{rid_name}</b>. <b>Увага!</b> Реєстрація роду коштує 500 ячок. ' \
                           f'Кошти будуть списані автоматично після реєстрації. Якщо на вашому рахунку недостатньо ' \
                           f'ячок, реєстрація буде відхилена\n\n'
            keyboard = types.InlineKeyboardMarkup()
            button = types.InlineKeyboardButton(text='Зареєструвати рід', callback_data='rid_done')
            keyboard.add(button)
            button = types.InlineKeyboardButton(text='Обрати іншу назву', callback_data='new_rid')
            keyboard.add(button)
            button = types.InlineKeyboardButton(text='Відмінити процедуру створення роду', callback_data='rid')
            keyboard.add(button)
            bot.send_message(m.chat.id, business_out, parse_mode='HTML', reply_markup=keyboard)

        bot.edit_message_text(
            text=f'Придумайте назву свого роду. <b>Увага!</b> Не можна використовувати назви "Самітник" та '
                 f'"Самітники". {stop_text}',
            message_id=call.message.id, chat_id=call.message.chat.id, parse_mode='HTML')
        register_next_step_handler(call.message, form_bus)

    if call.data == 'rid_done':
        bot.edit_message_text(
            text=f'Зачекайте. Створюється рід.',
            message_id=call.message.message_id, chat_id=call.message.chat.id)
        mess = call.message.text.split()
        index_1 = mess.index('назву')
        index_2 = mess.index('Увага!')
        namep = html(' '.join(mess[index_1 + 1:index_2])[:-1])
        passport = get_passport(call.from_user.id)
        keyboard = types.InlineKeyboardMarkup()
        callback_button = types.InlineKeyboardButton(text=f"⬅️ До головного меню", callback_data=f"menul")
        keyboard.add(callback_button)
        if int(passport[9]) < 1:
            bot.edit_message_text(text='На вашому рахунку недостатньо ячок для створення роду',
                                  message_id=call.message.message_id, chat_id=call.message.chat.id,
                                  reply_markup=keyboard)
            return
        passport[9] = int(passport[9]) - 500
        passport[13] = namep

        rid_out = f'<b>Рід</b>\n'
        rid_out += f'''{namep}\n\n'''
        username = passport[5]
        rid_out += f'Голова:\n<b><a href="t.me/{username}">{passport[2]} {passport[3]}</a></b>\n'
        n = bot.send_message(-1001424413839, rid_out, parse_mode='HTML').id
        new_rid(u, m, n)
        update_channel_rid(namep)
        bot.edit_message_text(
            text=f'Ви успішно зареєстрували рід <a href="https://t.me/FamilyRegistry/{n}">{namep}</a>.',
            message_id=call.message.message_id, chat_id=call.message.chat.id, reply_markup=keyboard,
            disable_web_page_preview=True, parse_mode='HTML')
        insert_passport_a(passport)

    if call.data == "new_rid_member":
        bot.edit_message_text(
            f'Введіть id громадянина Ячмінії, якого ви хочете прийняти в рід. '
            f'<a href="https://telegra.ph/YAk-d%D1%96znatis-id-akaunta-v-Telegram%D1%96-03-12">Як дізнатись id '
            f'акаунта в Телеграмі?</a>\n{stop_text}.',
            chat_id=call.message.chat.id, message_id=call.message.message_id, parse_mode='HTML')

        def new_emp_id(m):
            if m.text == 'СТОП':
                bot.send_message(m.chat.id, 'Ви відмінили процедуру прийняття в рід')
                rid_f(u, m, False)
                return

            if m.text == str(m.from_user.id):
                bot.send_message(m.chat.id,
                                 f'Ви не можете прийняти себе у свій же рід)\nСпробуйте ще раз)\n{stop_text}.',
                                 parse_mode='HTML')
                register_next_step_handler(m, new_emp_id)
                return

            if not m.text.isdigit():
                bot.send_message(m.chat.id,
                                 f'Вказаний неправильний ідентифікатор особи. Спробуйте знову.\n{stop_text}.',
                                 parse_mode='HTML')
                register_next_step_handler(m, new_emp_id)
                return

            id = int(m.text)
            new_emp = get_passport(id)
            if new_emp is None:
                bot.send_message(m.chat.id,
                                 f'Вказаний неправильний ідентифікатор або особа не має паспорта Ячмінії. '
                                 f'Спробуйте знову.\n{stop_text}.',
                                 parse_mode='HTML')
                register_next_step_handler(m, new_emp_id)
                return

            if new_emp[13] != 'Самітник':
                bot.send_message(m.chat.id,
                                 f'{user_link(new_emp[1], new_emp[2], new_emp[3])} уже є членом '
                                 f'роду {new_emp[13]}. Спробуйте знову.\n{stop_text}.',
                                 parse_mode='HTML')
                register_next_step_handler(m, new_emp_id)
                return

            passport = get_passport(u.id)
            rid = get_rid(passport[13])
            peoples = rid[3].split()

            if m.text in peoples:
                bot.send_message(m.chat.id,
                                 f'Цей громадянин уже є членом вашого роду. Спробуйте знову.\n{stop_text}.',
                                 parse_mode='HTML')
                register_next_step_handler(m, new_emp_id)
                return
            try:
                keyboard = types.InlineKeyboardMarkup()
                button = types.InlineKeyboardButton(text='Підтвердити', callback_data='new_rid_member_done')
                keyboard.add(button)
                button = types.InlineKeyboardButton(text='Відмінити', callback_data='new_rid_member_cancel')
                keyboard.add(button)
                bot.send_message(int(m.text),
                                 f'Вас хочуть прийняти у рід <a href="t.me/FamilyRegistry/{rid[5]}">{rid[1]}</a>',
                                 parse_mode='HTML', disable_web_page_preview=True, reply_markup=keyboard)
                bot.send_message(m.chat.id,
                                 f'{user_link(new_emp[1], new_emp[2], new_emp[3])} отримав '
                                 f'повідомлення про прийняття у рід. Очікуйте підвердження.',
                                 parse_mode='HTML')
            except:
                bot.send_message(m.chat.id,
                                 'Громадянин не може прийняти повідомлення від Системи. Попросіть у нього, щоб він '
                                 'відновив чат з Системою.')
            rid_f(u, m, False)

        register_next_step_handler(call.message, new_emp_id)
        return

    if call.data == 'edit_rid':
        def form_bus(m):
            if m.text == 'СТОП':
                bot.send_message(m.chat.id, 'Ви відмінили процедуру зміни назви роду.')
                rid_f(u, m, False)
                return
            rid_name = html(m.text)
            rid = get_rid(rid_name)
            if rid:
                bot.send_message(m.chat.id,
                                 f'Такий рід уже існує. Придумайте іншу назву і відправте знову.\n{stop_text}.',
                                 parse_mode='HTML')
                register_next_step_handler(m, form_bus)
                return

            if rid_name == 'Самітник' or rid_name == 'Самітники':
                bot.send_message(m.chat.id,
                                 f'Не можна використовувати назви "Самітник" та "Самітники". '
                                 f'Спробуйте ще раз.\n{stop_text}.',
                                 parse_mode='HTML')
                register_next_step_handler(m, form_bus)
                return

            business_out = f'Ваш рід матиме назву <b>{rid_name}</b>.'
            keyboard = types.InlineKeyboardMarkup()
            button = types.InlineKeyboardButton(text='Змінити назву', callback_data='edit_rid_done')
            keyboard.add(button)
            button = types.InlineKeyboardButton(text='Обрати іншу назву', callback_data='edit_rid')
            keyboard.add(button)
            button = types.InlineKeyboardButton(text='До меню роду', callback_data='rid')
            keyboard.add(button)
            bot.send_message(m.chat.id, business_out, parse_mode='HTML', reply_markup=keyboard)

        bot.edit_message_text(
            text=f'Придумайте нову назву роду. <b>Увага!</b> Не можна використовувати назви "Самітник" та '
                 f'"Самітники".\n{stop_text}.',
            message_id=call.message.id, chat_id=call.message.chat.id, parse_mode='HTML')
        register_next_step_handler(call.message, form_bus)

    if call.data == 'edit_rid_done':
        bot.edit_message_text(
            text=f'Зачекайте. Змінюється назва роду.',
            message_id=call.message.message_id, chat_id=call.message.chat.id)
        mess = call.message.text.split()
        index = mess.index('назву')
        namep = html(mess[index:-1])
        passport = get_passport(call.from_user.id)
        keyboard = types.InlineKeyboardMarkup()
        callback_button = types.InlineKeyboardButton(text=f"⬅️ До головного меню", callback_data=f"menul")
        keyboard.add(callback_button)
        rid = get_rid(passport[13])

        rid[1] = namep
        all_id = rid[3].split()[2:]
        all_passports = get_all_passports()
        for i in all_id:
            passport = get_passport(int(i))
            passport[13] = namep
            insert_passport_l(passport)
            all_passports[passport[0] - 1][13] = namep
        insert_rid_a(rid)
        update_channel_rid(rid[1])
        bot.edit_message_text(
            text=f'Ви успішно змінили назву роду на <a href="https://t.me/FamilyRegistry/{rid[5]}">{namep}</a>.',
            message_id=call.message.message_id, chat_id=call.message.chat.id, reply_markup=keyboard,
            disable_web_page_preview=True, parse_mode='HTML')
        insert_all_passports_g(all_passports)
        return

    if call.data == "new_rid_member_done":
        url = call.message.entities[0].url
        ch_id = -1001424413839
        bus_id = int(url.split('/')[-1])
        msg = bot.forward_message(thrash, ch_id, bus_id)
        rid_name = msg.text.split('\n')[1]
        rid = get_rid(rid_name)
        if f'{call.from_user.id}' in rid[3].split():
            bot.edit_message_text(f'Ви вже є членом роду {rid[1]}!', message_id=call.message.message_id,
                                  chat_id=call.message.chat.id)
            return
        rid[3] += f' {call.from_user.id}'
        bot.edit_message_text(f'Тепер Ви член роду {rid[1]}!', message_id=call.message.message_id,
                              chat_id=call.message.chat.id)
        employer = get_passport(call.from_user.id)
        bot.send_message(int(rid[2]),
                         f'{user_link(employer[1], employer[16], employer[17])} '
                         f'став членом роду {rid[1]}!',
                         parse_mode='HTML')
        employer[13] = rid[1]
        employer[14] = time.time()
        insert_rid_a(rid)
        insert_passport_a(employer)
        update_channel_rid(rid[1])
        return

    if call.data == "new_rid_member_cancel":
        url = call.message.entities[0].url
        ch_id = -1001424413839
        bus_id = int(url.split('/')[-1])
        msg = bot.forward_message(thrash, ch_id, bus_id)
        rid_name = msg.text.split('\n')[1]
        rid = get_rid(rid_name)
        bot.edit_message_text(f'Ви відмовились від запиту.', message_id=call.message.message_id,
                              chat_id=call.message.chat.id)
        employer = get_passport(call.from_user.id)
        bot.send_message(rid[2],
                         f'{user_link(employer[1], employer[16], employer[17])} відмовився від '
                         f'запиту на прийняття у рід',
                         parse_mode='HTML')
        return

    if call.data == 'del_member':
        member_user = call.message.entities[0].user
        member = get_passport(member_user.id)
        passport = get_passport(u.id)
        rid = get_rid(passport[13])
        employers = rid[3].split()
        number = employers.index(str(member_user.id))
        del (employers[number])
        rid[3] = ' '.join(employers)
        try:
            bot.send_message(member_user.id,
                             f'Вас вилучили з роду {rid[1]}.')
        except:
            pass

        bot.edit_message_text(
            chat_id=call.message.chat.id,
            text=f'Ви вилучили <a href="tg://user?id={member_user.id}">{member[2]} {member[3]}</a> з роду {rid[1]}.',
            message_id=call.message.message_id,
            parse_mode='HTML'
        )

        rid_f(u, m, False)
        member[13] = 'Самітник'
        insert_rid_a(rid)
        insert_passport_a(member)
        update_channel_rid(rid[1])
        return

    if call.data[0:10] == "rid_member":
        i = int(call.data[10:])
        passport = get_passport(u.id)
        rid = get_rid(passport[13])
        rid_member = get_passport(rid[3].split()[i])
        if rid_member is None:
            bot.edit_message_text(f'Виникла помилка', chat_id=call.message.chat.id, message_id=call.message.message_id)
            return

        keyboard = types.InlineKeyboardMarkup()
        button = types.InlineKeyboardButton(text="🚷Вилучити члена роду", callback_data='del_member')
        keyboard.add(button)
        keyboard = menu_footer(keyboard, 'rid_members')
        bot.edit_message_text(f'{user_link(rid_member[1], rid_member[16], rid_member[17])}',
                              chat_id=call.message.chat.id, message_id=call.message.message_id, parse_mode='HTML',
                              reply_markup=keyboard)

    if call.data == 'exit_rid':
        member_user = u
        member = get_passport(u.id)
        rid = get_rid(member[13])
        employers = rid[3].split()
        number = employers.index(str(member_user.id))
        del (employers[number])
        rid[3] = ' '.join(employers)

        keyboard = menu_footer(types.InlineKeyboardMarkup(), 'rid')
        bot.edit_message_text(f'Ви вийшли з роду {rid[1]}.', message_id=call.message.message_id,
                              chat_id=call.message.chat.id, reply_markup=keyboard)

        try:
            bot.send_message(
                chat_id=rid[2],
                text=f'<a href="tg://user?id={member_user.id}">{member[2]} {member[3]}</a> вийшов з роду {rid[1]}.',
                parse_mode='HTML'
            )
        except:
            pass
        rid_f(u, m, False)
        member[13] = 'Самітник'
        insert_rid_a(rid)
        insert_passport_a(member)
        update_channel_rid(rid[1])
        return

    if call.data == 'business':
        passport = get_passport(call.from_user.id)
        keyboard = types.InlineKeyboardMarkup()
        if passport is None:
            keyboard = menu_footer(types.InlineKeyboardMarkup(), 'menus')
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                  text=f'У вас відсутній паспорт резидента або громадянина Ячмінії.',
                                  reply_markup=keyboard)
            return

        businesses = get_business_owner([u.id])
        if businesses is None:
            callback_button = types.InlineKeyboardButton(text=f"🆕Зареєструвати підприємство",
                                                         callback_data=f"new_business")
            keyboard.add(callback_button)
            callback_button = types.InlineKeyboardButton(text=f"⬅️ До головного меню", callback_data=f"menul")
            keyboard.add(callback_button)
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                  text='Ви ще не маєте підприємства. Ви можете зареєструвати своє підприємство '
                                       'натиснувши кнопку нижче.',
                                  reply_markup=keyboard)
            return

        for i in businesses:
            callback_button = types.InlineKeyboardButton(text=f"{i[2]}",
                                                         callback_data=f"business{i[0]}")
            keyboard.add(callback_button)

        callback_button = types.InlineKeyboardButton(text=f"🆕Зареєструвати підприємство",
                                                     callback_data=f"new_business")
        keyboard.add(callback_button)
        keyboard = menu_footer(keyboard, 'menus')
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text='Це спеціалізоване меню підприємця. Тут ви можете керувати своїми підприємствами '
                                   'або зареєструвати нове',
                              reply_markup=keyboard)
        return

    if call.data[0:8] == "business":
        i = int(call.data[8:])
        business_seans[u.id] = get_all_businesses()[i - 1][1]
        business = get_seans_business(u.id, m)
        if not business:
            return
        business_f(business, m)
        return

    if call.data == "praciv":
        keyboard = types.InlineKeyboardMarkup()
        business = get_seans_business(u.id, m)
        if business is None:
            return
        for i in business[5].split()[2:]:
            employer = get_passport(int(i))
            if employer is None:
                continue
            callback_button = types.InlineKeyboardButton(text=f"{employer[2]} {employer[3]}",
                                                         callback_data=f"employer{i}")
            keyboard.add(callback_button)

        callback_button = types.InlineKeyboardButton(text=f"🆕Найняти працівника", callback_data=f"new_employer")
        keyboard.add(callback_button)
        keyboard = menu_footer(keyboard, f"business{business[0]}")
        bot.edit_message_text(text=f'Працівники "{business[2]}"', message_id=call.message.message_id,
                              chat_id=call.message.chat.id, reply_markup=keyboard)
        return

    if call.data[0:8] == "employer":
        i = int(call.data[8:])
        business = get_seans_business(u.id, m)
        if business is None:
            return
        employer = get_passport(i)
        if employer is None:
            keyboard = menu_footer(types.InlineKeyboardMarkup(), f"praciv")
            bot.edit_message_text(f'Виникла помилка', chat_id=call.message.chat.id, message_id=call.message.message_id,
                                  reply_markup=keyboard)
            return

        keyboard = types.InlineKeyboardMarkup()
        button = types.InlineKeyboardButton(text="💳Змінити заробітню плату", callback_data='change_bill')
        keyboard.add(button)
        button = types.InlineKeyboardButton(text="🚷Звільнити працівника", callback_data='del_employer')
        keyboard.add(button)
        keyboard = menu_footer(keyboard, f"praciv")
        bot.edit_message_text(f'{user_link(employer[1], employer[16], employer[17])}',
                              chat_id=call.message.chat.id, message_id=call.message.message_id, parse_mode='HTML',
                              reply_markup=keyboard)

    if call.data == 'new_employer':
        bot.edit_message_text(
            f'Введіть id громадянина Ячмінії, якого ви хочете найняти на роботу. '
            f'<a href="https://telegra.ph/YAk-d%D1%96znatis-id-akaunta-v-Telegram%D1%96-03-12">Як дізнатись id '
            f'акаунта в Телеграмі?</a>\n{stop_text}.',
            chat_id=call.message.chat.id, message_id=call.message.message_id, parse_mode='HTML')

        def new_emp_id(m):
            business = get_seans_business(u.id, m)
            if business is None:
                return

            if m.text == 'СТОП':
                bot.send_message(m.chat.id, 'Ви відмінили процедуру наймання на роботу')
                business_f(business, m, False)
                return

            if m.text == str(m.from_user.id):
                bot.send_message(m.chat.id,
                                 f'Ви не можете найняти себе на свою ж роботу)\nСпробуйте ще раз)\n{stop_text}.',
                                 parse_mode='HTML')
                register_next_step_handler(m, new_emp_id)
                return

            new_emp = get_passport(int(m.text))
            if new_emp is None:
                bot.send_message(m.chat.id,
                                 f'Вказаний неправильний ідентифікатор або особа не має паспорта Ячмінії. Спробуйте '
                                 f'знову.\n{stop_text}.',
                                 parse_mode='HTML')
                register_next_step_handler(m, new_emp_id)
                return

            employers = business[5].split()

            if m.text in employers:
                bot.send_message(m.chat.id,
                                 f'Цей громадянин уже працює у вашому підприємстві. Спробуйте знову.\n{stop_text}.',
                                 parse_mode='HTML')
                register_next_step_handler(m, new_emp_id)
                return

            keyboard = types.InlineKeyboardMarkup()
            button = types.InlineKeyboardButton(text='Підтвердити', callback_data='new_employer_done')
            keyboard.add(button)
            button = types.InlineKeyboardButton(text='Відмінити', callback_data='new_employer_cancel')
            keyboard.add(button)
            try:
                bot.send_message(int(m.text),
                                 f'Вас хочуть найняти на підприємство '
                                 f'<a href="t.me/businesses_yachminiya/{business[7]}">{business[2]}</a>',
                                 parse_mode='HTML', disable_web_page_preview=True, reply_markup=keyboard)
                bot.send_message(m.chat.id,
                                 f'{user_link(new_emp[1], new_emp[2], new_emp[3])} отримав '
                                 f'повідомлення про найняття на роботу. Очікуйте підвердження.',
                                 parse_mode='HTML')
            except:

                bot.send_message(m.chat.id,
                                 'Громадянин не може прийняти повідомлення від Системи. Попросіть у нього, щоб він '
                                 'відновив чат з Системою.')
            business_f(business, m, False)

        register_next_step_handler(call.message, new_emp_id)
        return

    if call.data == "new_employer_done":
        url = call.message.entities[0].url
        ch_id = -1001162793975
        bus_id = int(url.split('/')[-1])
        msg = bot.forward_message(thrash, ch_id, bus_id)
        tag = msg.text.split()[msg.text.split().index('Тег:') + 1]
        business = get_business(tag)
        if f'{u.id}' in business[5].split():
            bot.edit_message_text(f'Ви вже є працівником підприємства {business[2]}!',
                                  message_id=call.message.message_id,
                                  chat_id=call.message.chat.id)
            return
        business[5] += f' {call.from_user.id}'
        business[6] += f' 0'
        bot.edit_message_text(f'Тепер Ви працівник підприємства {business[2]}!', message_id=call.message.message_id,
                              chat_id=call.message.chat.id)
        insert_business_a(business)
        employer = get_passport(call.from_user.id)
        employer[15] += f' {tag}'
        insert_passport_a(employer)
        try:
            bot.send_message(int(business[3]),
                             f'{user_link(employer[1], employer[16], employer[17])} став працівником '
                             f'підприємства {business[2]}!',
                             parse_mode='HTML')
        except:
            pass
        return

    if call.data == 'edit_business':
        business = get_seans_business(u.id, m)
        if business is None:
            return

        def form_bus(m):
            business = get_seans_business(u.id, m)
            if business is None:
                return
            if m.text == 'СТОП':
                bot.send_message(m.chat.id, 'Ви відмінили процедуру редагування інформації підприємства')
                business_f(business, m, False)
                return
            mess = m.text.split('\n')
            try:
                namep = ' '.join(mess[-3].split()[1:])
                tag = '_'.join(mess[-2].split()[1:]).upper()
                about = ' '.join(mess[-1].split()[2:])

                low = 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', \
                      't', 'u', 'v', 'w', 'x', 'y', 'z'
                for i in tag:
                    if i.lower() not in low:
                        if not i.isnumeric() and i != '_':
                            bot.send_message(m.chat.id,
                                             f'Неправильний тег. Придумайте інший тег і '
                                             f'відправте форму знову.\n{stop_text}.',
                                             parse_mode='HTML')
                            register_next_step_handler(m, form_bus)
                            return

                business = get_business(namep)

                if business:
                    bot.send_message(m.chat.id,
                                     f'Підприємство з такою назвою або тегом уже існує. Придумайте іншу назву і '
                                     f'відправте форму знову.\n{stop_text}.',
                                     parse_mode='HTML')
                    register_next_step_handler(m, form_bus)
                    return

                business = get_business(tag)

                if business:
                    bot.send_message(m.chat.id,
                                     f'Підприємство з такою назвою або тегом уже існує. Придумайте іншу назву і '
                                     f'відправте форму знову.\n{stop_text}.',
                                     parse_mode='HTML')
                    register_next_step_handler(m, form_bus)
                    return

                passport = get_passport(m.from_user.id)

                business_out = f'Шаблон підприємства\n\n'
                business_out += f'''<b>Назва:</b> <i>{namep}</i>\n'''
                business_out += f'''<b>Власник:</b> 
                <i>{user_link(passport[1], passport[2], passport[3])}</i>\n'''
                business_out += f"<b>Тег:</b> <i>{tag}</i>\n"
                business_out += f"<b>Рід діяльності:</b> <i>{about}</i>\n"
                keyboard = types.InlineKeyboardMarkup()
                button = types.InlineKeyboardButton(text='Підтвердити шаблон', callback_data='business_edit_done')
                keyboard.add(button)
                button = types.InlineKeyboardButton(text='Заповнити форму заново', callback_data='edit_business')
                keyboard.add(button)
                bot.send_message(m.chat.id, business_out, parse_mode='HTML', reply_markup=keyboard)
            except:
                bot.send_message(m.chat.id,
                                 '''Ви неправильно ввели форму. Перевірте будь ласка:\n1. Чи ви скопіювали саме форму, 
                                 а не все повідомлення?\n2. Чи стоять пропуски після пунктів форми?''')
                register_next_step_handler(call.message, form_bus)
                return

        bot.edit_message_text(text=business_form, message_id=call.message.id, chat_id=call.message.chat.id,
                              parse_mode='HTML')
        register_next_step_handler(call.message, form_bus)

    if call.data == "new_employer_cancel":
        url = call.message.entities[0].url
        ch_id = -1001162793975
        bus_id = int(url.split('/')[-1])
        msg = bot.forward_message(thrash, ch_id, bus_id)
        tag = msg.text.split()[msg.text.split().index('Тег:') + 1]
        business = get_business(tag)
        bot.edit_message_text(f'Ви відмовились від запиту', message_id=call.message.message_id,
                              chat_id=call.message.chat.id)
        employer = get_passport(call.from_user.id)
        try:
            bot.send_message(int(business[3]),
                             f'{user_link(employer[1], employer[16], employer[17])} відмовився від '
                             f'запиту на найняття на роботу',
                             parse_mode='HTML')
        except:
            pass
        return

    if call.data == 'business_edit_done':
        mess = m.text.split('\n')
        namep = ' '.join(mess[-4].split()[1:])
        tag = '_'.join(mess[-2].split()[1:]).upper()
        about = ' '.join(mess[-1].split()[2:])

        business = get_seans_business(u.id, m)
        if business is None:
            return

        passport = get_passport(call.from_user.id)
        keyboard = menu_footer(types.InlineKeyboardMarkup(), f"business{business[0]}", "⬅️ До підприємства")
        edit_business = [business[0], tag, namep, u.id, business[4], business[5], business[6], business[7], business[8],
                         about]
        bot.edit_message_text(
            text=f'Ви успішно відредагували <a href="https://t.me/businesses_yachminiya/{business[7]}">{namep}</a>.',
            message_id=call.message.message_id, chat_id=call.message.chat.id, reply_markup=keyboard,
            disable_web_page_preview=True, parse_mode='HTML')
        insert_business_a(edit_business)
        update_channel_business(namep)
        if business[1] != tag:
            all_id = business[5].split()[2:]
            all_passports = get_all_passports()
            for i in all_id:
                passport = get_passport(int(i))
                passport[15].replace(f'{business[1]}', namep)
                insert_passport_l(passport)
                all_passports[passport[0] - 1][15].replace(f'{business[1]}', namep)
            insert_all_passports_g(all_passports)
        return

    if call.data == 'new_business':
        def form_bus(m):
            if m.text == 'СТОП':
                bot.send_message(m.chat.id, 'Ви відмінили процедуру створення підприємства')
                main_menu(m, False)
                return
            mess = m.text.split('\n')
            try:
                namep = ' '.join(mess[-3].split()[1:])
                tag = '_'.join(mess[-2].split()[1:]).upper()
                about = ' '.join(mess[-1].split()[2:])
            except:
                bot.send_message(m.chat.id,
                                 '''Ви неправильно ввели форму. Перевірте будь ласка:\n1. Чи ви скопіювали саме форму, 
                                 а не все повідомлення?\n2. Чи стоять пропуски після пунктів форми?''')
                register_next_step_handler(call.message, form_bus)
                return

            low = 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', \
                  'u', 'v', 'w', 'x', 'y', 'z'
            for i in tag:
                if i.lower() not in low:
                    if not i.isnumeric() and i != '_':
                        bot.send_message(m.chat.id,
                                         f'Неправильний тег. Придумайте інший тег і відправте форму знову.\n{stop_text}.',
                                         parse_mode='HTML')
                        register_next_step_handler(m, form_bus)
                        return

            if tag == '':
                bot.send_message(m.chat.id,
                                 f'Неправильний тег. Придумайте інший тег і відправте форму знову.\n{stop_text}.',
                                 parse_mode='HTML')
                register_next_step_handler(m, form_bus)
                return

            if namep == '':
                bot.send_message(m.chat.id,
                                 f'Неправильна назва. Придумайте іншу назву і відправте форму знову.\n{stop_text}.',
                                 parse_mode='HTML')
                register_next_step_handler(m, form_bus)
                return

            if about == '.' or about == ' .':
                bot.send_message(m.chat.id,
                                 f'Замість крапки в рід діяльності треба щось вписати. '
                                 f'Заповніть форму заново\n{stop_text}.',
                                 parse_mode='HTML')
                register_next_step_handler(m, form_bus)
                return

            business = get_business(namep)

            if business:
                bot.send_message(m.chat.id,
                                 f'Підприємство з такою назвою або тегом уже існує. Придумайте іншу назву і '
                                 f'відправте форму знову.\n{stop_text}.')
                register_next_step_handler(m, form_bus)
                return

            business = get_business(tag)

            if business:
                bot.send_message(m.chat.id,
                                 f'Підприємство з такою назвою або тегом уже існує. Придумайте іншу назву і '
                                 f'відправте форму знову.\n{stop_text}.')
                register_next_step_handler(m, form_bus)
                return

            passport = get_passport(m.from_user.id)

            business_out = f'Шаблон вашого майбутнього підприємства. Уважно перевірте, чи правильно ви заповнили ' \
                           f'форму. <b>Увага!</b> Реєстрація бізнесу коштує 500 ячок. Кошти будуть списані ' \
                           f'автоматично після реєстрації. Якщо на вашому рахунку недостатньо ячок, реєстрація ' \
                           f'буде відхилена\n\n'
            business_out += f'''<b>Назва:</b> <i>{namep}</i>\n'''
            business_out += f'''<b>Власник:</b> <i>
            {user_link(passport[1], passport[2], passport[3])}</i>\n'''
            business_out += f"<b>Тег:</b> <i>{tag}</i>\n"
            business_out += f"<b>Рід діяльності:</b> <i>{about}</i>\n"
            keyboard = types.InlineKeyboardMarkup()
            button = types.InlineKeyboardButton(text='Зареєструвати підприємство', callback_data='business_done')
            keyboard.add(button)
            button = types.InlineKeyboardButton(text='Заповнити форму заново', callback_data='new_business')
            keyboard.add(button)
            button = types.InlineKeyboardButton(text='Відмінити процедуру створення підприємства',
                                                callback_data='business')
            keyboard.add(button)
            bot.send_message(m.chat.id, business_out, parse_mode='HTML', reply_markup=keyboard)

        bot.edit_message_text(text=business_form, message_id=call.message.id, chat_id=call.message.chat.id,
                              parse_mode='HTML')
        register_next_step_handler(call.message, form_bus)

    if call.data == 'business_done':
        mess = call.message.text.split('\n')
        namep = ' '.join(mess[-4].split()[1:])
        tag = '_'.join(mess[-2].split()[1:]).upper()
        about = ' '.join(mess[-1].split()[2:])
        passport = get_passport(u.id)
        keyboard = types.InlineKeyboardMarkup()
        callback_button = types.InlineKeyboardButton(text=f"⬅️ До головного меню", callback_data=f"menul")
        keyboard.add(callback_button)
        if passport[9] < 500:
            bot.edit_message_text(text='На вашому рахунку недостатньо ячок для реєстрації підприємства',
                                  message_id=call.message.message_id, chat_id=call.message.chat.id,
                                  reply_markup=keyboard)
            return
        passport[9] = passport[9] - 500
        business_out = f'<b>Підприємство</b>\n\n'
        business_out += f'''<b>Назва:</b> <i>{namep}</i>\n'''
        business_out += f'<b>Власник:</b> <i>{user_link(passport[1], passport[2], passport[3])}</i>\n'
        business_out += f"<b>Тег:</b> <code>{tag}</code>\n"
        business_out += f'<b>Активи</b>: <i>0 ячок</i>'
        n = bot.send_message(-1001162793975, business_out, parse_mode='HTML').id
        bot.edit_message_text(
            text=f'Ви успішно зареєстрували <a href="https://t.me/businesses_yachminiya/{n}">{namep}</a>.',
            message_id=call.message.message_id, chat_id=call.message.chat.id, reply_markup=keyboard,
            disable_web_page_preview=True, parse_mode='HTML')
        new_business(u, namep, n, tag, about)
        insert_passport_a(passport)
        business_out = get_str_business(namep)
        bot.edit_message_text(text=business_out, chat_id=-1001162793975, message_id=n, parse_mode='HTML',
                              disable_web_page_preview=True)

    if call.data == "change_bill":
        employer_user = m.entities[0].user
        employer = get_passport(employer_user.id)

        business = get_seans_business(u.id, m)
        if business is None:
            return

        number = business[5].split().index(str(employer_user.id))
        old_bill = business[6].split()[number]

        bot.edit_message_text(
            f'Ви хочете змінити зарплату працівника <a href="tg://user?id={employer_user.id}">{employer[2]} '
            f'{employer[3]}</a>\nЙого теперішня зарплата: {old_bill} {glas(old_bill)}\nВведіть ціле додатнє число ячок '
            f'для нової зарплати. {stop_text}',
            message_id=call.message.message_id, chat_id=call.message.chat.id, parse_mode='HTML')

        def new_bill_f(m):
            if m.text == 'СТОП':
                keyboard = types.InlineKeyboardMarkup()
                callback_button = types.InlineKeyboardButton(text=f"⬅️ До працівників", callback_data=f"praciv")
                keyboard.add(callback_button)
                callback_button = types.InlineKeyboardButton(text=f"⬅️ До головного меню", callback_data=f"menul")
                keyboard.add(callback_button)
                bot.send_message(m.chat.id, 'Ви відмінили зміну заробітньої плати', reply_markup=keyboard)
                return

            try:
                new_bill = int(m.text)
            except:
                bot.send_message(m.chat.id,
                                 f'Неправильний формат числа. Спробуйте ще раз. {stop_text}',
                                 parse_mode='HTML')
                register_next_step_handler(m, new_bill_f)
                return

            if new_bill < 0:
                bot.send_message(m.chat.id,
                                 f"Зарплата не може бути від'ємною. Спробуйте ще раз. {stop_text}",
                                 parse_mode='HTML')
                register_next_step_handler(m, new_bill_f)
                return

            bills = business[6].split()
            bills[number] = str(new_bill)
            business[6] = ' '.join(bills)

            bot.send_message(m.chat.id,
                             f'Ви змінили зарплату працівника <a href="tg://user?id={employer_user.id}">{employer[2]} '
                             f'{employer[3]}</a> на {new_bill} {glas(new_bill)}',
                             parse_mode='HTML')
            business_f(business, m, False)
            insert_business_a(business)
            try:
                bot.send_message(employer_user.id,
                                 f'Вам змінили зарплату в підприємстві {business[2]}\nВаша нова зарплата {new_bill} '
                                 f'{glas(new_bill)}')
            except:
                pass

        register_next_step_handler(call.message, new_bill_f)
        return

    if call.data == 'del_employer':
        employer_user = call.message.entities[0].user
        employer = get_passport(employer_user.id)

        business = get_seans_business(u.id, m)
        if business is None:
            return

        number = business[5].split().index(str(employer_user.id))
        keyboard = types.InlineKeyboardMarkup()
        callback_button = types.InlineKeyboardButton(text=f"Звільнити", callback_data=f"del_employer_done")
        keyboard.add(callback_button)
        callback_button = types.InlineKeyboardButton(text=f"⬅️ Назад", callback_data=f"employer{number}")
        keyboard.add(callback_button)
        bot.edit_message_text(
            f'Ви дійсно хочете звільнити <a href="tg://user?id={employer_user.id}">{employer[2]} {employer[3]}</a>?',
            message_id=call.message.message_id, chat_id=call.message.chat.id, reply_markup=keyboard, parse_mode='HTML')
        return

    if call.data == 'del_employer_done':
        employer_user = call.message.entities[0].user
        employer = get_passport(employer_user.id)

        business = get_seans_business(u.id, m)
        if business is None:
            return

        number = business[5].split().index(str(employer_user.id))
        employers = business[5].split()
        bills = business[6].split()
        del (employers[number])
        del (bills[number])
        business[5] = ' '.join(bills)
        business[6] = ' '.join(bills)

        bot.edit_message_text(
            chat_id=call.message.chat.id,
            text=f'Ви звільнили працівника <a href="tg://user?id={employer_user.id}">{employer[2]} {employer[3]}</a>.',
            message_id=call.message.message_id,
            parse_mode='HTML'
        )
        business_f(business, m, False)
        insert_business_a(business)
        try:
            bot.send_message(employer_user.id,
                             f'Вас звільнили з підприємства {business[2][0]}')
        except:
            pass

    if call.data == "finances":
        business = get_seans_business(u.id, m)
        if business is None:
            return

        keyboard = types.InlineKeyboardMarkup()
        button = types.InlineKeyboardButton('💸Перевести кошти', callback_data='transfer')
        keyboard.add(button)
        button = types.InlineKeyboardButton('💳Зняти кошти', callback_data='withdraw')
        keyboard.add(button)
        button = types.InlineKeyboardButton('💵Нарахувати кошти зі свого рахунку', callback_data='count')
        keyboard.add(button)
        button = types.InlineKeyboardButton('🏦Виплатити зарплату працівникам', callback_data='salary')
        keyboard.add(button)
        callback_button = types.InlineKeyboardButton(text=f"⬅️ Назад", callback_data=f"business{business[0]}")
        keyboard.add(callback_button)
        callback_button = types.InlineKeyboardButton(text=f"⬅️ До головного меню", callback_data=f"menul")
        keyboard.add(callback_button)
        bot.edit_message_text(f'Керування фінансами\n{business[2]}\nАктиви: {business[4]} {glas(business[4])}',
                              message_id=call.message.message_id, chat_id=call.message.chat.id, reply_markup=keyboard)

    if call.data == 'transfer':
        business = get_seans_business(u.id, m)
        if business is None:
            return
        msg = f"{business[2]}\nДля переказу коштів напишіть повідомлення у наступному форматі:\n" \
              f"<code>[id отримувача] [сума переказу] [призначення платежу (необов'язково)]</code>\n{stop_text}\n" \
              f"Активи: {business[4]} {glas(business[4])}"
        bot.edit_message_text(message_id=call.message.message_id, chat_id=call.message.chat.id, text=msg,
                              parse_mode='HTML')

        def transfer(m):
            nonlocal business
            if m.text == 'СТОП':
                bot.send_message(m.chat.id, 'Ви відмінили процедуру переказу коштів.')
                business_f(business, m, False)
                return
            mess = m.text.split()
            if len(mess) < 2:
                bot.send_message(m.chat.id,
                                 f'Неправильний формат вхідних даних. Спробуйте знову.\n{stop_text}.',
                                 parse_mode='HTML')
                register_next_step_handler(m, transfer)
                return
            try:
                amount_m = int(mess[1])
            except:
                bot.send_message(m.chat.id,
                                 f'Введено хибну кількість ячок.\n{stop_text}.',
                                 parse_mode='HTML')
                register_next_step_handler(m, transfer)
                return

            if amount_m < 1:
                bot.send_message(m.chat.id,
                                 f'Вкажіть додатню кількість ячок для переказу. Спробуйте знову.\n{stop_text}.',
                                 parse_mode='HTML')
                register_next_step_handler(m, transfer)
                return
            acc_t = get_passport(mess[0])
            bus = False
            if acc_t is None:
                acc_t = get_business(mess[0])
                bus = True
                if acc_t is None:
                    bot.send_message(m.chat.id,
                                     f'Введено хибний ідентифікатор отримувача. Спробуйте знову.\n{stop_text}',
                                     parse_mode='HTML')
                    register_next_step_handler(m, transfer)
                    return

            if len(mess) > 2:
                description = ' '.join(m.text.split()[2:])
            else:
                description = None

            if int(business[4]) < amount_m:
                bot.send_message(m.chat.id,
                                 f'На рахунку підприємства {business[2]} недостатньо коштів для переказу. '
                                 f'Спробуйте меншу суму.\n{stop_text}.',
                                 parse_mode='HTML')
                register_next_step_handler(m, transfer)
                return

            comm = commission(int(amount_m), 1)

            if business[4] < amount_m + comm:
                bot.send_message(m.chat.id,
                                 f'На рахунку підприємства {business[2]} недостатньо коштів для списання комісії. '
                                 f'Спробуйте меншу суму коштів.\n{stop_text}.',
                                 parse_mode='HTML')
                register_next_step_handler(m, transfer)
                return

            business[4] = business[4] - amount_m - comm
            namep1 = f'<a href="https://t.me/businesses_yachminiya/{business[7]}">{business[2]}</a>'
            if bus:
                acc_t[4] = acc_t[4] + amount_m
                namep2 = f'<a href="https://t.me/businesses_yachminiya/{acc_t[7]}">{acc_t[2]}</a>'
                money_t = acc_t[4]
            else:
                acc_t[9] = acc_t[9] + amount_m
                namep2 = f'{user_link(acc_t[1], acc_t[2], acc_t[3])}'
                money_t = acc_t[9]

            msg = f'Державний Банк\n'
            msg += f'<b>Ячмінія</b>\n\n'
            msg += f'Переказ коштів\n'
            msg += f'Відправник: {namep1} ({business[4]})\n'
            msg += f'Отримувач: {namep2} ({money_t})\n'
            msg += f'Сума переказу: {amount_m} {glas(amount_m)}\n'
            msg += f'Комісія: {comm} {glas(comm)}\n'
            if description is not None:
                msg += f'Призначення переказу: {description}'

            bot.send_message(m.chat.id, msg, parse_mode='HTML', disable_web_page_preview=True)
            # bot.send_message(-1001282951480, f'Переказ коштів\nСума переказу: {amount_m} {glas(amount_m)}')

            if bus:
                # bot.edit_message_text(get_str_business(acc_t[1]), -1001162793975, acc_t[7], parse_mode='HTML')

                msg = f'Державний Банк\n'
                msg += f'<b>Ячмінія</b>\n\n'
                msg += f'На рахунок вашого підприємства переказали кошти\n'
                msg += f'Відправник: {namep1} ({business[9]})\n'
                msg += f'Отримувач: {namep2} ({money_t})\n'
                msg += f'Сума переказу: {amount_m} {glas(amount_m)}\n'
                if description is not None:
                    msg += f'Призначення переказу: {description}'
                try:
                    bot.send_message(acc_t[3], msg, parse_mode='HTML', disable_web_page_preview=True)
                except:
                    pass
            else:
                msg = f'Державний Банк\n'
                msg += f'<b>Ячмінія</b>\n\n'
                msg = f'На ваш рахунок переказали кошти\n'
                msg += f'Відправник: {namep1} ({business[9]})\n'
                msg += f'Сума переказу: {amount_m} {glas(amount_m)}\n'
                if description is not None:
                    msg += f'Призначення переказу: {description}'
                try:
                    bot.send_message(acc_t[1], msg, parse_mode='HTML', disable_web_page_preview=True)
                except:
                    pass

            business_f(business, m, False)
            insert_business_a(business)
            acc_g = get_passport(business[3])
            if bus:
                insert_business_a(acc_t)
                acc_t = get_passport(acc_t[3])
            else:
                insert_passport_a(acc_t)
            update_channel_business(business[1])
            update_channel_rid(acc_g[13])
            update_channel_rid(acc_t[13])

        register_next_step_handler(m, transfer)
        return

    if call.data == 'withdraw':
        business = get_seans_business(u.id, m)
        if business is None:
            return
        acc_t = get_passport(u.id)

        def withdraw(m):
            nonlocal business, acc_t
            if m.text == 'СТОП':
                bot.send_message(m.chat.id, 'Ви відмінили процедуру зняття коштів.')
                business_f(business, m, False)
                return

            try:
                amount_m = int(m.text)
            except:
                bot.send_message(m.chat.id,
                                 f'Неправильний формат вхідних даних. Спробуйте знову.\n{stop_text}.',
                                 parse_mode='HTML')
                register_next_step_handler(m, withdraw)
                return

            if business[4] < amount_m:
                bot.send_message(m.chat.id,
                                 f'На рахунку вашого підприємства недостатньо грошей для зняття. Спробуйте знову.'
                                 f'\n{stop_text}.',
                                 parse_mode='HTML')
                register_next_step_handler(m, withdraw)
                return

            if amount_m < 1:
                bot.send_message(m.chat.id,
                                 f'Вкажіть додатню кількість грошей для зняття. Спробуйте знову.\n{stop_text}.',
                                 parse_mode='HTML')
                register_next_step_handler(m, withdraw)
                return

            business[4] = business[4] - amount_m
            acc_t[9] = acc_t[9] + amount_m

            namep = f'{user_link(acc_t[1], acc_t[2], acc_t[3])}'
            money_t = acc_t[9]

            msg = f'Державний Банк\n'
            msg += f'<b>Ячмінія</b>\n\n'
            msg += f'Переказ коштів\n'
            msg += f'Відправник: <a href="https://t.me/businesses_yachminiya/{business[7]}">{business[2]}</a> ' \
                   f'({business[4]})\n'
            msg += f'Отримувач: {namep} ({money_t})\n'
            msg += f'Сума переказу: {amount_m} {glas(amount_m)}\n'
            bot.send_message(m.chat.id, msg, parse_mode='HTML', disable_web_page_preview=True)
            bot.send_message(-1001282951480, f'Переказ коштів\nСума переказу: {amount_m} {glas(amount_m)}')

            business_f(business, m, False)
            insert_business_a(business)
            insert_passport_a(acc_t)
            update_channel_business(business[1])
            update_channel_rid(acc_t[13])

        bot.edit_message_text(
            text=f'{business[2]}\nВведіть суму коштів, яку ви хочете зняти з рахунку підприємства\n{stop_text}\n'
                 f'Активи: {business[4]} {glas(business[4])}\nСтатки: {acc_t[11]} {glas(acc_t[11])}',
            message_id=call.message.message_id, chat_id=call.message.chat.id, parse_mode='HTML')
        register_next_step_handler(call.message, withdraw)
        return

    if call.data == 'count':
        business = get_seans_business(u.id, m)
        if business is None:
            return
        acc_g = get_passport(u.id)

        def count(m):
            nonlocal business, acc_g
            if m.text == 'СТОП':
                bot.send_message(m.chat.id, 'Ви відмінили процедуру нарахування коштів.')
                business_f(business, m, False)
                return

            try:
                amount_m = int(m.text)
            except:
                bot.send_message(m.chat.id,
                                 f'Неправильний формат вхідних даних. Спробуйте знову.\n{stop_text}.',
                                 parse_mode='HTML')
                register_next_step_handler(m, count)
                return

            if acc_g[9] < amount_m:
                bot.send_message(m.chat.id,
                                 f'На вашому рахунку недостатньо грошей для нарахування. Спробуйте знову.'
                                 f'\n{stop_text}.',
                                 parse_mode='HTML')
                register_next_step_handler(m, count)
                return

            if amount_m < 1:
                bot.send_message(m.chat.id,
                                 f'Вкажіть додатню кількість грошей для нараховувати. Спробуйте знову.\n{stop_text}.',
                                 parse_mode='HTML')
                register_next_step_handler(m, count)
                return

            business[4] = business[4] + amount_m
            acc_g[9] = acc_g[9] - amount_m

            namep = f'{user_link(acc_g[1], acc_g[2], acc_g[3])}'
            money_t = acc_g[9]

            msg = f'Державний Банк\n'
            msg += f'<b>Ячмінія</b>\n\n'
            msg += f'Переказ коштів\n'
            msg += f'Відправник: {namep} ({money_t})\n'
            msg += f'Отримувач: <a href="https://t.me/businesses_yachminiya/{business[7]}">{business[2]}</a> ' \
                   f'({business[4]})\n'
            msg += f'Сума переказу: {amount_m} {glas(amount_m)}\n'
            bot.send_message(m.chat.id, msg, parse_mode='HTML', disable_web_page_preview=True)
            bot.send_message(-1001282951480, f'Переказ коштів\nСума переказу: {amount_m} {glas(amount_m)}')

            business_f(business, m, False)
            insert_business_a(business)
            insert_passport_a(acc_g)
            update_channel_business(business[1])
            update_channel_rid(acc_g[13])

        bot.edit_message_text(
            text=f'{business[2]}\nВведіть суму коштів, яку ви хочете зняти з рахунку підприємства\n{stop_text}\n'
                 f'Активи: {business[4]} {glas(business[4])}\nСтатки: {acc_g[9]} {glas(acc_g[9])}',
            message_id=call.message.message_id, chat_id=call.message.chat.id, parse_mode='HTML')
        register_next_step_handler(call.message, count)
        return

    if call.data == 'salary':
        business = get_seans_business(u.id, m)
        if business is None:
            return

        id_list = business[5].split()
        salary_list = business[6].split()
        summa = 0
        for i in salary_list:
            summa += int(i)
        if summa == 0:
            keyboard = types.InlineKeyboardMarkup()
            callback_button = types.InlineKeyboardButton(text="⬅️ До підприємства",
                                                         callback_data=f"business{business[0]}")
            keyboard.add(callback_button)
            callback_button = types.InlineKeyboardButton(text=f"⬅️ До головного меню", callback_data=f"menul")
            keyboard.add(callback_button)
            bot.edit_message_text(
                f'У всіх працівників підприємства {business[2]} зарплата дорівнює нулю.',
                message_id=call.message.message_id, chat_id=call.message.chat.id, reply_markup=keyboard)
            return

        if summa > business[4]:
            keyboard = types.InlineKeyboardMarkup()
            callback_button = types.InlineKeyboardButton(text="⬅️ До підприємства",
                                                         callback_data=f"business{business[0]}")
            keyboard.add(callback_button)
            callback_button = types.InlineKeyboardButton(text=f"⬅️ До головного меню", callback_data=f"menul")
            keyboard.add(callback_button)
            bot.edit_message_text(
                'На рахунку вашого підприємства недостатньо коштів для виплати заробітньої плати',
                message_id=call.message.message_id, chat_id=call.message.chat.id, reply_markup=keyboard)
            return

        comm = commission(summa, 1)
        if summa + comm > business[4]:
            keyboard = types.InlineKeyboardMarkup()
            callback_button = types.InlineKeyboardButton(text="⬅️ До підприємства",
                                                         callback_data=f"business{business[0]}")
            keyboard.add(callback_button)
            callback_button = types.InlineKeyboardButton(text=f"⬅️ До головного меню", callback_data=f"menul")
            keyboard.add(callback_button)
            bot.edit_message_text(
                'На рахунку вашого підприємства недостатньо коштів для виплати комісії.',
                message_id=call.message.message_id, chat_id=call.message.chat.id, reply_markup=keyboard)
            return
        for i in range(2, len(id_list)):
            passport = get_passport(id_list[i])
            passport[9] = passport[9] + int(salary_list[i])
            try:
                bot.send_message(int(id_list[i]),
                                 f'Вам нарахували зарплату в підприємстві {business[2]} у розмірі {salary_list[i]} '
                                 f'{glas(salary_list[i])}')
            except:
                pass

        business[4] = int(business[4]) - summa - comm
        bot.edit_message_text(chat_id=call.message.chat.id, text='Заробітну плату успішно нараховано!',
                              message_id=call.message.message_id)
        bot.send_message(-1001282951480, 'Здійснено нарахування заробітної плати у підприємстві!')
        return

    if call.data == 'del_business':
        keyboard = types.InlineKeyboardMarkup()
        business = get_seans_business(u.id, m)
        if business is None:
            return
        number = business[7]
        callback_button = types.InlineKeyboardButton(text=f"❌Закрити", callback_data=f"del_business_done")
        keyboard.add(callback_button)
        callback_button = types.InlineKeyboardButton(text=f"⬅️ Назад", callback_data=f"business{number}")
        keyboard.add(callback_button)
        bot.edit_message_text(
            f'Ви дійсно хочете закрити підприємство <a href="https://t.me/businesses_yachminiya/{number}">{business[2]}'
            f'</a>? Ви втратите всі свої активи у ньому, '
            f'тому наполегливо радимо перенести їх на ваш особистий рахунок.',
            message_id=call.message.message_id, chat_id=call.message.chat.id, reply_markup=keyboard, parse_mode='HTML',
            disable_web_page_preview=True)
        return

    if call.data == 'del_business_done':
        business = get_seans_business(u.id, m)
        if business is None:
            return

        passport = get_passport(call.from_user.id)
        all_businesses = get_all_businesses()
        index = business[0]
        del all_businesses[index]
        for i in range(len(all_businesses)):
            all_businesses[i][0] = i + 1
        del_table_businesses()
        db.insert(table_businesses)
        insert_all_businesses_l(all_businesses)
        amount = get_amount_of_businesses()
        del_business_g(all_businesses, amount)

        keyboard = types.InlineKeyboardMarkup()
        callback_button = types.InlineKeyboardButton(text="⬅️ До підприємств", callback_data="business")
        keyboard.add(callback_button)
        callback_button = types.InlineKeyboardButton(text=f"⬅️ До головного меню", callback_data=f"menul")
        keyboard.add(callback_button)
        business_out = f'ПІДПРИЄМСТВО ЗАКРИТЕ'
        bot.edit_message_text(business_out, -1001162793975, business[7], parse_mode='HTML')
        del (business_seans[call.from_user.id])
        bot.edit_message_text(text='Ви закрили своє підприємство.', message_id=call.message.message_id,
                              chat_id=call.message.chat.id, reply_markup=keyboard)
        return
        # TODO вилучення з паспортів

    if call.data == 'state_menu':
        state_menu_f(u, m)
        return

    if call.data in (
            'Протектор', 'Граф', 'Скарбник', 'Старший Жандарм', 'Молодший Жандарм', 'Новобранець', 'Віконт', 'Карб'):
        state_emps_name = None
        if call.data in ('Протектор', 'Граф', 'Скарбник'):
            head = True
            if call.data == 'Протектор':
                short_ust = 'zh'
                per_name = 'Протектора'
                state_emps_name = 'Жандармами'
            elif call.data == 'Граф':
                short_ust = 'gr'
                per_name = 'Графа'
                state_emps_name = 'Ерлами'
            elif call.data == 'Скарбник':
                short_ust = 'bank'
                per_name = 'Скарбника'
                state_emps_name = 'Карбами'
            else:
                return
        else:
            head = False
            if call.data in ('Старший Жандарм', 'Молодший Жандарм', 'Новобранець'):
                short_ust = 'zh'
                per_name = 'Протектора'
            elif call.data == 'Віконт':
                short_ust = 'gr'
                per_name = 'Віконта'
            elif call.data == 'Карб':
                short_ust = 'bank'
                per_name = 'Карба'
            else:
                return
        keyboard = types.InlineKeyboardMarkup()
        button = types.InlineKeyboardButton(text='Особиста статистика', callback_data=f'stat_{short_ust}')
        keyboard.add(button)
        if head:
            button = types.InlineKeyboardButton(text=f'Керування {state_emps_name}', callback_data=f'con_{short_ust}')
            keyboard.add(button)
        button = types.InlineKeyboardButton(text='Переглянути документи громадянина Ячмінії',
                                            callback_data=f'document_check_{short_ust}')
        keyboard.add(button)
        keyboard = menu_footer(keyboard, 'state_menu')
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text=f'Меню {per_name}.',
                              reply_markup=keyboard)
        return

    spl_data = call.data.split('_')
    if spl_data[0] == 'stat':
        inst = get_institution(inst_shorts[spl_data[1]])
        get_all_employers, insert_emp_l, insert_all_employers_g, get_employer = get_inst_func(inst[1])[:4]
        if len(spl_data) == 3:
            emp = get_employer(int(spl_data[2]))
            passport = get_passport(int(spl_data[2]))
            back_callback = f'state_emp_{spl_data[2]}_{spl_data[1]}'
        else:
            emp = get_employer(u.id)
            passport = get_passport(u.id)
            back_callback = emp[2]
        keyboard = menu_footer(types.InlineKeyboardMarkup(), f'{back_callback}')
        if inst[1] == 'Жандармерія':
            doings_word = 'Вироків здійснено'
            try:
                am = zhan_queue[u.id]
            except:
                am = 0
                zhan_queue[u.id] = 0
            end = f'\nВироків виконано за останню годину: {am}/{zhan_rank[emp[2]][4]}'
        elif inst[1] == 'Графство':
            doings_word = 'Дій виконано'
            end = f''
        elif inst[1] == 'Державний Банк':
            doings_word = 'Звітів розглянуто'
            end = f''
        else:
            return
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text=f'{emp[2]}\n{user_link(passport[1], passport[2], passport[3])}'
                                   f'\n\n{doings_word} за весь час: {emp[3]}\n{doings_word} за час підзвітності: '
                                   f'{emp[4]}{end}',
                              reply_markup=keyboard, parse_mode='HTML')
        return

    if spl_data[0] == 'con':
        inst = get_institution(inst_shorts[spl_data[1]])
        get_all_employers, insert_emp_l, insert_all_employers_g, get_employer = get_inst_func(inst[1])[:4]
        if inst[1] == 'Жандармерія':
            all_emps = 'Жандармів'
            new_emp = 'Новобранця'
            msg_text = 'Жандармами'
        elif inst[1] == 'Графство':
            all_emps = 'Ерлів'
            new_emp = 'Віконта'
            msg_text = 'Ерлами'
        elif inst[1] == 'Державний Банк':
            all_emps = 'Карбів'
            new_emp = 'Карба'
            msg_text = 'Карбами'
        else:
            return
        keyboard = types.InlineKeyboardMarkup()
        button = types.InlineKeyboardButton(text=f'Статистика всіх {all_emps} та відправка звіту',
                                            callback_data=f'all_stat_{spl_data[1]}')
        keyboard.add(button)
        button = types.InlineKeyboardButton(text=f'Призначити громадянина на сан {new_emp}',
                                            callback_data=f'new_{spl_data[1]}')
        keyboard.add(button)
        button = types.InlineKeyboardButton(text=f'Список {all_emps}', callback_data=f'list_of_{spl_data[1]}')
        keyboard.add(button)
        keyboard = menu_footer(keyboard, get_employer(u.id)[2])
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text=f'Меню керування {msg_text}.',
                              reply_markup=keyboard)
        return

    if spl_data[0] == 'document' and spl_data[1] == 'check':
        keyboard = types.InlineKeyboardMarkup()
        button = types.InlineKeyboardButton(text='Переглянути паспорт громадянина Ячмінії', callback_data='pass_check')
        keyboard.add(button)
        if spl_data[2] in ('zh', 'bank'):
            button = types.InlineKeyboardButton(text='Переглянути рахунок громадянина Ячмінії',
                                                callback_data='acc_check')
            keyboard.add(button)
            san = get_zhan(u.id)[2]
        elif spl_data[2] == 'gr':
            san = get_erl(u.id)[2]
        else:
            san = 'state_menu'
        button = types.InlineKeyboardButton(text='Переглянути витяг з паспорта громадянина Ячмінії',
                                            callback_data='extract_list')
        keyboard.add(button)
        keyboard = menu_footer(keyboard, san)
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text=f'Меню перегляду документів.',
                              reply_markup=keyboard)
        return

    if spl_data[0] == 'all' and spl_data[1] == 'stat':
        keyboard = types.InlineKeyboardMarkup()
        button = types.InlineKeyboardButton(text='Відправити звіт за період підзвітності',
                                            callback_data=f'zvit_{spl_data[2]}')
        keyboard.add(button)
        keyboard = menu_footer(keyboard, f'con_{spl_data[2]}')
        inst = get_institution(inst_shorts[spl_data[2]])
        get_all_employers, insert_emp_l, insert_all_employers_g, get_employer = get_inst_func(inst[1])[:4]
        all_emps = get_all_employers()
        msg_out = f'Статистика всіх жандармів\n\nПерша колонка — період підзвітності, друга — за весь час\nПеріод ' \
                  f'підзвітності — {inst[7]}-{datetime.now().date().strftime("%d.%m.%Y")}\n\n'
        all_emps_sorted = sorted(all_emps, key=lambda x: len(get_passport(x[1])[2] + get_passport(x[1])[3]),
                                 reverse=True)
        name_len = len(get_passport(all_emps_sorted[0][1])[2] + get_passport(all_emps_sorted[0][1])[3])
        all_emps_sorted = sorted(all_emps, key=lambda x: x[3], reverse=True)
        per_len = len(str(all_emps_sorted[0][3]))
        all_emps_sorted = sorted(all_emps, key=lambda x: x[4], reverse=True)
        all_len = len(str(all_emps_sorted[0][4]))
        for i in all_emps:
            passport = get_passport(i[1])
            loc_name_len = len(passport[2] + passport[3])
            loc_per_len = len(str(i[3]))
            loc_all_len = len(str(i[4]))
            white1 = ' ' * (name_len - loc_name_len)
            white2 = ' ' * (per_len - loc_per_len)
            white3 = ' ' * (all_len - loc_all_len)
            msg_out += f'<code>{user_link(passport[1], passport[2], passport[3])}' \
                       f'{white1} {white3}{i[4]} {white2}{i[3]}</code>\n'
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text=msg_out, reply_markup=keyboard, parse_mode='HTML')

    if spl_data[0] == 'new':
        inst = get_institution(inst_shorts[spl_data[1]])
        get_all_employers, insert_emp_l, insert_all_employers_g, get_employer = get_inst_func(inst[1])[:4]
        if inst[1] == 'Жандармерія':
            new_emp_name = 'Новобранця Жандармерії'
        elif inst[1] == 'Графство':
            new_emp_name = 'Віконта'
        elif inst[1] == 'Державний Банк':
            new_emp_name = 'Карба'
        else:
            return
        bot.edit_message_text(
            f'Введіть id громадянина Ячмінії, якого ви хочете призначити на сан {new_emp_name}. '
            f'<a href="https://telegra.ph/YAk-d%D1%96znatis-id-akaunta-v-Telegram%D1%96-03-12">Як дізнатись id акаунта '
            f'в Телеграмі?</a>\n{stop_text}.',
            chat_id=call.message.chat.id, message_id=call.message.message_id, parse_mode='HTML')

        def new_emp_id(m):
            nonlocal new_emp, get_all_employers, insert_emp_l, insert_all_employers_g, get_employer
            if m.text == 'СТОП':
                bot.send_message(m.chat.id, f'Ви відмінили процедуру призначення на сан {new_emp_name}')
                state_menu_f(u, m, False)
                return

            if not m.text.isdigit():
                bot.send_message(m.chat.id,
                                 f'Вказаний неправильний ідентифікатор особи. Спробуйте знову.\n{stop_text}.',
                                 parse_mode='HTML')
                register_next_step_handler(m, new_emp_id)
                return

            id = int(m.text)
            new_emp = get_passport(id)
            if new_emp is None:
                bot.send_message(m.chat.id,
                                 f'Вказаний неправильний ідентифікатор або особа не має паспорта Ячмінії. Спробуйте '
                                 f'знову.\n{stop_text}.',
                                 parse_mode='HTML')
                register_next_step_handler(m, new_emp_id)
                return

            emp = get_employer(id)
            if emp:
                bot.send_message(m.chat.id,
                                 f'Цей громадянин уже є працівником вашої установи. Спробуйте знову.\n{stop_text}.',
                                 parse_mode='HTML')
                register_next_step_handler(m, new_emp_id)
                return

            try:
                keyboard = types.InlineKeyboardMarkup()
                button = types.InlineKeyboardButton(text='Підписати', callback_data='done_new_zh')
                keyboard.add(button)
                button = types.InlineKeyboardButton(text='Відмовитись', callback_data='cancel_new_zh')
                keyboard.add(button)
                bot.send_message(int(m.text),
                                 f'Вас хочуть призначити на сан {new_emp_name}. Поставте підпис для підтвердження '
                                 f'призначення.',
                                 parse_mode='HTML', disable_web_page_preview=True, reply_markup=keyboard)
                bot.send_message(m.chat.id,
                                 f'{user_link(new_emp[1], new_emp[2], new_emp[3])} отримав '
                                 f'повідомлення про призначення Новобранцем. Очікуйте підвердження.',
                                 parse_mode='HTML')
            except:
                bot.send_message(m.chat.id,
                                 'Громадянин не може прийняти повідомлення від Системи. Попросіть у нього, щоб він '
                                 'відновив чат з Системою.')
            state_menu_f(u, m, False)

        register_next_step_handler(call.message, new_emp_id)
        return

    if spl_data[0] == 'done' and spl_data[1] == 'new':
        inst = get_institution(inst_shorts[spl_data[2]])
        get_all_employers, insert_emp_l, insert_all_employers_g, get_employer, new_emp = get_inst_func(inst[1])[:5]
        passport = get_passport(u.id)
        user = get_user(u.id)
        if passport is None:
            keyboard = types.InlineKeyboardMarkup()
            callback_button = types.InlineKeyboardButton(text=f"⬅️ До головного меню", callback_data=f"menul")
            keyboard.add(callback_button)
            bot.edit_message_text(text='У вас нема громадянства Ячмінії', chat_id=m.chat.id, message_id=m.message_id,
                                  reply_markup=keyboard)
            return
        sans = passport[8].split(', ')
        if inst[1] == 'Жандармерія':
            new_san = 'Новобранець'
            doc = decree_new_zhan
        elif inst[1] == 'Графство':
            new_san = 'Віконт'
            doc = decree_new_erl
        elif inst[1] == 'Державний Банк':
            new_san = 'Карб'
            doc = decree_new_karb
        else:
            return
        if sans[0] == 'Без сану' or sans[0] == 'Безробітний':
            sans[0] = new_san
        else:
            sans.append(new_san)
        sans_all = get_sans(sans)
        keyboard = types.InlineKeyboardMarkup()
        button = types.InlineKeyboardButton(text='До головного меню', callback_data='menul')
        keyboard.add(button)
        bot.edit_message_text(f'Тепер Ви {new_san}!', message_id=call.message.message_id,
                              chat_id=call.message.chat.id, reply_markup=keyboard)

        bill = 0
        us_rights = ['0', '0', '0', '0', '0', '0', '0', '0', '0', '0']
        pass_rights = ['0', '0', '0', '0', '0']
        for i in sans_all:
            bill += i[2]
            us_rights_buf = i[3].split()
            pass_rights_buf = i[4].split()
            for j in range(len(us_rights_buf)):
                us_rights[j] = str(int(us_rights_buf[j]) | int(us_rights[j]))
            for j in range(len(pass_rights_buf)):
                pass_rights[j] = str(int(pass_rights_buf[j]) | int(pass_rights[j]))

        passport[12] = ' '.join(pass_rights)
        user[6] = ' '.join(us_rights)
        old_san = passport[8]
        passport[8] = ', '.join(sans)
        passport[11] = bill
        insert_passport_a(passport)
        insert_user_a(user)
        out = f'{user_link(passport[1], passport[2], passport[3])}\n{old_san} ⟹ {passport[8]}'
        # bot.send_message(-1001268255961, out, parse_mode='HTML')
        head = get_passport(inst[6])
        out = doc.replace('/link/', inst[5]).replace('/num/', str(inst[4] + 1)).replace(
            '/date/', datetime.now().date().strftime("%d.%m.%Y")).replace('/head_link/',
                                                                          f'{user_link(head[1], head[2], head[3])}'). \
            replace('/new_emp_acc_link/', f'{user_link(passport[1], passport[16], passport[17])}'). \
            replace('/new_emp_link/', f'{user_link(passport[1], passport[2], passport[3])}')
        bot.send_message(-1001124854070, out, parse_mode='HTML')
        new_emp(u)
        inst[4] += 1
        insert_institution_a(inst)
        return

    if spl_data[0] == 'cancel' and spl_data[1] == 'new':
        inst = get_institution(inst_shorts[spl_data[2]])
        if inst[1] == 'Жандармерія':
            new_emp_name = 'Новобранця Жандармерії'
        elif inst[1] == 'Графство':
            new_emp_name = 'Віконта'
        elif inst[1] == 'Державний Банк':
            new_emp_name = 'Карба'
        else:
            return
        keyboard = types.InlineKeyboardMarkup()
        keyboard.add(types.InlineKeyboardButton(text='До головного меню', callback_data='menu'))
        bot.edit_message_text(f'Ви відмовились від запиту', message_id=call.message.message_id,
                              chat_id=call.message.chat.id, reply_markup=keyboard)
        employer = get_passport(u.id)
        try:
            bot.send_message(inst[6],
                             f'{user_link(employer[1], employer[16], employer[17])} відмовився від '
                             f'запиту на призначення на сан {new_emp_name}',
                             parse_mode='HTML')
        except:
            pass
        return

    if spl_data[0] == 'list' and spl_data[1] == 'of':
        inst = get_institution(inst_shorts[spl_data[2]])
        get_all_employers, insert_emp_l, insert_all_employers_g, get_employer, new_emp = get_inst_func(inst[1])[:5]
        emps = get_all_employers()
        keyboard = types.InlineKeyboardMarkup()
        if inst[1] == 'Жандармерія':
            zh_lab = True
            msg_end = 'Жандармів\n\nУмовні позначення:\nСЖ — Старший Жандарм\nМЖ — Молодший Жандарм\nНБ — Новобранець'
        elif inst[1] == 'Графство':
            zh_lab = False
            msg_end = 'Ерлів'
        elif inst[1] == 'Державний Банк':
            zh_lab = False
            msg_end = 'Карбів'
        else:
            return
        for i in emps[1:]:
            passport = get_passport(i[1])
            if zh_lab:
                zh_rank = f'{zhan_rank[i[2]][0]} – '
            else:
                zh_rank = ''
            button = types.InlineKeyboardButton(text=f'{zh_rank}{passport[2]} {passport[3]}',
                                                callback_data=f'state_emp_{passport[1]}_{spl_data[2]}')
            keyboard.add(button)
        emp = get_employer(u.id)
        keyboard = menu_footer(keyboard, emp[2])
        bot.edit_message_text(
            text=f'Список {msg_end}',
            chat_id=m.chat.id, message_id=m.message_id, reply_markup=keyboard)
        return

    if spl_data[0] == 'state' and spl_data[1] == 'emp':
        emp_id = int(spl_data[2])
        inst = get_institution(inst_shorts[spl_data[3]])
        get_all_employers, insert_emp_l, insert_all_employers_g, get_employer, new_emp = get_inst_func(inst[1])[:5]
        emp = get_employer(emp_id)
        passport = get_passport(emp_id)
        keyboard = types.InlineKeyboardMarkup()

        if inst[1] == 'Жандармерія':
            button = types.InlineKeyboardButton(text='Змінити звання Жандарма', callback_data='change_zhan_rank')
            keyboard.add(button)
            emp_name = 'Жандарма'
        elif inst[1] == 'Графство':
            emp_name = 'Віконта'
        elif inst[1] == 'Державний Банк':
            emp_name = 'Карба'
        else:
            return
        button = types.InlineKeyboardButton(text=f'Особиста статистика {emp_name}', callback_data=f'stat_zh_{emp_id}')
        keyboard.add(button)
        button = types.InlineKeyboardButton(text=f'Звільнити {emp_name}', callback_data='del_zh')
        keyboard.add(button)
        keyboard = menu_footer(keyboard, f'list_of_{spl_data[3]}')
        bot.edit_message_text(text=f'{emp[2]}\n{user_link(passport[1], passport[2], passport[3])}',
                              chat_id=m.chat.id, message_id=m.message_id, reply_markup=keyboard, parse_mode='HTML')
        return

    if call.data == 'change_zhan_rank':
        keyboard = types.InlineKeyboardMarkup()
        mess = m.text.split('\n')
        rank = mess[0]
        rank_l = zhan_rank[rank]
        u = m.entities[0].user
        for i in range(2):
            button = types.InlineKeyboardButton(text=rank_l[2][i], callback_data=rank_l[3][i])
            keyboard.add(button)
        keyboard = menu_footer(keyboard, f'zhandarm{u.id}')
        passport = get_passport(u.id)
        bot.edit_message_text(
            text=f'{rank}\n{user_link(passport[1], passport[2], passport[3])}\nОберіть нове звання '
                 f'Жандарма',
            chat_id=m.chat.id, message_id=m.message_id, reply_markup=keyboard, parse_mode='HTML')
        return

    if call.data[:5] == 'up_zh' and len(call.data) < 7:
        r = int(call.data[5])
        u = m.entities[0].user
        keyboard = types.InlineKeyboardMarkup()
        button = types.InlineKeyboardButton(text='Підвищити', callback_data=f'up_zh_done{r}')
        keyboard.add(button)
        keyboard = menu_footer(keyboard, f'zhandarm{u.id}')
        passport = get_passport(u.id)
        if r == 1:
            rank = 'Молодшого Жандарма'
        else:
            rank = 'Старшого Жандарма'
        bot.edit_message_text(
            text=f'Ви дійсно хочете підвищити {user_link(passport[1], passport[16], passport[17])} '
                 f'до звання {rank}?',
            chat_id=m.chat.id, message_id=m.message_id, reply_markup=keyboard, parse_mode='HTML')
        return

    if call.data[:10] == 'up_zh_done':
        r = int(call.data[10])
        u = m.entities[0].user
        passport = get_passport(u.id)
        user = get_user(u.id)
        if r == 1:
            rank = 'Молодший Жандарм'
            rank_g = 'Молодшого Жандарма'
        else:
            rank = 'Старший Жандарм'
            rank_g = 'Старшого Жандарма'
        new_san = passport[8].replace('Молодший Жандарм', rank).replace('Новобранець', rank)
        sans = new_san.split(', ')
        sans_all = get_sans(sans)
        keyboard = types.InlineKeyboardMarkup()
        button = types.InlineKeyboardButton(text='До меню Протектора', callback_data='Протектор')
        keyboard.add(button)
        bot.edit_message_text(
            f'{user_link(passport[1], passport[2], passport[3])} підвищений у званні до {rank_g}',
            message_id=call.message.message_id,
            chat_id=call.message.chat.id, parse_mode='HTML', reply_markup=keyboard)

        bill = 0
        us_rights = ['0', '0', '0', '0', '0', '0', '0', '0', '0', '0']
        pass_rights = ['0', '0', '0', '0', '0']
        for i in sans_all:
            bill += i[2]
            us_rights_buf = i[3].split()
            pass_rights_buf = i[4].split()
            for j in range(len(us_rights_buf)):
                us_rights[j] = str(int(us_rights_buf[j]) | int(us_rights[j]))
            for j in range(len(pass_rights_buf)):
                pass_rights[j] = str(int(pass_rights_buf[j]) | int(pass_rights[j]))

        passport[12] = ' '.join(pass_rights)
        user[6] = ' '.join(us_rights)
        old_san = passport[8]
        passport[8] = ', '.join(sans)
        passport[11] = bill
        insert_passport_a(passport)
        insert_user_a(user)
        out = f'{user_link(passport[1], passport[2], passport[3])}\n{old_san} ⟹ {passport[8]}'
        # bot.send_message(-1001268255961, out, parse_mode='HTML')
        inst = get_institution('Жандармерія')
        head = get_passport(inst[6])
        out = decree_up_zhan.replace('/link/', inst[5]).replace('/num/', str(inst[4] + 1)).replace(
            '/date/', datetime.now().date().strftime("%d.%m.%Y")).replace('/prot_link/',
                                                                          f'<a href="tg://user?id={head[1]}">{head[2]} '
                                                                          f'{head[3]}</a>').replace(
            '/up_zhan_acc_link/', f'{user_link(passport[1], passport[16], passport[17])}').replace(
            '/rank_g/', rank_g)
        bot.send_message(-1001124854070, out, parse_mode='HTML')
        emp = get_zhan(u.id)
        emp[2] = rank
        insert_zhan_a(emp)
        inst[4] += 1
        insert_institution_a(inst)
        return

    if call.data[:7] == 'down_zh' and len(call.data) < 9:
        r = int(call.data[7])
        u = m.entities[0].user
        keyboard = types.InlineKeyboardMarkup()
        button = types.InlineKeyboardButton(text='Понизити', callback_data=f'down_zh_done{r}')
        keyboard.add(button)
        keyboard = menu_footer(keyboard, f'zhandarm{u.id}')
        passport = get_passport(u.id)
        if r == 1:
            rank = 'Молодшого Жандарма'
        else:
            rank = 'Новобранця'
        bot.edit_message_text(
            text=f'Ви дійсно хочете понизити {user_link(passport[1], passport[16], passport[17])} '
                 f'до звання {rank}?',
            chat_id=m.chat.id, message_id=m.message_id, reply_markup=keyboard, parse_mode='HTML')
        return

    if call.data[:12] == 'down_zh_done':
        r = int(call.data[12])
        u = m.entities[0].user
        passport = get_passport(u.id)
        user = get_user(u.id)
        if r == 1:
            rank = 'Молодший Жандарм'
            rank_g = 'Молодшого Жандарма'
        else:
            rank = 'Новобранець'
            rank_g = 'Новобранця'
        new_san = passport[8].replace('Молодший Жандарм', rank).replace('Старший Жандарм', rank)
        sans = new_san.split(', ')
        sans_all = get_sans(sans)
        keyboard = types.InlineKeyboardMarkup()
        button = types.InlineKeyboardButton(text='До меню Протектора', callback_data='Протектор')
        keyboard.add(button)
        bot.edit_message_text(
            f'{user_link(passport[1], passport[16], passport[17])} понижений у званні до {rank_g}',
            message_id=call.message.message_id,
            chat_id=call.message.chat.id, parse_mode='HTML', reply_markup=keyboard)

        bill = 0
        us_rights = ['0', '0', '0', '0', '0', '0', '0', '0', '0', '0']
        pass_rights = ['0', '0', '0', '0', '0']
        for i in sans_all:
            bill += i[2]
            us_rights_buf = i[3].split()
            pass_rights_buf = i[4].split()
            for j in range(len(us_rights_buf)):
                us_rights[j] = str(int(us_rights_buf[j]) | int(us_rights[j]))
            for j in range(len(pass_rights_buf)):
                pass_rights[j] = str(int(pass_rights_buf[j]) | int(pass_rights[j]))

        passport[12] = ' '.join(pass_rights)
        user[6] = ' '.join(us_rights)
        old_san = passport[8]
        passport[8] = ', '.join(sans)
        passport[11] = bill
        insert_passport_a(passport)
        insert_user_a(user)
        out = f'{user_link(passport[1], passport[2], passport[3])}\n{old_san} ⟹ {passport[8]}'
        # bot.send_message(-1001268255961, out, parse_mode='HTML')
        inst = get_institution('Жандармерія')
        head = get_passport(inst[6])
        out = decree_down_zhan.replace('/link/', inst[5]).replace('/num/', str(inst[4] + 1)).replace(
            '/date/', datetime.now().date().strftime("%d.%m.%Y")).replace('/prot_link/',
                                                                          f'<a href="tg://user?id={head[1]}">{head[2]} '
                                                                          f'{head[3]}</a>').replace(
            '/down_zhan_acc_link/', f'{user_link(passport[1], passport[16], passport[17])}').replace(
            '/rank_g/', rank_g)
        bot.send_message(-1001124854070, out, parse_mode='HTML')
        emp = get_zhan(u.id)
        emp[2] = rank
        insert_zhan_a(emp)
        inst[4] += 1
        insert_institution_a(inst)
        return

    if spl_data[0] == 'del':
        inst = get_institution(inst_shorts[spl_data[1]])
        if inst[1] == 'Жандармерія':
            emp_name = 'Жандарма'
        elif inst[1] == 'Графство':
            emp_name = 'Віконта'
        elif inst[1] == 'Державний Банк':
            emp_name = 'Карба'
        else:
            return
        u = m.entities[0].user
        keyboard = types.InlineKeyboardMarkup()
        button = types.InlineKeyboardButton(text='Звільнити', callback_data=f'done_del_{spl_data[1]}')
        keyboard.add(button)
        keyboard = menu_footer(keyboard, f'state_emp_{u.id}_{spl_data[1]}')
        passport = get_passport(u.id)
        bot.edit_message_text(
            text=f'Ви дійсно хочете звільнити {user_link(passport[1], passport[16], passport[17])} '
                 f'з сану {emp_name}?',
            chat_id=m.chat.id, message_id=m.message_id, reply_markup=keyboard, parse_mode='HTML')
        return

    if spl_data[0] == 'done' and spl_data[1] == 'del':
        inst = get_institution(inst_shorts[spl_data[2]])
        get_all_employers, insert_emp_l, insert_all_employers_g, get_employer, new_emp, del_table_inst, table_inst, \
        insert_all_employers_l, get_amount_of_emps, del_emp_g = get_inst_func(
            inst[1])
        if inst[1] == 'Жандармерія':
            emp_name = 'Жандарма'
            doc = decree_del_zhan
        elif inst[1] == 'Графство':
            emp_name = 'Віконта'
            doc = decree_del_erl
        elif inst[1] == 'Державний Банк':
            emp_name = 'Карба'
            doc = decree_del_karb
        else:
            return
        u = m.entities[0].user
        passport = get_passport(u.id)
        user = get_user(u.id)
        emp = get_employer(u.id)
        sans = passport[8].split(', ')
        del (sans[sans.index(emp[2])])
        if len(sans) == 0:
            sans.append('Без сану')
        sans_all = get_sans(sans)
        keyboard = types.InlineKeyboardMarkup()
        button = types.InlineKeyboardButton(text='До меню держслужбовця', callback_data=get_employer(u.id)[2])
        keyboard.add(button)
        bot.edit_message_text(
            f'{user_link(passport[1], passport[2], passport[3])} звільнений з сану {emp_name}.',
            message_id=call.message.message_id,
            chat_id=call.message.chat.id, parse_mode='HTML', reply_markup=keyboard)
        bill = 0
        us_rights = ['0', '0', '0', '0', '0', '0', '0', '0', '0', '0']
        pass_rights = ['0', '0', '0', '0', '0']
        for i in sans_all:
            bill += i[2]
            us_rights_buf = i[3].split()
            pass_rights_buf = i[4].split()
            for j in range(len(us_rights_buf)):
                us_rights[j] = str(int(us_rights_buf[j]) | int(us_rights[j]))
            for j in range(len(pass_rights_buf)):
                pass_rights[j] = str(int(pass_rights_buf[j]) | int(pass_rights[j]))

        passport[12] = ' '.join(pass_rights)
        user[6] = ' '.join(us_rights)
        old_san = passport[8]
        passport[8] = ', '.join(sans)
        passport[11] = bill
        insert_passport_a(passport)
        insert_user_a(user)
        out = f'{user_link(passport[1], passport[2], passport[3])}\n{old_san} ⟹ {passport[8]}'
        # bot.send_message(-1001268255961, out, parse_mode='HTML')
        inst = get_institution('Жандармерія')
        head = get_passport(inst[6])
        out = doc.replace('/link/', inst[5]).replace('/num/', str(inst[4] + 1)).replace(
            '/date/', datetime.now().date().strftime("%d.%m.%Y")). \
            replace('/head_link/', f'{user_link(head[1], head[2], head[3])}').replace(
            '/del_emp_acc_link/', f'{user_link(passport[1], passport[16], passport[17])}')
        bot.send_message(-1001124854070, out, parse_mode='HTML')

        all_emps = get_all_employers()
        del (all_emps[emp[0] - 1])
        for i in range(len(all_emps)):
            all_emps[i][0] = i + 1
        del_table_inst()
        db.insert(table_inst)
        insert_all_employers_l(all_emps)
        amount = get_amount_of_emps()
        del_emp_g(all_emps, amount)

        inst[4] += 1
        insert_institution_a(inst)
        return

    if call.data == 'pass_check':
        bot.edit_message_text(
            f'Введіть id громадянина Ячмінії, чий паспорт ви хочете переглянути. '
            f'<a href="https://telegra.ph/YAk-d%D1%96znatis-id-akaunta-v-Telegram%D1%96-03-12">Як дізнатись id акаунта '
            f'в Телеграмі?</a>\n{stop_text}',
            chat_id=call.message.chat.id, message_id=call.message.message_id, parse_mode='HTML')

        def new_emp_id(m):
            if m.text == 'СТОП':
                bot.send_message(m.chat.id, 'Ви відмінили перегляд паспорту')
                state_menu_f(u, m, False)
                return
            keyboard = menu_footer(types.InlineKeyboardMarkup(), 'Протектор')
            bot.send_message(m.chat.id, get_str_passport(m.text), parse_mode='HTML', reply_markup=keyboard)

        register_next_step_handler(call.message, new_emp_id)
        return

    if call.data == 'acc_check':
        bot.edit_message_text(
            f'Введіть id громадянина Ячмінії, чий рахунок ви хочете переглянути. '
            f'<a href="https://telegra.ph/YAk-d%D1%96znatis-id-akaunta-v-Telegram%D1%96-03-12">Як дізнатись id акаунта '
            f'в Телеграмі?</a>\n{stop_text}.',
            chat_id=call.message.chat.id, message_id=call.message.message_id, parse_mode='HTML')

        def new_emp_id(m):
            if m.text == 'СТОП':
                bot.send_message(m.chat.id, 'Ви відмінили перегляд рахунку')
                state_menu_f(u, m, False)
                return
            keyboard = menu_footer(types.InlineKeyboardMarkup(), 'Протектор')
            bot.send_message(m.chat.id, get_str_acc(m.text), parse_mode='HTML', reply_markup=keyboard)

        register_next_step_handler(call.message, new_emp_id)
        return

    if spl_data[0] == 'zvit':
        inst = get_institution(inst_shorts[spl_data[1]])
        if time.time() - datetime.strptime(inst[7], '%d.%m.%Y').timestamp() < 259200:
            bot.answer_callback_query(callback_query_id=call.id,
                                      text='Не можна відправляти звіти частіше, ніж раз у 3 дні', show_alert=True)
            return
        bot.edit_message_text(chat_id=m.chat.id, message_id=m.message_id,
                              text=f'Напишіть коментар до звіту.\nЯкщо ви не бажаєте залишати коментар, введіть '
                                   f'<code>Без коментарів</code>.\n{stop_text}',
                              parse_mode='HTML')

        def zvit_done(m):
            nonlocal inst
            if m.text == 'СТОП':
                keyboard = menu_footer(types.InlineKeyboardMarkup(), f'all_stat_{spl_data[1]}', '⬅️ До статистики')
                bot.send_message(m.chat.id, 'Ви відмінили відправку звіту.', reply_markup=keyboard)
                return
            msg_out = f'Звіт про діяльність {inst[2]} за період ' \
                      f'{inst[7]}-{datetime.now().date().strftime("%d.%m.%Y")}\n\nВиконано дій за час підзвітності:\n\n'

            get_all_employers, insert_emp_l, insert_all_employers_g = get_inst_func(inst[1])[:3]
            all_employers = get_all_employers()
            all_employers_sorted = sorted(all_employers,
                                          key=lambda x: len(get_passport(x[1])[2] + get_passport(x[1])[3]),
                                          reverse=True)
            name_len = len(get_passport(all_employers_sorted[0][1])[2] + get_passport(all_employers_sorted[0][1])[3])
            all_employers_sorted = sorted(all_employers, key=lambda x: x[3], reverse=True)
            per_len = len(str(all_employers_sorted[0][3]))
            for i in all_employers:
                passport = get_passport(i[1])
                loc_name_len = len(passport[2] + passport[3])
                loc_per_len = len(str(i[4]))
                white1 = ' ' * (name_len - loc_name_len)
                white2 = ' ' * (per_len - loc_per_len)
                msg_out += f'<code>{user_link(passport[1], passport[2], passport[3])}' \
                           f'{white1} {white2}{i[4]}</code>\n'
            passport = get_passport(m.from_user.id)

            if m.text != 'Без коментарів':
                msg_out += f'\nКоментар:\n{m.text}\n'
            msg_out += f'\nПідписано:\n{user_link(passport[1], passport[2], passport[3])}'
            message = bot.send_message(-1001511247539, msg_out, parse_mode='HTML')
            msg_out = f'Звіт про діяльність {inst[2]} за період {inst[7]}-{datetime.now().date().strftime("%d.%m.%Y")}'
            n = bot.send_message(-1001543732225, msg_out, parse_mode='HTML').message_id
            keyboard = types.InlineKeyboardMarkup()
            button = types.InlineKeyboardButton(text='Переглянути звіт',
                                                url=f't.me/yachminiya_test_bot?start=zvit_{n}_{message.message_id}')
            keyboard.add(button)
            bot.edit_message_reply_markup(-1001543732225, n, reply_markup=keyboard)
            keyboard = menu_footer(types.InlineKeyboardMarkup(), all_employers[0][2], 'До меню держслужбовця')
            bot.send_message(u.id,
                             f'<a href="https://t.me/c/1543732225/{n}">Звіт опубліковано</a>. Ви можете повернутись до '
                             f'головного меню', reply_markup=keyboard, parse_mode='HTML')
            for i in all_employers:
                i[4] = 0
                insert_emp_l(i)
            insert_all_employers_g(all_employers)
            inst[7] = f'{datetime.now().date().strftime("%d.%m.%Y")}'
            insert_institution_a(inst)

        register_next_step_handler(m, zvit_done)
        return

    if spl_data[0] == 'finance' and spl_data[1] == 'zvit':
        passport = get_passport(u.id)
        if passport is None:
            return
        bot.edit_message_reply_markup(m.chat.id, m.message_id, reply_markup=None)
        m_id = int(spl_data[2])
        msg = bot.forward_message(thrash, -1001543732225, m_id)
        zvit_text = msg.text

        def get_am_of_money(m):
            if m.text == 'СТОП':
                bot.send_message(m.chat.id, 'Ви відмінили проведення фінансування')
                main_menu(m, False)
                return
            if not m.text.isdigit():
                m = bot.send_message(m.chat.id, f'Неправильний формат повідомлення. Спробуйте знову. {stop_text}')
                register_next_step_handler(m, get_am_of_money)
                return
            am = int(m.text)
            if am == 0:
                m = bot.send_message(m.chat.id, f'Кількість ячок не може бути нульовою. Спробуйте знову. {stop_text}')
                register_next_step_handler(m, get_am_of_money)
                return
            if am > 1000000:
                m = bot.send_message(m.chat.id, f'Введене завелике число ячок. Спробуйте знову. {stop_text}')
                register_next_step_handler(m, get_am_of_money)
                return

            def get_comment(m):
                nonlocal zvit_text, am, passport, u
                if m.text == 'СТОП':
                    bot.send_message(m.chat.id, 'Ви відмінили проведення фінансування')
                    main_menu(m, False)
                    return
                if len(m.text) > 2000:
                    m = bot.send_message(m.chat.id, f'Занадто довгий текст коментаря, спробуйте ще раз. {stop_text}')
                    register_next_step_handler(m, get_comment)
                    return
                ln = '\n'
                msg_out = f'Звіт про нарахування коштів на підставах звіту ' \
                          f'{" ".join(zvit_text.split(ln)[0].split()[1:])}\n'
                msg_out += f'\nСума нарахування: {am} {glas(am)}\n'
                msg_out += f'\nКоментар:\n{m.text}\n'
                msg_out += f'\nПідписано:\n{user_link(passport[1], passport[2], passport[3])}'
                m = bot.send_message(-1001511247539, msg_out, parse_mode='HTML')
                msg_out = f'{zvit_text}\n\nЗвіт про нарахування коштів на підставах звіту ' \
                          f'{" ".join(zvit_text.split()[1:-3])}\n' \
                          f'Опубліковано {datetime.now().date().strftime("%d.%m.%Y")}'
                keyboard = types.InlineKeyboardMarkup()
                keyboard.add(types.InlineKeyboardButton(text='Переглянути звіт про діяльність',
                                                        url=f't.me/yachminiya_test_bot?start=zvitd_'
                                                            f'{spl_data[2]}_{spl_data[3]}'))
                keyboard.add(types.InlineKeyboardButton(text='Переглянути звіт про нарахування коштів',
                                                        url=f't.me/yachminiya_test_bot?start=finzvit_'
                                                            f'{spl_data[2]}_{m.id}'))
                bot.edit_message_text(text=msg_out, chat_id=-1001543732225, message_id=spl_data[2],
                                      reply_markup=keyboard, parse_mode='HTML')
                inst = get_institution(inst_shorts[" ".join(zvit_text.split()[3:-3])])
                try:
                    keyboard = types.InlineKeyboardMarkup()
                    button = types.InlineKeyboardButton(text='Переглянути фінансовий звіт',
                                                        url=f'https://t.me/c/1543732225/{spl_data[2]}')
                    keyboard.add(button)
                    bot.send_message(inst[6],
                                     f"Установа <b>{inst[1]}</b> отримала фінансування за період "
                                     f"{zvit_text.split()[-1]}. Ви зобов'язані надати звіт про розпорядження "
                                     f"отриманими фінансами. Для цього натисніть кнопку нижче, ви будете "
                                     f"перенаправлені на "
                                     f"повідомлення зі звітами. Там натисність на кнопку перегляду фінансового звіту, "
                                     f"яка перенаправить вас сюди.\n\nУВАГА!\nЯкщо ви не відправите звіт протягом "
                                     f"наступних 3 днів, ви можете бути притягнути до кримінальної відповідальності.",
                                     reply_markup=keyboard, parse_mode='HTML')
                except Exception as e:
                    print(e)
                bot.send_message(u.id,
                                 f'<a href="https://t.me/c/1543732225/{spl_data[2]}">Звіт опубліковано</a>. Ви можете '
                                 f'повернутись до головного меню', reply_markup=keyboard, parse_mode='HTML')
                inst[3] += am
                insert_institution_a(inst)

            m = bot.send_message(m.chat.id,
                                 f"Напишіть коментар (обов'язково)\n{stop_text}",
                                 parse_mode='HTML')
            register_next_step_handler(m, get_comment)

        m = bot.send_message(m.chat.id, f'Введіть кількість ячок, які ви хочете нарахувати на рахунок установи. '
                                        f'{stop_text}', parse_mode='HTML')
        register_next_step_handler(m, get_am_of_money)
        return

    if spl_data[0] == 'finzvit':
        bot.edit_message_reply_markup(m.chat.id, m.message_id, reply_markup=None)
        m_id = spl_data[3]
        bot.copy_message(m.chat.id, -1001511247539, int(m_id))
        mess_id = int(spl_data[1])
        msg = bot.forward_message(thrash, -1001543732225, mess_id)
        zvit_text = msg.text
        inst = get_institution(inst_shorts[" ".join(zvit_text.split('\n')[0].split()[3:-3])])
        if inst[1] == 'Жандармерія':
            emp_name = 'Жандармами'
            emp_name_1 = 'Жандармів'
            emp_name_2 = 'Жандарма'
        elif inst[1] == 'Графство':
            emp_name = 'Віконтами'
            emp_name_1 = 'Віконтів'
            emp_name_2 = 'Віконта'
        elif inst[1] == 'Державний Банк':
            emp_name = 'Карбами'
            emp_name_1 = 'Карбів'
            emp_name_2 = 'Карба'
        else:
            return

        msg_out = 'Згідно зі звітами про діяльність та нарахування коштів здійсніть розподіл отриманих коштів між ' \
                  f'{emp_name} {inst[2]}\nСписок працівників:\n\n'
        get_employers, insert_emp_l, insert_all_employers_g = get_inst_func(inst[1])[:3]
        emps = get_employers()
        for i in emps:
            passport = get_passport(i[1])
            msg_out += f'{user_link(passport[1], passport[2], passport[3])}\n'
        msg_out += f'\nВведіть кількість ячок, яку ви хочете нарахувати кожному із {emp_name_1} строго у тому ж ' \
                   f'порядку, що і в цьому повіломленні. Для кожного {emp_name_2} — з нового рядка. Приклад.'
        m = bot.send_message(m.chat.id, msg_out, parse_mode='HTML')

        def get_msg(m):
            if m.text == 'СТОП':
                bot.send_message(m.chat.id, 'Ви відмінили процедуру розподілу коштів')
                main_menu(m, False)
                return

            spl_text = m.text.split('\n')
            moneys_list = []
            for i in spl_text:
                if i.isdigit():
                    moneys_list.append(int(i))
                else:
                    bot.send_message(m.chat.id, 'Неправильний формат повідомлення')
                    register_next_step_handler(m, get_msg)
                    return

            if len(moneys_list) != len(emps):
                bot.send_message(m.chat.id, f'Кількість рядків має бути рівною кількості {emp_name_2}')
                register_next_step_handler(m, get_msg)
                return

            m = bot.send_message(m.chat.id, 'Напишіть коментар до звіту.')

            def get_comm(m):
                nonlocal emps
                if m.text == 'СТОП':
                    bot.send_message(m.chat.id, 'Ви відмінили процедуру розподілу коштів')
                    main_menu(m, False)
                    return
                m_id = int(spl_data[1])
                msg = bot.forward_message(thrash, -1001543732225, m_id)
                zvit_text = msg.text
                passport = get_passport(m.from_user.id)

                ln = '\n'
                msg_out = f'Звіт про розподіл коштів на підставах звіту про нарахування коштів за ' \
                          f'{zvit_text.split(ln)[3].split(" ")[1]}\n\n'

                all_employers_sorted = sorted(emps,
                                              key=lambda x: len(get_passport(x[1])[2] + get_passport(x[1])[3]),
                                              reverse=True)
                for i in emps:
                    i.append(moneys_list[i[0] - 1])
                name_len = len(
                    get_passport(all_employers_sorted[0][1])[2] + get_passport(all_employers_sorted[0][1])[3])
                all_employers_sorted = sorted(emps, key=lambda x: x[-1], reverse=True)
                per_len = len(str(all_employers_sorted[0][-1]))
                for i in emps:
                    passport = get_passport(i[1])
                    loc_name_len = len(passport[2] + passport[3])
                    loc_per_len = len(str(i[4]))
                    white1 = ' ' * (name_len - loc_name_len)
                    white2 = ' ' * (per_len - loc_per_len)
                    msg_out += f'<code>{user_link(passport[1], passport[2], passport[3])}' \
                               f'{white1} {white2}{i[4]}</code>\n'

                passport = get_passport(m.from_user.id)
                msg_out += f'\nКоментар:\n{m.text}\n'
                msg_out += f'\nПідписано:\n{user_link(passport[1], passport[2], passport[3])}'
                m = bot.send_message(-1001511247539, msg_out, parse_mode='HTML')
                msg_out = f'{zvit_text}\n\nЗвіт про розподіл коштів на підставах звіту про нарахування коштів за ' \
                          f'{zvit_text.split(ln)[3].split(" ")[1]}\n' \
                          f'Опубліковано {datetime.now().date().strftime("%d.%m.%Y")}'
                keyboard = types.InlineKeyboardMarkup()
                keyboard.add(types.InlineKeyboardButton(text='Переглянути звіт про діяльність',
                                                        url=f't.me/yachminiya_test_bot?start=zvitd_'
                                                            f'{spl_data[1]}_{spl_data[3]}'))
                keyboard.add(types.InlineKeyboardButton(text='Переглянути звіт про нарахування коштів',
                                                        url=f't.me/yachminiya_test_bot?start=finzvitd_'
                                                            f'{spl_data[1]}_{spl_data[2]}'))
                keyboard.add(types.InlineKeyboardButton(text='Переглянути звіт про розподіл коштів',
                                                        url=f't.me/yachminiya_test_bot?start=rozp_'
                                                            f'{spl_data[1]}_{m.id}'))
                bot.edit_message_text(text=msg_out, chat_id=-1001543732225, message_id=spl_data[1],
                                      reply_markup=keyboard, parse_mode='HTML')

                '''
                all_passports = get_all_passports()
                for i in range(len(emps)):
                    passport = get_passport(emps[i][1])
                    passport[9] += moneys_list[i]
                    insert_passport_l(passport)
                    all_passports[passport[0] - 1][9] += moneys_list[i]
                insert_all_passports_g(all_passports)'''

            register_next_step_handler(m, get_comm)

        register_next_step_handler(m, get_msg)
        return

    if call.data == 'prostir_menu':
        prostir_menu_f(u, m)
        return

    if spl_data[0] == 'private' and spl_data[1] in ('chats', 'channels'):
        if spl_data[1] == 'chats':
            all_ch = get_all_chats()
            adnum = 13
            str_in0 = 'chat'
            str_in1 = 'чатів'
            str_in2 = 'чати'
            str_in3 = ". Чат з'явиться тут, і ви зможете адмініструвати його."
        else:
            all_ch = get_all_channels()
            adnum = 7
            str_in0 = 'channel'
            str_in1 = 'каналів'
            str_in2 = 'канали'
            str_in3 = " і напишіть будь-яке повідомлення у каналі. " \
                      "Канал з'явиться тут, і ви зможете адмініструвати його."
        keyboard = types.InlineKeyboardMarkup()
        buttons = []
        for i in all_ch:
            if str(call.from_user.id) in i[adnum].split():
                but = types.InlineKeyboardButton(i[2], callback_data=f'private_{str_in0}_{i[1]}')
                buttons.append(but)
        n = int(spl_data[2])
        ln = 5 + n * 5
        zero = False
        more = True
        if len(buttons) == 0:
            zero = True
        elif len(buttons) <= ln:
            more = False
            ln = len(buttons)

        if zero:
            msg_text = f'У вас нема приватних {str_in1}. Додайте бота у якийсь зі своїх {str_in1}{str_in3}'
            keyboard = menu_footer(keyboard, "prostir_menu")
            bot.edit_message_text(msg_text, m.chat.id, m.message_id, reply_markup=keyboard, parse_mode='HTML')
            return
        if more:
            for i in range(n * 5, ln):
                keyboard.keyboard.append([buttons[i]])
            if n:
                but0 = types.InlineKeyboardButton('◀️', callback_data=f'private_{str_in0}s_{n - 1}')
            else:
                but0 = types.InlineKeyboardButton('⏺', callback_data=f'empty')
            but1 = types.InlineKeyboardButton('▶️', callback_data=f'private_{str_in0}s_{n + 1}')
            keyboard.keyboard.append([but0, but1])
            msg_text = f'Ваші приватні {str_in2}. [{1 + n * 5}-{ln}]'
        else:
            for i in range(n * 5, ln):
                keyboard.keyboard.append([buttons[i]])
            if n:
                but0 = types.InlineKeyboardButton('◀️', callback_data=f'private_{str_in0}s_{n - 1}')
            else:
                but0 = types.InlineKeyboardButton('⏺', callback_data=f'empty')
            but1 = types.InlineKeyboardButton('⏺', callback_data=f'empty')
            keyboard.keyboard.append([but0, but1])
            msg_text = f'Список ваших приватних {str_in1}. [{1 + n * 5}-{ln}]'

        keyboard = menu_footer(keyboard, "prostir_menu")
        bot.edit_message_text(msg_text, m.chat.id, m.message_id, reply_markup=keyboard, parse_mode='HTML')
        return

    if call.data == 'empty':
        bot.answer_callback_query(call.id, text='Ця кнопка не виконує дій, окрім показу цього повідомлення. '
                                                'Не натискай її, будь ласка.', show_alert=True)
        return

    if call.data == 'in_development':
        bot.answer_callback_query(call.id, text='Якщо ви бачите це повідомлення, функція яку ви хочете використати ще '
                                                'не готова, і наразі проводиться її розробка.', show_alert=True)
        return

    if spl_data[0] == 'private' and spl_data[1] in ('chat', 'channel') and len(spl_data) < 4:
        if spl_data[1] == 'chat':
            check = True
            ch = get_chat(int(spl_data[2]))
            is_on = 8
            ch_name = 'chat'
            ch_name1 = 'чаті'
            own = 7
            linked = 14
            link = 4
            ch_name2 = 'каналу'
            ch_name3 = 'Чат'
        else:
            check = False
            ch = get_channel(int(spl_data[2]))
            is_on = 6
            ch_name = 'channel'
            ch_name1 = 'каналі'
            own = 5
            linked = 8
            link = 3
            ch_name2 = 'чату'
            ch_name3 = 'Канал'

        keyboard = types.InlineKeyboardMarkup()

        if ch[is_on]:
            status = 'Ввімкнений'
        else:
            status = 'Ввимкнений'

        if ch[own] == call.from_user.id:
            if ch[is_on]:
                keyboard.add(types.InlineKeyboardButton(f'Вимкнути бота в {ch_name1}',
                                                        callback_data=f'{ch_name}_turn_off_{spl_data[2]}'))
            else:
                keyboard.add(types.InlineKeyboardButton(f'Ввімкнути бота в {ch_name1}',
                                                        callback_data=f'{ch_name}_turn_on_{spl_data[2]}'))

            keyboard.add(types.InlineKeyboardButton(f'Адміністратори', callback_data=f'{ch_name}_admins_{spl_data[2]}'))

            keyboard.add(types.InlineKeyboardButton(f"Прив'язка до {ch_name2}",
                                                    callback_data=f'{ch_name}_linking_{spl_data[2]}'))

            keyboard.add(types.InlineKeyboardButton(f'Керування посиланням та доступом до Простору Ячмінії',
                                                    callback_data=f'{ch_name}_prostir_{spl_data[2]}'))

            if check:
                keyboard.add(types.InlineKeyboardButton(f"▶️ Наступна сторінка",
                                                        callback_data=f'{call.data}_next'))
            else:
                keyboard.add(types.InlineKeyboardButton(f"Опублікувати пост з реакціями",
                                                        callback_data=f'channel_post_{spl_data[2]}'))
        else:
            if check:
                keyboard.add(
                    types.InlineKeyboardButton(f'Тригери репутації',
                                               callback_data='in_development')) # f'{ch_name}_reptrig_{spl_data[2]}'
                keyboard.add(
                    types.InlineKeyboardButton(f'Тригери повідомлень',
                                               callback_data=f'{ch_name}_messtrig_{spl_data[2]}'))
                keyboard.add(
                    types.InlineKeyboardButton(f'Привітальне повідомлення',
                                               callback_data=f'{ch_name}_welcmess_{spl_data[2]}'))
            else:
                keyboard.add(types.InlineKeyboardButton(f"Опублікувати пост з реакціями",
                                                        callback_data=f'channel_post_{spl_data[2]}'))

        if ch[linked]:
            linked = f"Прив'язаний до {ch_name2}"
        else:
            linked = f"Не прив'язаний до {ch_name2}"

        keyboard = menu_footer(keyboard, f'private_{spl_data[1]}s_0')
        bot.edit_message_text(f'{ch_name3} {ch[2]}\nСтатус: {status}\n{linked}', message_id=m.message_id,
                              chat_id=m.chat.id, reply_markup=keyboard)
        return

    if spl_data[0] == 'private' and spl_data[1] in ('chat', 'channel') and spl_data[3] == 'next':
        if spl_data[1] == 'chat':
            check = True
            ch = get_chat(int(spl_data[2]))
            is_on = 8
            ch_name = 'chat'
            ch_name1 = 'чаті'
            own = 7
            linked = 14
            link = 4
            ch_name2 = 'каналу'
            ch_name3 = 'Чат'
        else:
            check = False
            ch = get_channel(int(spl_data[2]))
            is_on = 6
            ch_name = 'channel'
            ch_name1 = 'каналі'
            own = 5
            linked = 8
            link = 3
            ch_name2 = 'чату'
            ch_name3 = 'Канал'
        keyboard = types.InlineKeyboardMarkup()
        if check:
            keyboard.add(
                types.InlineKeyboardButton(f'Тригери репутації',
                                           callback_data='in_development')) # f'{ch_name}_reptrig_{spl_data[2]}'
            keyboard.add(
                types.InlineKeyboardButton(f'Тригери повідомлень', callback_data=f'{ch_name}_messtrig_0_{spl_data[2]}'))
            keyboard.add(
                types.InlineKeyboardButton(f'Привітальне повідомлення',
                                           callback_data=f'{ch_name}_welcmess_{spl_data[2]}'))
            keyboard.add(types.InlineKeyboardButton(f"◀️ Попередня сторінка",
                                                    callback_data=f'{"_".join(spl_data[:-1])}'))

        if ch[is_on]:
            status = 'Ввімкнений'
        else:
            status = 'Ввимкнений'
        if ch[linked]:
            linked = f"Прив'язаний до {ch_name2}"
        else:
            linked = f"Не прив'язаний до {ch_name2}"
        keyboard = menu_footer(keyboard, 'private_chats_0')
        bot.edit_message_text(f'{ch_name3} {ch[2]}\nСтатус: {status}\n{linked}', m.chat.id, m.message_id,
                              reply_markup=keyboard)
        return

    if spl_data[0] in ('chat', 'channel') and spl_data[1] == 'turn' and spl_data[2] in ('on', 'off') and \
            len(spl_data) == 4:
        if spl_data[2] == 'on':
            keyboard = types.InlineKeyboardMarkup()
            passport = get_passport(u.id)
            day = datetime.today().weekday()
            pay = 5 * (7 - day)
            text = f'Для ввімкнення бота ви маєте сплатити {pay} {glas(pay)}' \
                   f' за цей тиждень (5 ячок за кожен день). Надалі ви сплачуватимете по 35 ячок на тиждень.\n' \
                   f'На вашому рахунку {passport[9]} {glas(passport[9])}.'
            keyboard.add(types.InlineKeyboardButton(text=f'Сплатити {pay} {glas(pay)}',
                                                    callback_data=f'{call.data}_done'))
            keyboard = menu_footer(keyboard, f'private_{spl_data[0]}_{spl_data[3]}')
            bot.edit_message_text(chat_id=m.chat.id, message_id=m.message_id, text=text,
                                  reply_markup=keyboard)
        else:
            keyboard = types.InlineKeyboardMarkup()
            day = datetime.today().weekday()
            pay = 5 * (7 - day)
            text = f'Ви точно хочете вимкнути бота? Ви втратите {pay} {glas(pay)}, які сплачені' \
                   f' за цей тиждень (5 ячок за кожен день).'
            keyboard.add(types.InlineKeyboardButton(text=f'Вимкнути бота',
                                                    callback_data=f'{call.data}_done'))
            keyboard = menu_footer(keyboard, f'private_{spl_data[0]}_{spl_data[3]}')
            bot.edit_message_text(chat_id=m.chat.id, message_id=m.message_id, text=text,
                                  reply_markup=keyboard)
        return

    if spl_data[0] in ('chat', 'channel') and spl_data[1] == 'turn' and spl_data[2] in ('on', 'off') and \
            spl_data[4] == 'done':
        if spl_data[0] == 'chat':
            ch = get_chat(int(spl_data[3]))
            is_on = 8
            linked = 14
            ch_f = insert_chat_a
            ch_name = 'чаті'
            ch_name1 = 'каналу'
        else:
            ch = get_channel(int(spl_data[3]))
            is_on = 6
            linked = 8
            ch_f = insert_channel_a
            ch_name = 'каналі'
            ch_name1 = 'чату'

        keyboard = types.InlineKeyboardMarkup()
        keyboard = menu_footer(keyboard, f'private_{spl_data[0]}_{spl_data[3]}', '⬅️ До чату')
        passport = get_passport(u.id)
        if spl_data[2] == 'on':
            if ch[linked]:
                keyboard.add(types.InlineKeyboardButton(text=f"Відв'язати {ch_name[-1]}",
                                                        callback_data=f'{spl_data[0]}_unlink_{spl_data[3]}'))
                keyboard = menu_footer(keyboard, f'private_{spl_data[0]}_{spl_data[3]}', '⬅️ До чату')
                text = f"Для вимкнення бота в {ch_name} треба його відв'язати від {ch_name1}. Зробити це можна за " \
                       f"кнопкою нижче"
                bot.edit_message_text(chat_id=m.chat.id, message_id=m.message_id, text=text,
                                      reply_markup=keyboard)
                return

            day = datetime.today().weekday()
            pay = 5 * (7 - day)
            if passport[9] < pay:
                text = 'На вашому рахунку недостатньо ячок.'
                bot.edit_message_text(chat_id=m.chat.id, message_id=m.message_id, text=text,
                                      reply_markup=keyboard)
                return
            passport[9] -= pay
            ch[is_on] = 1
            text = f'Бот тепер працює в {ch_name} {ch[2]}.'
            bot.edit_message_text(chat_id=m.chat.id, message_id=m.message_id, text=text,
                                  reply_markup=keyboard)
        else:
            ch[is_on] = 0
            text = f'Бот більше не працює в {ch_name} {ch[2]}.'
            bot.edit_message_text(chat_id=m.chat.id, message_id=m.message_id, text=text,
                                  reply_markup=keyboard)
        insert_passport_a(passport)
        ch_f(ch)
        return

    if spl_data[0] in ('chat', 'channel') and spl_data[1] == 'admins':
        if spl_data[0] == 'chat':
            ch = get_chat(int(spl_data[2]))
            link = 13
            ch_name = 'чату'
        else:
            ch = get_channel(int(spl_data[2]))
            link = 7
            ch_name = 'каналу'
        keyboard = types.InlineKeyboardMarkup()
        admins = ch[link].split()[2:]
        for i in admins:
            if int(i) == u.id:
                continue
            user_admin = get_user(int(i))
            keyboard.add(types.InlineKeyboardButton(text=user_admin[2],
                                                    callback_data=f'{spl_data[0]}_admin_{i}_{spl_data[2]}'))
        keyboard.add(types.InlineKeyboardButton(text='Додати адміністратора',
                                                callback_data=f'{spl_data[0]}_add_admin_{spl_data[2]}'))
        keyboard = menu_footer(keyboard, f'private_{spl_data[0]}_{spl_data[2]}')
        bot.edit_message_text(text=f'Список адміністраторів {ch_name} {ch[2]}', chat_id=m.chat.id,
                              message_id=m.message_id, reply_markup=keyboard)
        return

    if spl_data[0] in ('chat', 'channel') and spl_data[1] == 'admin':
        if spl_data[0] == 'chat':
            ch = get_chat(int(spl_data[3]))
            ch_name = 'чату'
        else:
            ch = get_channel(int(spl_data[3]))
            ch_name = 'каналу'
        keyboard = types.InlineKeyboardMarkup()
        user = get_user(int(spl_data[2]))
        passport = get_passport(int(spl_data[2]))
        if not passport:
            keyboard = menu_footer(keyboard, f'private_{spl_data[0]}_{spl_data[3]}', '⬅️ До чату')
            bot.edit_message_text(text='')
        keyboard.add(types.InlineKeyboardButton(text='Передати право власника (в боті)',
                                                callback_data=f'{spl_data[0]}_give_creator_{spl_data[2]}_{spl_data[3]}'))
        keyboard.add(types.InlineKeyboardButton(text='Вилучити адміністратора',
                                                callback_data=f'{spl_data[0]}_del_admin_{spl_data[2]}_{spl_data[3]}'))

        keyboard = menu_footer(keyboard, f'{spl_data[0]}_admins_{spl_data[3]}')
        bot.edit_message_text(text=f'Адміністратор {ch_name} {ch[2]}\n{user[2]}', chat_id=m.chat.id,
                              message_id=m.message_id, reply_markup=keyboard)
        return

    if spl_data[0] in ('chat', 'channel') and spl_data[1] == 'give' and spl_data[2] == 'creator':
        if spl_data[0] == 'chat':
            ch = get_chat(int(spl_data[4]))
            ch_name = 'чату'
            chl = get_channel(ch[14])
            ch_name1 = 'чат'
            ch_name2 = 'каналу'
        else:
            ch = get_channel(int(spl_data[4]))
            ch_name = 'каналу'
            chl = get_chat(ch[18])
            ch_name1 = 'канал'
            ch_name2 = 'чату'
        if chl:
            text_in = f'''\n\nУВАГА!\nТак як {ch_name1} "{ch[2]}" прив'язаний до {ch_name2} "{chl[2]}", ви передасте 
            право власника на канал і чат.'''
        else:
            text_in = ''
        user = get_user(int(spl_data[3]))
        keyboard = types.InlineKeyboardMarkup()
        keyboard.add(types.InlineKeyboardButton(text='Передати право власника',
                                                callback_data=f'{spl_data[0]}_give_'
                                                              f'creatordone_{spl_data[3]}_{spl_data[4]}'))
        keyboard = menu_footer(keyboard, f'{spl_data[0]}_admins_{spl_data[4]}')
        bot.edit_message_text(text=f'Ви точно хочете передати право власника {ch_name} акаунту {user[2]}? Це '
                                   f'незворотня дія.{text_in}',
                              chat_id=m.chat.id, message_id=m.message_id, reply_markup=keyboard)
        return

    if spl_data[0] in ('chat', 'channel') and spl_data[1] == 'give' and spl_data[2] == 'creatordone':
        if spl_data[0] == 'chat':
            ch = get_chat(int(spl_data[4]))
            chl = get_channel(ch[14])
            own = 7
            ownl = 5
            ch_f = insert_chat_a
            ch_name = 'чату'
            chl_f = insert_channel_a
            ch_name1 = 'чат'
            ch_name2 = 'каналу'
        else:
            ch = get_channel(int(spl_data[4]))
            chl = get_chat(ch[18])
            own = 5
            ownl = 7
            ch_f = insert_channel_a
            ch_name = 'каналу'
            chl_f = insert_chat_a
            ch_name1 = 'канал'
            ch_name2 = 'чату'
        ch[own] = int(spl_data[3])
        ch_f(ch)
        if chl:
            chl[ownl] = int(spl_data[3])
            chl_f(chl)
        keyboard = types.InlineKeyboardMarkup()
        keyboard = menu_footer(keyboard, f'private_{spl_data[0]}_{spl_data[4]}', f'⬅️ До {ch_name}')
        bot.edit_message_text(text=f'Права власника передані.', chat_id=m.chat.id, message_id=m.message_id,
                              reply_markup=keyboard)
        try:
            bot.send_message(int(spl_data[3]), f'Вам передали право власника {ch_name} "{ch[2]}"')
        except:
            pass
        return

    if spl_data[0] in ('chat', 'channel') and spl_data[1] == 'del' and spl_data[2] == 'admin':
        if spl_data[0] == 'chat':
            ch = get_chat(int(spl_data[4]))
            ch_f = insert_chat_a
            adm = 13
            ch_name = 'чату'
        else:
            ch = get_channel(int(spl_data[4]))
            ch_f = insert_channel_a
            adm = 7
            ch_name = 'каналу'
        adm_list = ch[adm].split()
        adm_list.remove(spl_data[3])
        ch[adm] = ' '.join(adm_list)
        ch_f(ch)
        keyboard = types.InlineKeyboardMarkup()
        keyboard = menu_footer(keyboard, f'private_{spl_data[0]}_{spl_data[4]}', f'⬅️ До {ch_name}')
        bot.edit_message_text(text=f'Адміністратор вилучений', chat_id=m.chat.id, message_id=m.message_id,
                              reply_markup=keyboard)
        try:
            bot.send_message(int(spl_data[3]), f'Вас вилучили з адміністраторів {ch_name} "{ch[2]}"')
        except:
            pass
        return

    if spl_data[0] in ('chat', 'channel') and spl_data[1] == 'add' and spl_data[2] == 'admin':
        if spl_data[0] == 'chat':
            ch = get_chat(int(spl_data[3]))
            link = 13
            ch_f = insert_chat_a
            ch_name = 'чату'
        else:
            ch = get_channel(int(spl_data[3]))
            link = 7
            ch_f = insert_channel_a
            ch_name = 'каналу'
        keyboard = types.InlineKeyboardMarkup()
        keyboard = menu_footer(keyboard, f'{spl_data[0]}_admins_{spl_data[3]}')
        bot.edit_message_text(text=f'Введіть id акаунта, яку ви хочете зробити адміністратором. '
                                     f'<a href="https://telegra.ph/YAk-d%D1%96znatis-id-akaunta-v-Telegram%D1%96-03-12">'
                                     f'Як дізнатись id акаунта в Телеграмі?</a>\n{stop_text}.',
                                     chat_id=call.message.chat.id, message_id=call.message.message_id,
                                     parse_mode='HTML')

        def add_adm(message):
            """ms = bot.forward_message(thrash, m.chat.id, m.message_id)
            if mess.text != ms.text:
                return
            bot.send_message(message.chat.id, 'лмао')"""
            if message.text == 'СТОП':
                bot.send_message(m.chat.id, 'Ви відмінили процедуру додавання адміністратора.', reply_markup=keyboard)
                return

            if not message.text.isdigit():
                bot.send_message(message.chat.id, 'Вказаний неправильний ідентифікатор акаунта.', reply_markup=keyboard)
                return

            user = get_user(int(message.text))

            if not user:
                bot.send_message(message.chat.id, 'Акаунт не зареєстрований у боті. Попросіть у особи, хай вона'
                                                  ' розпочне бесіду з ботом.', reply_markup=keyboard)
                return

            ch[link] = f'{ch[link]} {message.text}'
            ch_f(ch)

            try:
                bot.send_message(message.text, f'{user_link(message.from_user.id, html(name(message.from_user)))} '
                                               f'призначив вас адміністратором {ch_name} "{html(ch[2])}". '
                                               f'Тепер ви можете керувати ним через меню керування Простором Ячмінії.',
                                 parse_mode='HTML')
            except:
                pass

            bot.send_message(message.chat.id, f'{user_link(user[1], html(user[2]))} став '
                                              f'адміністратором {ch_name} "{html(ch[2])}"', parse_mode='HTML',
                             reply_markup=keyboard)

        register_next_step_handler(m, add_adm)
        return

    if spl_data[0] in ('chat', 'channel') and spl_data[1] == 'linking':
        if spl_data[0] == 'chat':
            ch = get_chat(int(spl_data[2]))
            link = 14
            ch_f = get_channel
            ch_name0 = 'Чат'
            ch_name1 = 'каналу'
        else:
            ch = get_channel(int(spl_data[2]))
            link = 8
            ch_f = get_chat
            ch_name0 = 'Канал'
            ch_name1 = 'чату'

        keyboard = types.InlineKeyboardMarkup()
        if ch[link]:
            ch_l = ch_f(ch[link])
            keyboard.add(types.InlineKeyboardButton(text="Відв'язати",
                                                    callback_data=f'{spl_data[0]}_unlink_{spl_data[2]}'))
            text = f'''{ch_name0} "{ch[2]}" прив'язаний до {ch_name1} "{ch_l[2]}".'''
        else:
            keyboard.add(types.InlineKeyboardButton(text="Прив'язати",
                                                    callback_data=f'{spl_data[0]}_link_{spl_data[2]}'))
            text = f'''{ch_name0} не прив'язаний до {ch_name1}.'''

        keyboard = menu_footer(keyboard, f'private_{spl_data[0]}_{spl_data[2]}')
        bot.edit_message_text(text=text, chat_id=m.chat.id, message_id=m.message_id, reply_markup=keyboard)
        return

    if spl_data[0] in ('chat', 'channel') and spl_data[1] == 'unlink':
        if spl_data[0] == 'chat':
            ch = get_chat(int(spl_data[2]))
            ch_l = get_channel(ch[14])
            ch_name0 = 'чат'
            ch_name1 = 'каналу'
        else:
            ch = get_channel(int(spl_data[2]))
            ch_l = get_chat(ch[8])
            ch_name0 = 'канал'
            ch_name1 = 'чату'

        keyboard = types.InlineKeyboardMarkup()
        keyboard.add(types.InlineKeyboardButton(text="Відв'язати",
                                                callback_data=f'{spl_data[0]}_unlinkdone_{spl_data[2]}'))
        text = f'''Ви точно хочете відв'язати {ch_name0} "{ch[2]}" від {ch_name1} "{ch_l[2]}"? 
        Ви втратите чимало переваг.'''
        keyboard = menu_footer(keyboard, f'{spl_data[0]}_linking_{spl_data[2]}')
        bot.edit_message_text(text=text, chat_id=m.chat.id, message_id=m.message_id, reply_markup=keyboard)
        return

    if spl_data[0] in ('chat', 'channel') and spl_data[1] == 'unlinkdone':
        if spl_data[0] == 'chat':
            chat = get_chat(int(spl_data[2]))
            channel = get_channel(chat[14])
            ch_name0 = 'чат'
            ch_name1 = 'каналу'
        else:
            channel = get_channel(int(spl_data[2]))
            chat = get_chat(channel[8])
            ch_name0 = 'канал'
            ch_name1 = 'чату'

        chat[14] = 0
        channel[8] = 0
        insert_chat_a(chat)
        insert_channel_a(channel)
        text = f'''Ви відв'язали {ch_name0} від {ch_name1}.'''
        keyboard = types.InlineKeyboardMarkup()
        keyboard = menu_footer(keyboard, f'private_{spl_data[0]}_{spl_data[2]}', '⬅️ До чату')
        bot.edit_message_text(text=text, chat_id=m.chat.id, message_id=m.message_id, reply_markup=keyboard)
        return

    if spl_data[0] in ('chat', 'channel') and spl_data[1] == 'link':
        if spl_data[0] == 'chat':
            ch = get_chat(int(spl_data[2]))
            chs = get_all_channels(u.id)
            ch_name0 = 'чату'
            ch_name1 = 'канал'
        else:
            ch = get_channel(int(spl_data[2]))
            chs = get_all_chats(u.id)
            ch_name0 = 'каналу'
            ch_name1 = 'чат'
        keyboard = types.InlineKeyboardMarkup()
        for i in chs:
            keyboard.add(types.InlineKeyboardButton(text=i[2],
                                                    callback_data=f'{spl_data[0]}_linkdone_{spl_data[2]}_{i[1]}'))
        keyboard = menu_footer(keyboard, f'{spl_data[0]}_linking_{spl_data[2]}')
        text = f'''Оберіть {ch_name1}, який ви хочете прив'язати до {ch_name0} "{ch[2]}".'''
        bot.edit_message_text(text=text, chat_id=m.chat.id, message_id=m.message_id, reply_markup=keyboard)
        return

    if spl_data[0] in ('chat', 'channel') and spl_data[1] == 'linkdone':
        if spl_data[0] == 'chat':
            chat = get_chat(int(spl_data[2]))
            channel = get_channel(int(spl_data[3]))
            ch_name0 = 'чат'
            ch_name1 = 'каналу'
        else:
            channel = get_channel(int(spl_data[2]))
            chat = get_chat(int(spl_data[3]))
            ch_name0 = 'канал'
            ch_name1 = 'чату'

        chat[14] = channel[1]
        channel[8] = chat[1]
        insert_chat_a(chat)
        insert_channel_a(channel)
        text = f'''Ви прив'язали {ch_name0} до {ch_name1}.'''
        keyboard = types.InlineKeyboardMarkup()
        keyboard = menu_footer(keyboard, f'private_{spl_data[0]}_{spl_data[2]}', '⬅️ До чату')
        bot.edit_message_text(text=text, chat_id=m.chat.id, message_id=m.message_id, reply_markup=keyboard)
        return

    if spl_data[0] in ('chat', 'channel') and spl_data[1] == 'prostir':
        if spl_data[0] == 'chat':
            ch = get_chat(int(spl_data[2]))
            link = 4
            ch_name0 = 'чат'
            ch_name1 = 'чату'
        else:
            ch = get_channel(int(spl_data[2]))
            link = 3
            ch_name0 = 'канал'
            ch_name1 = 'каналу'

        keyboard = types.InlineKeyboardMarkup()
        if ch[link] == 'NoneURL':
            text = f"Ви не вказали посилання до {ch_name1}. Вказавши його ви відкриєте {ch_name0} для Простору " \
                   f"Ячмінії."
            keyboard.add(types.InlineKeyboardButton(f'Відкрити {ch_name0} для Простору Ячмінії',
                                                    callback_data=f'{spl_data[0]}_open_{spl_data[2]}'))
        else:
            text = f"Посилання на {ch_name0} вказане:\n{ch[link]}\nЯкщо посилання неробоче, ви можете замінити " \
                   f"його натиснувши на кнопку нижче. Також ви можете відкликати посилання і закрити чат від " \
                   f"Простору Ячмінії"

            keyboard.add(types.InlineKeyboardButton(f'Редагувати посилання',
                                                    callback_data=f'{spl_data[0]}_edit_{spl_data[2]}'))
            keyboard.add(types.InlineKeyboardButton(f'Відкликати посилання і закрити {ch_name0} від Простору Ячмінії',
                                                    callback_data=f'{spl_data[0]}_close_{spl_data[2]}'))
        keyboard = menu_footer(keyboard, f'private_{spl_data[0]}_{spl_data[2]}')
        bot.edit_message_text(text=text, chat_id=m.chat.id, message_id=m.message_id, reply_markup=keyboard)
        return

    if spl_data[0] in ('chat', 'channel') and spl_data[1] in ('open', 'edit'):
        if spl_data[0] == 'chat':
            ch = get_chat(int(spl_data[2]))
            link = 4
            ch_name0 = 'чат'
            ch_name1 = 'чату'
            ch_in = insert_chat_a
        else:
            ch = get_channel(int(spl_data[2]))
            link = 3
            ch_name0 = 'канал'
            ch_name1 = 'каналу'
            ch_in = insert_channel_a
        keyboard = types.InlineKeyboardMarkup()
        keyboard = menu_footer(keyboard, f'{spl_data[0]}_prostir_{spl_data[2]}')
        if spl_data[1] == 'open':
            word0 = f'відкриття {ch_name1} для Простору Ячмінії'
            word1 = f'відкриття {ch_name1}'
            word2 = f'відкрили {ch_name0} для Простору Ячмінії'
        else:
            word0 = f'редагування посилання на {ch_name0}'
            word1 = f'редагування посилання'
            word2 = f'відредагували посилання на {ch_name0}'

        text = f'''Для {word0} надішліть посилання на нього. {stop_text}'''
        bot.edit_message_text(text=text, chat_id=m.chat.id, message_id=m.message_id, parse_mode='HTML')

        def get_link(message):
            if message.text == 'СТОП':
                bot.send_message(m.chat.id, f'Ви відмінили процедуру {word1}.', reply_markup=keyboard)
                return
            if re.fullmatch(r'(https://|)t\.me/(joinchat/|)\w*', message.text):
                ch[link] = message.text
                bot.send_message(m.chat.id, f'Ви успішно {word2}. '
                                            f'Якщо бот увімкнений та оплачений, то {ch_name0} буде видимий в '
                                            f'Просторі Ячмінії. Ви завжди можете закрити чат.', reply_markup=keyboard)
                ch_in(ch)
            else:
                bot.send_message(m.chat.id,
                                 f'Ви надіслали направильне посилання на {ch_name0}. Спробуйте ще раз. {stop_text}.',
                                 parse_mode='HTML')
                register_next_step_handler(m, get_link)
                return
        register_next_step_handler(m, get_link)
        return

    if spl_data[0] in ('chat', 'channel') and spl_data[1] == 'close':
        if spl_data[0] == 'chat':
            ch = get_chat(int(spl_data[2]))
            link = 4
            ch_name0 = 'чат'
            ch_in = insert_chat_a
        else:
            ch = get_channel(int(spl_data[2]))
            link = 3
            ch_name0 = 'канал'
            ch_in = insert_channel_a
        ch[link] = 'NoneURL'
        ch_in(ch)
        keyboard = types.InlineKeyboardMarkup()
        keyboard = menu_footer(keyboard, f'{spl_data[0]}_prostir_{spl_data[2]}')
        text = f'''Ви успішно відкликали посилання на {ch_name0}.'''
        bot.edit_message_text(text=text, chat_id=m.chat.id, message_id=m.message_id, reply_markup=keyboard)
        return

    if spl_data[0] in ('chat', 'channel') and spl_data[1] == 'reptrig':
        if spl_data[0] == 'chat':
            ch = get_chat(int(spl_data[2]))
            link = 4
            ch_name0 = 'чат'
            ch_in = insert_chat_a
        else:
            ch = get_channel(int(spl_data[2]))
            link = 3
            ch_name0 = 'канал'
            ch_in = insert_channel_a

        return

    if spl_data[0] == 'chat' and spl_data[1] == 'messtrig':
        chat = get_chat(int(spl_data[3]))
        keyboard = types.InlineKeyboardMarkup()
        if chat[11] == 'None':
            msg_text = 'Наразі у вашому чаті нема жодного тригеру повідомлення, проте ви можете ' \
                   'додати його натиснувши на кнопку нижче.'
            keyboard.add(types.InlineKeyboardButton('🆕 Додати тригер', callback_data=f'chat_addmesstrig_{spl_data[3]}'))
        else:
            triggers = chat[11].split('#*%|%*#')

            buttons = []
            for i in range(len(triggers)):
                but = types.InlineKeyboardButton(triggers[i], callback_data=f'chat_trigger_{i}_{spl_data[3]}')
                buttons.append(but)
            n = int(spl_data[2])
            ln = 5 + n * 5
            more = True
            if len(buttons) <= ln:
                more = False
                ln = len(buttons)

            for i in range(n * 5, ln):
                keyboard.keyboard.append([buttons[i]])
            keyboard.add(types.InlineKeyboardButton('🆕 Додати тригер', callback_data=f'chat_addmesstrig_{spl_data[3]}'))
            if n:
                but0 = types.InlineKeyboardButton('◀️', callback_data=f'chat_messtrig_{n-1}_{spl_data[3]}')
            else:
                but0 = types.InlineKeyboardButton('⏺', callback_data=f'empty')
            if more:
                but1 = types.InlineKeyboardButton('▶️', callback_data=f'chat_messtrig_{n+1}_{spl_data[3]}')
            else:
                but1 = types.InlineKeyboardButton('⏺', callback_data=f'empty')
            keyboard.keyboard.append([but0, but1])

            msg_text = f'Список тригерів повідомлень вашого чату. [{1 + n * 5}-{ln}]'

        keyboard = menu_footer(keyboard, f"private_chat_{spl_data[3]}_next")
        bot.edit_message_text(msg_text, m.chat.id, m.message_id, reply_markup=keyboard, parse_mode='HTML')
        return

    if spl_data[0] == 'chat' and spl_data[1] == 'trigger':
        chat = get_chat(int(spl_data[3]))
        keyboard = types.InlineKeyboardMarkup()
        trigger = chat[11].split('#*%|%*#')[int(spl_data[2])]
        text = chat[12].split('#*%|%*#')[int(spl_data[2])]
        msg_text = f'Тригер\n{html(trigger)}\n\nТекст:\n{text}\n\nДля редагування тригера видаліть його і додайте новий.'
        keyboard.add(types.InlineKeyboardButton(text='Видалити тригер',
                                                callback_data=f'chat_trigger_delete_{spl_data[2]}_{spl_data[3]}'))
        keyboard = menu_footer(keyboard, f'chat_messtrig_0_{spl_data[3]}')
        bot.edit_message_text(chat_id=m.chat.id, message_id=m.message_id, text=msg_text, parse_mode='HTML',
                              reply_markup=keyboard)
        return

    if spl_data[0] == 'chat' and spl_data[1] == 'addmesstrig':
        chat = get_chat(int(spl_data[2]))

        keyboard = types.InlineKeyboardMarkup()
        keyboard = menu_footer(keyboard, f'chat_messtrig_0_{spl_data[2]}')

        def get_trig_name(m0):
            if m0.text == 'СТОП':
                bot.send_message(m.chat.id, f'Ви відмінили процедуру додавання тригера.', reply_markup=keyboard)
                return
            if len(m0.text) > 200:
                bot.send_message(m.chat.id, f'Ви відмінили процедуру додавання тригера.', reply_markup=keyboard)
                register_next_step_handler(m0, get_trig_name)
                return

            def get_trig_text(m1):
                if m1.text == 'СТОП':
                    bot.send_message(m.chat.id, f'Ви відмінили процедуру додавання тригера.', reply_markup=keyboard)
                    return
                if len(m0.text) > 200:
                    bot.send_message(m.chat.id, f'Ви відмінили процедуру додавання тригера.', reply_markup=keyboard)
                    register_next_step_handler(m0, get_trig_name)
                    return

                try:
                    bot.send_message(thrash, m1.text, parse_mode='HTML')
                except:
                    bot.send_message(m.chat.id, f'давай по новой міша, всьо хуйня ', reply_markup=keyboard)
                    return

                chat[11] = m0.text if chat[11] == 'None' else f'{chat[11]}#*%|%*#{m0.text}'
                chat[12] = m1.text if chat[12] == 'None' else f'{chat[12]}#*%|%*#{m1.text}'

                insert_chat_a(chat)
                bot.send_message(text='Тригер збережено', chat_id=m.chat.id, reply_markup=keyboard)
            bot.send_message(text='Надішліть текст, який буде реакцією бота на тригер.',
                                  chat_id=m.chat.id)
            register_next_step_handler(m0, get_trig_text)

        bot.edit_message_text(text='Надішліть тригер, на який реагуватиме бот.', message_id=m.message_id,
                              chat_id=m.chat.id)
        register_next_step_handler(m, get_trig_name)
        return

    if spl_data[0] == 'chat' and spl_data[1] == 'welcmess':
        chat = get_chat(int(spl_data[2]))
        keyboard = types.InlineKeyboardMarkup()
        if chat[3] == 'None':
            msg_text = 'Наразі у вашому чаті відсутнє привітальне повідомлення, проте ви можете ' \
                   'додати його натиснувши на кнопку нижче.'
            keyboard.add(types.InlineKeyboardButton('🆕 Додати привітальне повідомлення',
                                                    callback_data=f'chat_addwelcmess_{spl_data[2]}'))
        else:
            msg_text = f'Привітальне повідомлення:\n\n{chat[3]}'

            keyboard.add(types.InlineKeyboardButton('Редагувати привітальне повідомлення',
                                                    callback_data=f'chat_editwelcmess_{spl_data[2]}'))
            keyboard.add(types.InlineKeyboardButton('Вилучити привітальне повідомлення',
                                                    callback_data=f'chat_delwelcmess_{spl_data[2]}'))

        keyboard = menu_footer(keyboard, f'private_chat_{spl_data[2]}_next')
        bot.edit_message_text(msg_text, chat_id=m.chat.id, message_id=m.message_id, parse_mode='HTML',
                              reply_markup=keyboard)
        return

    if spl_data[0] == 'chat' and spl_data[1] in ('addwelcmess', 'editwelcmess'):
        chat = get_chat(int(spl_data[2]))

        keyboard = types.InlineKeyboardMarkup()
        keyboard = menu_footer(keyboard, f'private_chat_{spl_data[2]}_next')

        def get_welc(m0):
            if m0.text == 'СТОП':
                bot.send_message(m.chat.id, f'Ви відмінили процедуру додавання привітального повідомлення.',
                                 reply_markup=keyboard)
                return
            if len(m0.text) > 2000:
                bot.send_message(m.chat.id, f'Більше 2000 символів.', reply_markup=keyboard)
                register_next_step_handler(m0, get_trig_name)
                return
            try:
                bot.send_message(thrash, m0.text, parse_mode='HTML')
            except:
                bot.send_message(m.chat.id, f'давай по новой міша, всьо хуйня ', reply_markup=keyboard)
                return

            chat[3] = m0.text
            insert_chat_a(chat)
            bot.send_message(text='Привітальне повідомлення збережено', chat_id=m.chat.id, reply_markup=keyboard)

        bot.edit_message_text(text='Надішліть тригер, на який реагуватиме бот.', message_id=m.message_id,
                              chat_id=m.chat.id)
        register_next_step_handler(m, get_welc)
        return

    if spl_data[0] == 'chat' and spl_data[1] == 'delwelcmess':
        chat = get_chat(int(spl_data[2]))

        keyboard = types.InlineKeyboardMarkup()
        keyboard = menu_footer(keyboard, f'private_chat_{spl_data[2]}_next')

        chat[3] = 'None'
        insert_chat_a(chat)
        bot.edit_message_text(text='Привітальне повідомлення вилучено.', message_id=m.message_id,
                              chat_id=m.chat.id, reply_markup=keyboard)
        return

    if spl_data[0] == 'channel' and spl_data[1] == 'post':
        channel = get_channel(int(spl_data[2]))

        def get_post_message(m0):

            def get_react(m1):
                try:
                    m_id = bot.copy_message(channel[1], m0.chat.id, m0.message_id).message_id
                except:
                    keyboard = menu_footer(types.InlineKeyboardMarkup(), f'private_channel_{spl_data[2]}')
                    bot.send_message(m.chat.id, 'Виникла помилка', reply_markup=keyboard)
                    return

                spl_text = m1.text.split('\n')
                reacts = []
                votes = []
                for i in range(len(spl_text)):
                    reacts.append([])
                    votes.append([])
                    for j in spl_text[i].split('|'):
                        reacts[i].append(str(j))
                        votes[i].append([])
                new_post(channel[1], m_id, str(reacts), str(votes))

                keyboard = menu_footer(types.InlineKeyboardMarkup(), f'private_channel_{spl_data[2]}')
                bot.send_message(m.chat.id, 'Готово', reply_markup=keyboard)

            bot.send_message(text='Надішліть реакції.', chat_id=m.chat.id)
            register_next_step_handler(m0, get_react)

        bot.edit_message_text('Надішліть пост.', chat_id=m.chat.id, message_id=m.message_id)
        register_next_step_handler(m, get_post_message, True)
        return

    if spl_data[0] == 'react':
        x = int(spl_data[1])
        y = int(spl_data[2])
        channel = get_channel(m.chat.id)
        if not channel:
            return
        keyboard = m.reply_markup
        post = get_post(m.chat.id, m.message_id)
        post[4] = eval(post[4])
        voted = False
        l_x, l_y = None, None
        for i in range(len(post[4])):
            for j in range(len(post[4][i])):
                if u.id in post[4][i][j]:
                    voted = True
                    l_x = i
                    l_y = j
        if voted:
            button = keyboard.keyboard[l_x][l_y]
            react = ' '.join(button.text.split()[:-1])
            num = int(button.text.split()[-1])
            keyboard.keyboard[l_x][l_y] = types.InlineKeyboardButton(f'{react} {num-1}',
                                                                     callback_data=f'react_{l_x}_{l_y}')
            post[4][l_x][l_y].remove(u.id)
            text = f'Ви забрали свою реакцію з "{react}"'
            if x != l_x or y != l_y:
                button = keyboard.keyboard[x][y]
                react = ' '.join(button.text.split()[:-1])
                num = int(button.text.split()[-1])
                keyboard.keyboard[x][y] = types.InlineKeyboardButton(f'{react} {num + 1}',
                                                                    callback_data=f'react_{x}_{y}')
                post[4][x][y].append(u.id)
                text = f'Ви змінили свою реакцію на "{react}"'
        else:
            button = keyboard.keyboard[x][y]
            react = ' '.join(button.text.split()[:-1])
            num = int(button.text.split()[-1])
            keyboard.keyboard[x][y] = types.InlineKeyboardButton(f'{react} {num + 1}',
                                                                 callback_data=f'react_{x}_{y}')
            post[4][x][y].append(u.id)
            text = f'Ви відреагували "{react}"'
        bot.edit_message_reply_markup(m.chat.id, m.message_id, reply_markup=keyboard)
        bot.answer_callback_query(call.id, text=text)
        post[3] = str(post[3])
        post[4] = str(post[4])
        insert_post_a(post)
        return


@bot.message_handler(func=lambda m: m.chat.id == -1001452719524, content_types=['new_chat_members'])
def new_chat_member_gr(m):
    global welcome_m, pass_form_call

    for i in m.new_chat_members:
        if i.is_bot():
            continue
        user = get_user(i.id)
        if user is None:
            non_reg(i, m)
            try:
                bot.restrict_chat_member(chat_id=m.chat.id, user_id=i.id)
            except:
                pass
            continue
    keyboard = types.InlineKeyboardMarkup()
    callback_button = types.InlineKeyboardButton(text="🖋 Заповнити форму на паспорт", callback_data="pass")
    keyboard.add(callback_button)
    chat = m.chat
    welc = chat[3]
    welc_l = welc.split('{enter}')
    welc_out = ''
    for i in range(len(welc_l)):
        welc_out += f'{welc_l[i]}\n'
    welc_out = welc_out.replace('{empty}', f'{chr(8205)}')
    welc_out = welc_out.replace('{name}', f'{name(m.from_user)}')

    pass_form_call = m.from_user.id
    bot.send_message(m.chat.id, welc_out, parse_mode='HTML', reply_markup=keyboard, reply_to_message_id=m.message_id)


@bot.message_handler(content_types=['new_chat_members'])
def new_chat_members(m):
    chat = get_chat(m.chat.id)
    """if m.new_chat_members[0].id == BOT_USER:
        if get_chat(m.chat.id) is not None:
            return
        out = f'{chat.title}\n'
        out += f'{chat.id}\n'
        if chat.username is not None:
            out += f'{chat.username}\n\n'
        if chat.description is not None:
            out += f'{chat.description}'
        # bot.send_message(-1001476087749, f'{out}')

        if m.from_user.id != CREATOR:
            bot.send_message(chat.id, f'{out}\n\nФлешка з цими матеріалами вже в Гаазі')
            bot.send_message(chat.id, 'буенос діас, педрілас!')
            bot.leave_chat(chat.id)
            return

        new_chat(chat)
        return"""

    for i in m.new_chat_members:
        if i.id == BOT_USER:
            out = f'{m.chat.title}\n'
            out += f'{m.chat.id}\n'
            if m.chat.username is not None:
                out += f'{m.chat.username}\n\n'
            if m.chat.description is not None:
                out += f'{m.chat.description}'
            # bot.send_message(-1001476087749, f'{out}')

            if chat:
                continue
            if m.chat.type != 'supergroup':
                bot.send_message(m.chat.id, f'Для коректної роботи бота група має бути супергрупою. Відкрийте '
                                            f'історію чату, і група автоматично стане такою. Після цього додайте '
                                            f'бота знову')
                bot.leave_chat(m.chat.id)
                return
            admins = [0, 0]
            cr = 0
            for j in bot.get_chat_administrators(m.chat.id):
                user = j.user
                if j.status == 'creator':
                    cr = user.id
                else:
                    if not get_user(user.id):
                        continue
                admins.append(user.id)
            admins = list(map(lambda x: str(x), admins))
            if cr:
                new_chat(m.chat, 'Приватний', cr, admins)
                keyboard = types.InlineKeyboardMarkup()
                but = types.InlineKeyboardButton(text='До меню Простору Ячмінії',
                                                 url='t.me/yachminiya_test_bot?start=prostir_menu')
                keyboard.add(but)
                bot.send_message(m.chat.id, f'Чат {m.chat.title} доданий до приватного Простору Ячмінії. '
                                            f'Для коректної роботи бота власник чату має ввімкнути бота в меню'
                                            f'Простору Ячмінії. Якщо виникли проблеми з доступом до власника, '
                                            f'зверніться до {user_link(CREATOR, "Назарія фон Герсте")}.',
                                 reply_markup=keyboard, parse_mode='HTML')
                return
            else:
                bot.send_message(m.chat.id, f'Власник чату не може бути анонімним. Для додавання чату змініть права'
                                            f' власника. Бот зараз лівне.')
                bot.leave_chat(m.chat.id)
                return

        if chat[6] in ('Основний', 'Службовий'):
            user = get_user(i.id)
            if user is None:
                try:
                    bot.restrict_chat_member(chat_id=m.chat.id, user_id=i.id)
                except:
                    pass
                keyboard = types.InlineKeyboardMarkup()
                button = types.InlineKeyboardButton(text='🤖 Пройти авторизацію', url='t.me/yachminiya_bot')
                keyboard.add(button)
                bot.send_message(m.chat.id,
                                 f'<a href="tg://user?id={i.id}">{name(i)}</a>, вітаємо! Ти потрапив(ла) до Простору '
                                 f'Ячмінії, але для отримання права спілкування тобі треба пройти авторизацію за '
                                 f'кнопкою знизу',
                                 parse_mode='HTML', reply_markup=keyboard)
                continue
        if chat[8]:
            welc = chat[3]
            if welc == 'None':
                return
            welc_out = welc.replace('/enter/', '\n')
            welc_out = welc_out.replace('/empty/', f'{chr(8205)}')
            welc_out = welc_out.replace('/name/', f'{name(i.user)}')
            bot.send_message(m.chat.id, welc_out, parse_mode='HTML', reply_to_message_id=m.message_id)
        return


@bot.message_handler(content_types=["text"])
def commands(m):
    global aktyv, lakt, zhandarm, CREATOR, voting_q, del_pass, weekdays, global_user, t, false_day
    tt = time.time()
    mess = m.text.split()

    chat = get_chat(m.chat.id)
    if m.chat.type != 'private':
        if not chat:
            bot.leave_chat(m.chat.id)
            return
        if m.text == '!чат':
            bot.send_message(m.chat.id, 'чат')
            return
        if not chat[8]:
            return

    if m.from_user.id == 777000:
        if not chat[14]:
            return
        channel_id = m.forward_from_chat.id
        m_id = m.forward_from_message_id
        chat_id = str(m.chat.id)[4:]
        post = get_post(channel_id, m_id)
        if not post:
            return
        keyboard = types.InlineKeyboardMarkup()
        if post[3] == 'None':
            return
        else:
            react = eval(post[3])
            """react_spl = post[3].split('\n')
            for i in range(len(react_spl)):
                react.append([])
                for j in react_spl[i].split('|'):
                    react[i].append(j)"""
            for i in range(len(react)):
                keyboard.keyboard.append([])
                for j in range(len(react[i])):
                    keyboard.keyboard[i].append(types.InlineKeyboardButton(f'{react[i][j]} 0',
                                                                           callback_data=f'react_{i}_{j}'))
        but = types.InlineKeyboardButton(text='💬 Коментарі', url=f'https://t.me/c/{chat_id}/1?thread={m.message_id}')
        keyboard.add(but)
        bot.edit_message_reply_markup(channel_id, m_id, reply_markup=keyboard)

    if m.reply_to_message:
        """
        if m.reply_to_message.from_user.id == 777000:
            text_of_but = m.reply_to_message.reply_markup.keyboard[-1][-1].text
            num = int(text_of_but.split()[1])
            channel_id = m.reply_to_message.forward_from_chat.id
            m_id = m.reply_to_message.forward_from_message_id
            chat_id = str(m.chat.id)[4:]
            but = types.InlineKeyboardButton(text=f'💬 {num+1}', url=f'https://t.me/c/{chat_id}/1?thread={m.message_id}')
            keyboard = types.InlineKeyboardMarkup()
            keyboard.add(but)
            bot.edit_message_reply_markup(channel_id, m_id, reply_markup=keyboard)"""
        # pprint(m.json)
        pass

    man = get_user(m.from_user.id)
    man_pass = get_passport(m.from_user.id)
    if man is not None:
        changed = False
        if man[2] != name(m.from_user):
            man[2] = name(m.from_user)
            changed = True
        if man[5] != m.from_user.username:
            man[5] = m.from_user.username
            changed = True
        if changed:
            insert_user_a(man)
    if man_pass is not None:
        changed = False
        if man_pass[4] != name(m.from_user):
            man_pass[4] = name(m.from_user)
            changed = True
        if man_pass[5] != m.from_user.username:
            man_pass[5] = m.from_user.username
            changed = True
        if changed:
            insert_passport_a(man_pass)

    if m.forward_sender_name or m.forward_from or m.forward_from_chat or m.forward_from_message_id:
        return

    try:
        aktyv[m.from_user.id][0] = aktyv[m.from_user.id][0] + 1
        aktyv[m.from_user.id][1] = aktyv[m.from_user.id][1] + len(m.text.split())
        lakt += 1
        if lakt > 14:
            aktyv_r()
    except:
        aktyv[m.from_user.id] = [1, len(m.text.split())]
        lakt += 1
        if lakt > 14:
            aktyv_r()

    if m.text[0] == '!':
        if f_queue(m):
            return

    if chat[11] != 'None' and m.chat.type == 'supergroup':
        triggers = chat[11].split('#*%|%*#')
        if m.text in triggers:
            tr_text = chat[12].split('#*%|%*#')[triggers.index(m.text)]
            bot.send_message(m.chat.id, tr_text, parse_mode='HTML')
            return

    """if m.chat.type == 'private':
        msg = bot.forward_message(-1001344984878, m.chat.id, m.message_id)
        bot.reply_to(msg, f'{m.chat.id} {m.message_id}')

    if m.chat.id == -1001344984878:
        if m.reply_to_message is not None:
            mess_r = m.reply_to_message
            c_id = int(mess_r.text.split()[0])
            m_id = int(mess_r.text.split()[1])
            try:
                if mess()[0] == 'р':
                    bot.send_message(chat_id=c_id, text=' '.join(m.text.split()[1:]), reply_to_message_id=m_id)
                else:
                    bot.send_message(chat_id=c_id, text=' '.join(m.text.split()))
            except:
                pass

    if m.chat.id == -1001404271371:
        bot.forward_message(-1001492661297, m.chat.id, m.message_id)"""

    if m.text == '!оновити_бд':
        if m.from_user.id != CREATOR:
            return
        update_all_db()
        bot.send_message(m.chat.id, 'good')

    if mess[0] == '!п' or m.text == '!me' or m.text == '!pass':
        if len(mess) > 1:
            if mess[1][-1] == 'с' or mess[1][-1] == 'c':
                if mess[1][:-1].isdigit():
                    t = int(mess[1][:-1])
                else:
                    bot.send_message(m.chat.id, 'Неправильний формат даних')
                    return
                rig = False
                id = m.from_user.id
                if t > 3600:
                    t = 3600
            else:
                rig = True
                id = mess[1]
        elif m.reply_to_message:
            id = m.reply_to_message.from_user.id
            rig = True
        else:
            id = m.from_user.id
            rig = False
            t = 60

        if rig:
            passport = get_user(m.from_user.id)
            if passport is None:
                non_reg(m.from_user, m)
                return
            if not int(passport[6].split()[1]):
                bot.send_message(m.from_user.id, 'Ви не маєте права на перегляд чужого паспорта.')
                return
            try:
                bot.send_message(m.from_user.id, get_str_passport(id), parse_mode='HTML')
                bot.send_message(m.chat.id, 'Перегляньте <a href="t.me/yachminiya_bot">чат з Системою</a>.',
                                 parse_mode='HTML', disable_web_page_preview=True)
            except:
                bot.send_message(m.chat.id,
                                 'Відновіть <a href="t.me/yachminiya_bot">чат з Системою</a> для перегляду документу.',
                                 parse_mode='HTML', disable_web_page_preview=True)
        else:
            n = bot.send_message(m.chat.id, get_str_passport(id), parse_mode='HTML').message_id
            Timer(t, del_doc, args=(m.chat.id, n)).start()
        if m.chat.id == -1001329014820:
            bot.send_message(m.chat.id, time.time() - tt)

    if m.text.lower() in reputation or m.text.lower() in bad_reputation:
        if m.chat.type == 'private':
            return
        if m.reply_to_message is None:
            return
        elif m.reply_to_message.from_user.id == m.from_user.id:
            bot.reply_to(m, 'Не можна змінювати репутацію собі')
            return

        if m.text.lower() in reputation:
            l = 1
            word = 'підвищує'
            cooldown = 60
        else:
            l = -1
            word = 'занижує'
            cooldown = 90

        u_g_id = m.from_user.id
        u_t_id = m.reply_to_message.from_user.id
        u_g = get_user(u_g_id)
        if u_g is None:
            non_reg(m.from_user, m)
            return

        u_t = get_user(u_t_id)
        if u_g is None:
            non_reg(m.reply_to_message.from_user, m)
            return

        if int(u_g[4]) < int(time.time() // 1):
            u_g[4] = int(time.time() // 1) + cooldown
            u_t[3] = int(u_t[3]) + l

            msg = f'{u_g[2]}[{u_g[3]}] {word} репутацію {u_t[2]}[{u_t[3]}]'
            bot.send_message(m.chat.id, msg, parse_mode='HTML')
            insert_user_a(u_g)
            insert_user_a(u_t)
            return
        else:
            time_to_sfdfsdfsfdsdf = int((float(u_g[4]) - time.time()) // 1) + 2
            last_nums = int(time_to_sfdfsdfsfdsdf) % 100
            last_num = int(time_to_sfdfsdfsfdsdf) % 10
            if 10 < last_nums < 20:
                glas_s = 'секунд'
            elif int(last_num) % 10 in (2, 3, 4):
                glas_s = 'секунди'
            elif int(last_num) % 10 in (5, 6, 7, 8, 9, 0):
                glas_s = 'секунд'
            else:
                glas_s = 'секунду'
            bot.send_message(m.chat.id, f'Зачекайте ще {time_to_sfdfsdfsfdsdf} {glas_s}')
            return

    if mess[0] == '!тест':
        '''global_user = m.from_user
        t = Timer(int(mess[1]), timeout, args=(m.from_user, m))
        t.start()'''
        """if len(mess) < 2:
            bot.send_message(m.chat.id, 'йди нахуй')
            return"""
        """for i in range(int(mess[1])):
            test_new_timer_pre(bot, m)"""
        """try:
            message = bot.send_message(mess[1], 'test', disable_notification=True)
            bot.delete_message(mess[1], message.message_id)
        except Exception as e:
            print(e)"""
        # print(bot.get_chat_administrators(m.chat.id))
        url = m.reply_to_message.entities[0].url
        p_id = url.split('/')[-2].split('.')[1]
        # bot.send_message(m.chat.id, get_str_passport(int(p_id)))
        if simplify(get_str_passport(int(p_id))) == m.reply_to_message.text:
            bot.send_message(m.chat.id, 'Дані документа актуальні')
        else:
            bot.send_message(m.chat.id, 'Дані документа не актуальні')

    if mess[0] == '!рандом_актив':
        if m.from_user.id != CREATOR:
            return
        passports = get_all_passports()
        for i in passports:
            i[23] = ' '.join([str(random.randint(0, 150 - i[0])) for _ in range(31)])
            i[24] = ' '.join([str(random.randint(0, 500 - i[0])) for _ in range(31)])
            insert_passport_l(i)
        insert_all_passports_g(passports)

    if mess[0] == '!очистити_актив':
        if m.from_user.id != CREATOR:
            return
        passports = get_all_passports()
        for i in passports:
            i[23] = ' '.join(['0' for _ in range(31)])
            i[24] = ' '.join(['0' for _ in range(31)])
            insert_passport_l(i)
        insert_all_passports_g(passports)

    if mess[0] == '!день':
        try:
            false_day = int(mess[1])
            bot.send_message(m.chat.id, f'день змінено на {false_day}')
        except:
            bot.send_message(m.chat.id, 'пішов нахуй')

    if mess[0] == '!топ' or mess[0] == '!кращий_топ':
        if mess[0] == '!топ':
            top = True
        else:
            top = False
        if len(m.text.split()) > 1:
            try:
                am_n = int(m.text.split()[1])
            except:
                bot.reply_to(m, 'Неправильний формат.')
                return
        else:
            am_n = 10

        users = get_all_users_rep_order()
        amount = len(users)

        """for i in range(amount):
            for j in range(i, amount):
                if top:
                    if int(users[i][3]) < int(users[j][3]):
                        users[i], users[j] = users[j], users[i]
                else:
                    if int(users[i][3]) > int(users[j][3]):
                        users[i], users[j] = users[j], users[i]"""

        if am_n > 30:
            am_n = 30
        elif am_n > amount:
            am_n = amount
        if top:
            msg_out = f'Найкраща репутація\n'
            users.reverse()
        else:
            msg_out = f'Дійсно найкраща репутація\n'

        for i in range(am_n):
            if int(users[i][3]) != 0:
                msg_out += f'{users[i][3]} <a href="t.me/{users[i][5]}">{html(users[i][2])}</a>\n'
        bot.send_message(m.chat.id, msg_out, parse_mode='HTML', disable_web_page_preview=True)
        if m.chat.id == -1001329014820:
            bot.send_message(m.chat.id, time.time() - tt)
        return

    if m.text.split()[0] == '!кращий_топ':
        if len(m.text.split()) > 1:
            try:
                am_n = int(m.text.split()[1])
            except:
                bot.reply_to(m, 'Неправильний формат.')
                return
        else:
            am_n = 10

        users = get_all_users()
        amount = len(users)

        for i in range(amount):
            for j in range(i, amount):
                if int(users[i][3]) > int(users[j][3]):
                    users[i], users[j] = users[j], users[i]

        if am_n > 30:
            am_n = 30
        elif am_n > amount:
            am_n = amount
        msg_out = f'Дійсно найкраща репутація\n'

        for i in range(am_n):
            msg_out += f'{users[i][3]} <a href="t.me/{users[i][5]}">{html(users[i][2])}</a>\n'
        bot.send_message(m.chat.id, msg_out, parse_mode='HTML', disable_web_page_preview=True)
        return

    if mess[0] == '!рахунок':
        if len(mess) > 1:
            if mess[1][-1] == 'с' or mess[1][-1] == 'c':
                if mess[1][:-1].isdigit():
                    t = int(mess[1][:-1])
                else:
                    bot.send_message(m.chat.id, 'Неправильний формат даних')
                    return
                rig = False
                id = m.from_user.id
                if t > 3600:
                    t = 3600
            else:
                rig = True
                id = mess[1]
        elif m.reply_to_message:
            id = m.reply_to_message.from_user.id
            rig = True
        else:
            id = m.from_user.id
            rig = False
            t = 60

        if rig:
            passport = get_user(m.from_user.id)
            if passport is None:
                non_reg(m.from_user, m)
                return
            if not int(passport[6].split()[1]):
                bot.send_message(m.from_user.id, 'Ви не маєте права на перегляд чужого паспорта.')
                return
            try:
                bot.send_message(m.from_user.id, get_str_passport(id), parse_mode='HTML')
                bot.send_message(m.chat.id, 'Перегляньте <a href="t.me/yachminiya_bot">чат з Системою</a>.',
                                 parse_mode='HTML', disable_web_page_preview=True)
            except:
                bot.send_message(m.chat.id,
                                 'Відновіть <a href="t.me/yachminiya_bot">чат з Системою</a> для перегляду документу.',
                                 parse_mode='HTML', disable_web_page_preview=True)
        else:
            n = bot.send_message(m.chat.id, get_str_acc(id), parse_mode='HTML').message_id
            Timer(t, del_doc, args=(m.chat.id, n)).start()

    if mess[0] == '!активи':
        if len(mess) != 2:
            bot.send_message(m.chat.id, 'Неправильний формат даних')
            return
        us_id = mess[1]
        bot.send_message(m.chat.id, get_str_aktives(us_id), parse_mode='HTML', disable_web_page_preview=True)

    if mess[0] == '!перевести':
        acc_g = get_passport(m.from_user.id)
        if acc_g is None:
            bot.send_message(m.chat.id, f'Ви не маєте громадянства Ячмінії.')

        if m.reply_to_message is None:
            if len(mess) < 3:
                bot.send_message(m.chat.id, 'Неправильний формат вхідних даних.')
                return
            try:
                amount_m = int(mess[2])
            except:
                bot.send_message(m.chat.id, 'Введено хибну кількість ячок.')
                return
            if amount_m < 1:
                bot.send_message(m.chat.id, 'Вкажіть додатню кількість ячок для переказу.')

            acc_t = get_passport(mess[1])
            pp_bus = 0
            if acc_t is None:
                acc_t = get_business(mess[1])
                pp_bus = 1
                if acc_t is None:
                    bot.send_message(m.chat.id, 'Введено хибний ідентифікатор отримувача.')
                    return

            if len(mess) > 3:
                description = ' '.join(m.text.split()[3:])
            else:
                description = None
        else:
            if len(mess) < 2:
                bot.send_message(m.chat.id, 'Неправильний формат вхідних даних.')
                return
            try:
                amount_m = int(mess[1])
            except:
                bot.send_message(m.chat.id, 'Введено хибну кількість ячок.')
                return
            if amount_m < 1:
                bot.send_message(m.chat.id, 'Вкажіть додатню кількість ячок для переказу.')

            try:
                acc_t = get_passport(m.reply_to_message.from_user.id)
                pp_bus = 2
            except:
                bot.send_message(m.chat.id, 'Введено хибний ідентифікатор отримувача.')
                return
            if len(mess) > 2:
                description = ' '.join(m.text.split()[2:])
            else:
                description = None

        if int(acc_g[9]) < amount_m:
            bot.send_message(m.chat.id, f'На вашому рахунку недостатньо грошей для переказу')
            return

        comm = commission(int(amount_m), 2)

        if int(acc_g[9]) < amount_m + comm:
            bot.send_message(m.chat.id,
                             f'У вас недостатньо коштів на рахунку для списання комісії. Спробуйте меншу суму коштів')
            return

        if pp_bus == 0 or pp_bus == 2:
            acc_g[9] = acc_g[9] - amount_m - comm
            acc_t[9] = acc_t[9] + amount_m
            namep = f'{user_link(acc_t[1], acc_t[2], acc_t[3])}'
            money_t = acc_t[9]
        else:
            acc_g[9] = int(acc_g[9]) - amount_m - comm
            acc_t[4] = int(acc_t[4]) + amount_m
            namep = f'<a href="https://t.me/businesses_yachminiya/{acc_t[7]}">{acc_t[2]}</a>'
            money_t = acc_t[4]

        msg = f'Державний Банк\n'
        msg += f'<b>Ячмінія</b>\n\n'
        msg += f'Переказ коштів\n'
        msg += f'Відправник: {user_link(acc_g[1], acc_g[2], acc_g[3])} ({acc_g[9]})\n'
        msg += f'Отримувач: {namep} ({money_t})\n'
        msg += f'Сума переказу: {amount_m} {glas(amount_m)}\n'
        msg += f'Комісія: {comm} {glas(comm)}\n'
        if description is not None:
            msg += f'Призначення переказу: {description}'

        bot.send_message(m.chat.id, msg, parse_mode='HTML', disable_web_page_preview=True)
        # bot.send_message(-1001282951480, f'Переказ коштів\nСума переказу: {amount_m} {glas(amount_m)}')

        if pp_bus == 0:
            msg = f'Державний Банк\n'
            msg += f'<b>Ячмінія</b>\n\n'
            msg = f'На ваш рахунок переказали кошти\n'
            msg += f'Відправник: {user_link(acc_g[1], acc_g[2], acc_g[3])} ({acc_g[9]})\n'
            msg += f'Сума переказу: {amount_m} {glas(amount_m)}\n'
            if description is not None:
                msg += f'Призначення переказу: {description}'
            try:
                bot.send_message(acc_t[1], msg, parse_mode='HTML', disable_web_page_preview=True)
            except:
                pass
        elif pp_bus == 1:
            # bot.edit_message_text(get_str_business(acc_t[1]), -1001162793975, acc_t[7], parse_mode='HTML')

            msg = f'Державний Банк\n'
            msg += f'<b>Ячмінія</b>\n\n'
            msg += f'На рахунок вашого підприємства переказали кошти\n'
            msg += f'Відправник: {user_link(acc_g[1], acc_g[2], acc_g[3])} ({acc_g[9]})\n'
            msg += f'Отримувач: {namep} ({money_t})\n'
            msg += f'Сума переказу: {amount_m} {glas(amount_m)}\n'
            if description is not None:
                msg += f'Призначення переказу: {description}'
            try:
                bot.send_message(acc_t[3], msg, parse_mode='HTML', disable_web_page_preview=True)
            except:
                pass

        insert_passport_a(acc_g)
        if pp_bus == 0 or pp_bus == 2:
            insert_passport_a(acc_t)
        else:
            insert_business_a(acc_t)
            acc_t = get_passport(acc_t[3])

        update_channel_rid(acc_g[13])
        update_channel_rid(acc_t[13])

    if mess[0] == '!найбагатші':
        if len(mess) < 2:
            bot.send_message(m.chat.id,
                             'Другий аргумент повинен бути одним із наступних:\n<code>Люди</code>\n'
                             '<code>Підприємства</code>\n<code>Роди</code>\n\n'
                             'Примітка: враховуються виключно активи, особисті рахунки ігноруються.',
                             parse_mode='HTML')
            return
        else:
            if mess[1].lower() not in ('люди', 'підприємства', 'роди'):
                bot.send_message(m.chat.id,
                                 'Другий аргумент повинен бути одним із наступних:\n<code>Люди</code>\n'
                                 '<code>Підприємства</code>\n<code>Роди</code>\n\nПримітка: '
                                 'враховуються виключно активи, особисті рахунки ігноруються.',
                                 parse_mode='HTML')
                return
            if len(mess) == 3:
                try:
                    am_n = int(mess[2])
                except:
                    bot.send_message(m.chat.id, 'Неправильний формат.')
                    return
            else:
                am_n = 10

        msg_out = f'Найбагатші {mess[1].lower()}\n'
        passports = get_all_passports()
        businesses = get_all_businesses()
        rids = get_all_rids()
        if mess[1].lower() == 'люди':
            for i in range(len(passports)):
                passports[i][9] = 0
                for j in range(len(businesses)):
                    if passports[i][1] == businesses[j][3]:
                        passports[i][9] += businesses[j][4]

            if am_n > 30:
                am_n = 30
            elif am_n > len(passports):
                am_n = len(passports)

            for i in range(len(passports)):
                for j in range(i, len(passports)):
                    if int(passports[i][9]) < int(passports[j][9]):
                        passports[i], passports[j] = passports[j], passports[i]

            for i in range(am_n):
                if int(passports[i][9]) > 0:
                    msg_out += f'{passports[i][9]} ' \
                               f'<a href="t.me/{passports[i][5]}">{passports[i][2]} {passports[i][3]}</a>\n'
        elif mess[1].lower() == 'підприємства':
            if am_n > 30:
                am_n = 30
            elif am_n > len(businesses):
                am_n = len(businesses)

            for i in range(len(businesses)):
                for j in range(i, len(businesses)):
                    if int(businesses[i][4]) < int(businesses[j][4]):
                        businesses[i], businesses[j] = businesses[j], businesses[i]

            for i in range(am_n):
                if int(businesses[i][4]) > 0:
                    msg_out += f'{businesses[i][4]} <a href="https://t.me/businesses_yachminiya/{businesses[i][7]}">' \
                               f'{businesses[i][2]}</a>\n'
        elif mess[1].lower() == 'роди':
            if am_n > 30:
                am_n = 30
            elif am_n > len(rids):
                am_n = len(rids)

            for i in range(len(rids)):
                all_id = list(map(lambda x: int(x), rids[i][3].split()[2:]))
                passport = get_passport(rids[i][2])
                all_id.append(passport[1])
                businesses = get_business_owner(all_id)
                for j in businesses:
                    rids[i][4] += j[4]

            for i in range(len(rids)):
                for j in range(i, len(rids)):
                    if int(rids[i][4]) < int(rids[j][4]):
                        rids[i], rids[j] = rids[j], rids[i]

            for i in range(am_n):
                if int(rids[i][4]) > 0:
                    msg_out += f'{rids[i][4]} <a href="https://t.me/FamilyRegistry/{rids[i][5]}">{rids[i][1]}</a>\n'

        bot.send_message(m.chat.id, msg_out, parse_mode='HTML', disable_web_page_preview=True)
        return

    if m.text == '!очистити':
        if m.chat.type == 'private':
            return
        if m.reply_to_message is None:
            bot.reply_to(m, 'Команда повинна використовуватись у відповідь на повідомлення')
            return
        u = get_user(m.from_user.id)
        if u is None:
            non_reg(m.from_user, m)
            return
        if not int(u[6].split()[3]):
            bot.reply_to(m, 'Ви не маєте права виконувати цю команду')
            return
        try:
            passport = bot.forward_message(thrash, m.chat.id, m.reply_to_message.message_id).forward_from
            bot.delete_message(m.chat.id, m.reply_to_message.message_id)
        except:
            return
        if passport is not None:
            frw = True
        else:
            frw = False

        for i in range(m.reply_to_message.message_id + 1, m.message_id):
            try:
                if frw:
                    passport = bot.forward_message(thrash, m.chat.id, i).forward_from
                    if passport is not None:
                        if passport.id == m.reply_to_message.from_user.id:
                            bot.delete_message(m.chat.id, i)
                else:
                    mess = bot.forward_message(thrash, m.chat.id, i)
                    passport = mess.forward_from
                    usr_name = mess.forward_sender_name
                    if passport is None:
                        if usr_name == name(m.reply_to_message.from_user):
                            bot.delete_message(m.chat.id, i)
            except:
                pass

        try:
            bot.delete_message(m.chat.id, m.message_id)
        except:
            pass

    if m.text == '!дел':
        if m.chat.type == 'private':
            return
        if m.reply_to_message is None:
            bot.reply_to(m, 'Команда повинна використовуватись у відповідь на повідомлення')
            return
        u = get_user(m.from_user.id)
        if u is None:
            non_reg(m.from_user, m)
            return
        if not int(u[6].split()[3]):
            bot.reply_to(m, 'Ви не маєте права виконувати цю команду')
            return

        try:
            bot.delete_message(m.chat.id, m.reply_to_message.message_id)
            bot.delete_message(m.chat.id, m.message_id)
        except:
            pass

    if m.text == '!айді':
        if m.reply_to_message is not None:
            bot.send_message(m.chat.id, f'{m.reply_to_message.from_user.id}')
            return
        bot.send_message(m.chat.id, f'{m.chat.id}')

    if m.text == '!id':
        msg = f'Chat id: <code>{m.chat.id}</code>\n'
        msg += f'User id: <code>{m.from_user.id}</code>\n'
        if m.reply_to_message is not None:
            msg += f'Reply user id: <code>{m.reply_to_message.from_user.id}</code>\n'
            msg += f'Reply message id: <code>{m.reply_to_message.message_id}</code>\n'
        try:
            bot.send_message(m.chat.id, msg, parse_mode='HTML')
        except:
            pass

    if m.text == '!оновити_актив':
        aktyv_r()
        bot.reply_to(m, 'Таблицю активності успішно оновлено!')
        return

    if mess[0] in ('!інфо', '!а'):
        if m.reply_to_message is not None:
            u = m.reply_to_message.from_user
        else:
            u = m.from_user
        passport = get_passport(u.id)
        if passport is None:
            bot.send_message(m.chat.id, f"{user_link(u.id, name(u))} не має правового зв'язку з Ячмінією")
            return
        all_passports = get_all_passports()
        all_messages = 0
        all_words = 0
        for i in all_passports:
            all_messages += sum(map(lambda x: int(x), i[23].split()))
            all_words += sum(map(lambda x: int(x), i[24].split()))
        if not (all_messages or all_words):
            bot.send_message(m.chat.id, 'Дані відсутні')
            return

        messages = sum(map(lambda x: int(x), passport[23].split()))
        words = sum(map(lambda x: int(x), passport[24].split()))
        per_mess = messages / all_messages
        per_words = words / all_words

        if len(mess) == 1:
            out = f'Інформація\n{user_link(passport[1], passport[2], passport[3])}\n\n'
            out += f'Код: <code>{passport[18]}</code>\n'
            out += f'Репутація: {passport[19]}\n'
            out += f'Повідомлень за місяць: {messages}\n'
            out += f'Слів за місяць: {words}\n'
            out += f"Процент активу: {round((per_mess + per_words) * 50, 2)}%"
            bot.send_message(m.chat.id, out, parse_mode='HTML')
            return

        if mess[0] != '!а':
            bot.send_message(m.chat.id, 'Неправильний формат даних')
            return

        if mess[1].isdigit:
            check_day = int(mess[1]) - 1
        else:
            bot.send_message(m.chat.id, 'Неправильний формат даних')
            return

        if check_day not in range(0, 31):
            bot.send_message(m.chat.id, 'Неправильний формат даних')
            return

        """if mess[1].lower() == 'тиждень':
            word1 = 'Тижнева'
            word2 = 'тиждень'
            day = None
            one_day = False
        elif mess[1].lower() == 'сьогодні':
            day = datetime.today().weekday()
            word1 = 'Сьогоднішня'
            word2 = 'сьогодні'
            one_day = True
        elif mess[1].lower() == 'вчора':
            day = datetime.today().weekday() - 1
            if day < 0:
                day += 7
            word1 = 'Вчорашня'
            word2 = 'вчора'
            one_day = True
        elif mess[1].lower() == 'позавчора':
            day = datetime.today().weekday() - 2
            if day < 0:
                day += 7
            word1 = 'Позавчорашня'
            word2 = 'вчорашня'
            one_day = True
        elif mess[1].lower() == 'завтра':
            time.sleep(1)
            bot.send_message(m.chat.id, 'Я, по твоєму, схожа на Вангу?')
            return
        elif mess[1].lower() == 'післязавтра':
            time.sleep(1)
            bot.send_message(m.chat.id, 'Ну це вже не лізе в жодні рамки. Що ти хочеш від мене?')
            return
        else:
            try:
                day, word2, word1 = weekdays[mess[1].lower()]
            except:
                bot.send_message(m.chat.id, 'Неправильний формат даних')
                return
            one_day = True

        if one_day:
            all_msgs = 0
            all_words = 0
            msg = int(passport[23].split()[day])
            word = int(passport[24].split()[day])
            for i in all_passports:
                all_msgs += int(i[23].split()[day])
                all_words += int(i[24].split()[day])
            m_per = msg / all_msgs
            w_per = word / all_words
            percent = round((m_per + w_per) * 50, 2)
        else:
            msg = 0
            word = 0
            all_msgs = 0
            all_words = 0
            msgs = passport[23].split()
            words = passport[24].split()
            for i in all_passports:
                msg_l = i[23].split()
                word_l = i[24].split()
                for j in range(len(msg_l)):
                    all_msgs += int(msg_l[j])
                    all_words += int(word_l[j])

            for i in range(len(msgs)):
                msg += int(msgs[i])
                word += int(words[i])
            m_per = msg / all_msgs
            w_per = word / all_words
            percent = round((m_per + w_per) * 50, 2)"""

        all_msgs = 0
        all_words = 0
        msg = int(passport[23].split()[check_day])
        word = int(passport[24].split()[check_day])
        for i in all_passports:
            all_msgs += int(i[23].split()[check_day])
            all_words += int(i[24].split()[check_day])
        if not (all_msgs or all_words):
            bot.send_message(m.chat.id, 'Дані відсутні')
            return
        m_per = msg / all_msgs
        w_per = word / all_words
        percent = round((m_per + w_per) * 50, 2)

        if false_day:
            day = false_day
        else:
            day = datetime.today().day
        month = datetime.today().month
        if check_day + 1 > day:
            month = month_num[month - 2]
        str_date = f'{check_day + 1} {months[month][0]}'

        out = f'Активність за {str_date}\n'
        out += f'<a href="tg://user?id={u.id}">{html(name(u))}\n\n</a>'
        out += f'Повідомлень: {msg}\n'
        out += f'Слів: {word}\n'
        out += f"Процент активу: {percent}%"
        bot.send_message(m.chat.id, out, parse_mode='HTML')

    if mess[0] == '!стаття':
        if m.chat.type == 'private':
            bot.reply_to(m, 'Удачі, братан)')
            return
        try:
            number = int(mess[1])
        except:
            bot.send_message(m.chat.id, 'Неправильний формат.')
            return
        if len(mess) < 3:
            if m.reply_to_message is None:
                bot.send_message(m.chat.id, 'Команда використовується у відповідь на повідомлення')
                return
            id_loh = m.reply_to_message.from_user.id
        else:
            id_loh = int(mess[2])

        zhan = get_user(m.from_user.id)
        if zhan is None:
            non_reg(m.from_user, m)
            return

        zher = get_passport(id_loh)
        if zher is None:
            ban = True
            zher = get_user(id_loh)
            if zher is None:
                try:
                    zher = bot.get_chat(id_loh)
                    zher_name = name(zher)
                except:
                    bot.send_message(m.chat.id, 'Неправильний формат.')
                    return
            else:
                zher_name = zher[2]
        else:
            ban = False
            zher_name = zher[2] + zher[3]

        zhan = get_zhan(m.from_user.id)
        try:
            st_am = zhan_queue[m.from_user.id]
        except:
            zhan_queue[m.from_user.id] = 0
            st_am = 0
        if st_am >= zhan_rank[zhan[2]][4]:
            bot.send_message(m.chat.id,
                             f'Ви вже здійснили {st_am} вироків протягом минулої години, що є лімітом. Попросіть іншого'
                             f' жандарма здійснити вирок.')
            return
        else:
            zhan_queue[m.from_user.id] += 1
            Timer(3600, zhan_hour, args=(m.from_user.id,))

        adm = get_all_admin()
        am = len(adm)
        st = adm[number - 1]
        if number > am:
            bot.send_message(m.chat.id, 'Неправильний номер статті.')
            return

        chats = get_all_chats()
        for i in chats:
            if i[6] != 'Основний':
                continue
            if ban:
                time_b = time.time() + int(st[2]) * 3600
                try:
                    bot.kick_chat_member(chat_id=i[2], user_id=id_loh, until_date=time_b)
                except:
                    pass
            else:
                time_m = time.time() + int(st[2]) * 3600
                try:
                    bot.restrict_chat_member(chat_id=i[2], user_id=id_loh, until_date=time_m)
                except:
                    pass
        if ban:
            text1 = 'Ви були вилучені із Простору Ячмінії'
            text2 = 'вилучений із Простору Ячмінії за статею'
        else:
            text1 = 'Ви втратили право спілкування у Просторі Ячмінії'
            text2 = 'втрачає право спілкування у Просторі Ячмінії за статею'

        zhan_pass = get_passport(m.from_user.id)
        keyboard = types.InlineKeyboardMarkup()
        button = types.InlineKeyboardButton(text='Подати позов у Карний Суд', callback_data='krime_sud_nm')
        keyboard.add(button)
        try:
            bot.send_message(m.chat.id,
                             f'<a href="tg://user?id={id_loh}">{html(zher_name)}</a> {text2} {number} '
                             f'<a href="https://telegra.ph/Rozd%D1%96l-%D0%86%D0%86%D0%86-Adm%D1%96n%D1%96strativn%D1%9'
                             f'6-pravoporushennya-04-24">Розділу ІІІ Карного зводу</a> на {st[2]} годин(и)',
                             parse_mode='HTML', disable_web_page_preview=True)
            bot.send_message(id_loh,
                             f'{text1} {zhan_rank[zhan[2]][5]} '
                             f'<a href="tg://user?id={m.from_user.id}">{zhan_pass[2]} {zhan_pass[3]}</a> '
                             f'<code>{zhan_pass[18]}</code> на {st[2]} годин(и) за статею {number} '
                             f'<a href="https://telegra.ph/Rozd%D1%96l-%D0%86%D0%86%D0%86-Adm%D1%96n'
                             f'%D1%96strativn%D1%96-pravoporushennya-04-24">Розділу ІІІ Карного зводу</a>\n'
                             f'Текст статті:\n{st[1]}\n\nЯкщо ви вважаєте, що цей вирок був неправомірним, подайте '
                             f'позов на Жандарма у Карний Суд за статею Х.',
                             reply_markup=keyboard, parse_mode='HTML', disable_web_page_preview=True)
        except Exception as e:
            print(e)
        zhan[3] += 1
        zhan[4] += 1
        insert_zhan_a(zhan)

    """if m.text == '!додати_чат':
        if m.chat.type == 'private':
            return
        user = get_user(m.from_user.id)
        if user is None:
            non_reg(m.from_user, m)
            return
        chat = get_chat(m.chat.id)
        number = chat[0]

        user[9] += f' {number}'
        insert_user_a(user)
        bot.reply_to(m, 'Цей чат успішно додано до вашого Простору Ячмінії!')
        return"""

    if m.text == '!помилування':
        if m.chat.type == 'private':
            bot.reply_to(m, 'Удачі, братан)')
            return
        if m.reply_to_message is None:
            bot.send_message(m.chat.id, 'Команда повинна бути використана у відповідь на повідомлення')
            return

        zhan = get_user(m.from_user.id)
        if zhan is None:
            non_reg(m.from_user, m)
            return
        rights = zhan[6]
        if not int(rights.split()[4]):
            bot.send_message(m.chat.id, 'Ви не маєте прав на використання цієї команди')
            return

        chats = get_all_chats()
        for i in chats:
            try:
                bot.unban_chat_member(chat_id=i[2], user_id=m.reply_to_message.from_user.id, only_if_banned=True)
                bot.promote_chat_member(chat_id=i[2], user_id=m.reply_to_message.from_user.id)
            except:
                pass
        bot.send_message(m.chat.id, f'{html(name(m.reply_to_message.from_user))} поновлений(а) у своїх правах')
        try:
            bot.send_message(m.reply_to_message.from_user.id, 'Ви поновлені у своїх правах у Просторі Ячмінії')
        except:
            pass
        return

    if m.text == '!черга':
        if m.from_user.id != CREATOR:
            # bot.reply_to(m, 'Ви не маєте права на використання цієї команди')
            return
        zhandarm = 0
        bot.send_message(m.chat.id, 'Чергу Жандармерії успішно очищено!')
        return

    # if m.text == '!зарплата':

    # голосування. початок та завершення

    if mess[0].split('_')[0] == '!найактивніші':
        if len(mess[0].split('_')) == 2:
            if mess[0].split('_')[1].isdigit():
                am_n = int(mess[0].split('_')[1])
            else:
                bot.send_message(m.chat.id, 'Неправильний формат!')
                return
        elif len(mess[0].split('_')) == 1:
            am_n = 10
        else:
            bot.send_message(m.chat.id, 'Неправильний формат!')
            return

        if len(mess) == 1:
            alltime = True
            check_day = None
        elif len(mess) == 2:
            if mess[1].isdigit():
                alltime = False
                check_day = (True, int(mess[1]) - 1)
                if check_day[1] not in range(0, 31):
                    bot.send_message(m.chat.id, 'Неправильний формат даних')
                    return
            elif mess[1].lower() == 'тиждень':
                alltime = False
                check_day = (False, 'тиждень')
            else:
                bot.send_message(m.chat.id, 'Неправильний формат!')
                return
        else:
            bot.send_message(m.chat.id, 'Неправильний формат!')
            return

        passports = get_all_passports()
        if am_n > len(passports):
            am_n = len(passports)
        elif am_n > 40:
            am_n = 40

        if alltime:
            for i in passports:
                i[23] = sum(map(lambda y: int(y), i[23].split()))
                i[24] = sum(map(lambda y: int(y), i[24].split()))
            in_word = ''
        else:
            if check_day[0]:
                for i in passports:
                    i[23] = int(i[23].split()[check_day[1]])
                    i[24] = int(i[24].split()[check_day[1]])

                if false_day:
                    day = false_day
                else:
                    day = datetime.today().day
                month = datetime.today().month
                if check_day[1] + 1 > day:
                    month = month_num[month - 2]
                in_word = f' за {check_day[1] + 1} {months[month][0]}'
            else:
                return
        all_messages = sum((i[23] for i in passports))
        all_words = sum((i[24] for i in passports))
        percentages = [[i[1], round((((i[23] / all_messages) + (i[24] / all_words)) * 50), 2)] for i in passports]
        percentages.sort(key=itemgetter(1), reverse=True)

        msg_out = f'Найактивніші{in_word}\n'
        long_len = len(str(percentages[0][1]))
        for i in percentages:
            i[0] = get_passport(i[0])
            if round(i[1], 1) == i[1]:
                zero = '0'
                minus = 1
            else:
                zero = ''
                minus = 0
            i[1] = f'<code>{" " * (long_len - len(str(i[1])) - minus)}{i[1]}{zero}% </code>'
        for i in range(am_n):
            msg_out += f'{percentages[i][1]}' \
                       f'<a href="t.me/{percentages[i][0][5]}">{percentages[i][0][2]} {percentages[i][0][3]}</a>\n'
        bot.send_message(m.chat.id, msg_out, disable_web_page_preview=True, parse_mode='HTML')

    if m.text.split()[0] == '!права':
        if m.from_user.id != CREATOR:
            bot.reply_to(m, 'Ви не маєте права на використання цієї команди!')
            return
        id = int(mess[1])
        rights = ' '.join(mess[2:])
        user = get_user(id)
        if user is None:
            bot.send_message(m.chat.id, 'щось не так.')
            return
        user[6] = rights
        insert_user_a(user)
        bot.send_message(m.chat.id, 'Права оновлено!')
        return

    if m.text.split()[0] == '!перевірка':
        if m.from_user.id != CREATOR:
            return
        keyboard = types.InlineKeyboardMarkup()
        button = types.InlineKeyboardButton(text='🗳 Голосування', callback_data='golos')
        keyboard.add(button)
        msg = ''
        bot.send_message(m.chat.id, msg, reply_markup=keyboard)

    if m.text.split()[0] == '!лотерея':
        user = get_user(m.from_user.id)
        if user is None:
            return

        if not int(user[6].split()[7]):
            bot.reply_to(m, 'Ви не маєте прав на використання цієї команди')
            return

        try:
            num = m.text.split()[1].split('-')
            num1 = int(num[0])
            num2 = int(num[1])
            if len(m.text.split()) > 2:
                num3 = int(m.text.split()[2])
                our_list = list(range(num1, num2 + 1))
                num_out = ''
                for i in range(num3):
                    el = random.choice(our_list)
                    our_list.remove(el)
                    num_out += f'{el}\n'
            else:
                num_out = random.randint(num1, num2)
            bot.send_message(m.chat.id, num_out)
        except Exception as e:
            bot.send_message(m.chat.id, f'Неправильний формат')
            return

    if m.text.split()[0] == '!пов':
        if m.from_user.id != CREATOR:
            return
        id_t = int(m.text.split()[1])
        text = ' '.join(m.text.split()[2:])
        try:
            bot.send_message(id_t, text)
        except:
            pass
    if m.text.split()[0] == '!повр':
        if m.from_user.id != CREATOR:
            return
        id_t = int(m.text.split()[1])
        rep_id = int(m.text.split()[2])
        text = ' '.join(m.text.split()[3:])
        try:
            bot.send_message(id_t, text, reply_to_message_id=rep_id)
        except:
            pass

    if m.text.split()[0] in ('!нарахувати', '!списати'):
        user = get_user(m.from_user.id)
        if user is None:
            bot.send_message(m.chat.id, f'Ви не маєте громадянства Ячмінії.')
        if not int(user[6].split()[7]):
            bot.send_message(m.chat.id, 'Ви не маєте прав на використання цієї команди')
            return

        if m.reply_to_message is None:
            if len(mess) < 3:
                bot.send_message(m.chat.id, 'Неправильний формат вхідних даних.')
                return
            try:
                amount_m = int(mess[2])
            except:
                bot.send_message(m.chat.id, 'Введено хибну кількість ячок.')
                return
            if amount_m < 1:
                bot.send_message(m.chat.id, 'Вкажіть додатню кількість ячок для переказу.')

            acc_t = get_passport(mess[1])
            pp_bus = 0
            if acc_t is None:
                acc_t = get_business(mess[1])
                pp_bus = 1
                if acc_t is None:
                    bot.send_message(m.chat.id, 'Введено хибний ідентифікатор отримувача.')
                    return

            if len(mess) > 3:
                description = ' '.join(m.text.split()[3:])
            else:
                description = None
        else:
            if len(mess) < 2:
                bot.send_message(m.chat.id, 'Неправильний формат вхідних даних.')
                return
            try:
                amount_m = int(mess[1])
            except:
                bot.send_message(m.chat.id, 'Введено хибну кількість ячок.')
                return
            if amount_m < 1:
                bot.send_message(m.chat.id, 'Вкажіть додатню кількість ячок для переказу.')

            try:
                acc_t = get_passport(m.reply_to_message.from_user.id)
                pp_bus = 2
            except:
                bot.send_message(m.chat.id, 'Введено хибний ідентифікатор отримувача.')
                return
            if len(mess) > 2:
                description = ' '.join(m.text.split()[2:])
            else:
                description = None

        if m.text.split()[0] == '!нарахувати':
            line_1 = 'Нарахування коштів'
            line_2 = 'нарахування'
            line_3 = 'На ваш рахунок переказали кошти'
            line_4 = 'На рахунок вашого підприємства нарахували кошти'
            plus = True
        else:
            line_1 = 'Списання коштів'
            line_2 = 'списання'
            line_3 = 'З вашого рахунку списали кошти'
            line_4 = 'З рахунку вашого підприємства списали кошти'
            plus = False

        if pp_bus == 0 or pp_bus == 2:
            if plus:
                acc_t[9] = acc_t[9] + amount_m
            else:
                acc_t[9] = acc_t[9] - amount_m
            namep = f'{user_link(acc_t[1], acc_t[2], acc_t[3])}'
            money_t = acc_t[9]
        else:
            if plus:
                acc_t[4] = int(acc_t[4]) + amount_m
            else:
                acc_t[4] = int(acc_t[4]) - amount_m
            namep = f'<a href="https://t.me/businesses_yachminiya/{acc_t[7]}">{acc_t[2]}</a>'
            money_t = acc_t[4]

        msg = f'Державний Банк\n'
        msg += f'<b>Ячмінія</b>\n\n'
        msg += f'{line_1}\n'
        msg += f'Рахунок: {namep} ({money_t})\n'
        msg += f'Сума {line_2}: {amount_m} {glas(amount_m)}\n'
        if description is not None:
            msg += f'Призначення {line_2}: {description}'

        bot.send_message(m.chat.id, msg, parse_mode='HTML', disable_web_page_preview=True)
        # bot.send_message(-1001282951480, f'Переказ коштів\nСума переказу: {amount_m} {glas(amount_m)}')

        if pp_bus == 0:
            msg = f'Державний Банк\n'
            msg += f'<b>Ячмінія</b>\n\n'
            msg = f'{line_3}\n'
            msg += f'Сума переказу: {amount_m} {glas(amount_m)}\n'
            if description is not None:
                msg += f'Призначення переказу: {description}'
            try:
                bot.send_message(acc_t[1], msg, parse_mode='HTML', disable_web_page_preview=True)
            except:
                pass
        elif pp_bus == 1:
            # bot.edit_message_text(get_str_business(acc_t[1]), -1001162793975, acc_t[7], parse_mode='HTML')

            msg = f'Державний Банк\n'
            msg += f'<b>Ячмінія</b>\n\n'
            msg += f'{line_4}\n'
            msg += f'Рахунок: {namep} ({money_t})\n'
            msg += f'Сума {line_2}: {amount_m} {glas(amount_m)}\n'
            if description is not None:
                msg += f'Призначення {line_2}: {description}'
            try:
                bot.send_message(acc_t[3], msg, parse_mode='HTML', disable_web_page_preview=True)
            except:
                pass

        if pp_bus == 0 or pp_bus == 2:
            insert_passport_a(acc_t)
        else:
            insert_business_a(acc_t)
        return

    if m.text.split()[0] == '!сан':
        new_san = ' '.join(mess[1:])
        sans = new_san.split(', ')
        user = get_user(m.from_user.id)
        user_s = get_user(m.reply_to_message.from_user.id)
        passport = get_passport(m.reply_to_message.from_user.id)

        if m.from_user.id != CREATOR:
            if sans[0] == 'Безробітний' and int(user[6].split()[8]) == 1 and passport[8] == 'Без сану':
                pass
            else:
                bot.send_message(m.chat.id, 'Ви не маєте права використовувати цю команду')
                return
        if m.reply_to_message is None:
            bot.reply_to(m, 'Ця команда використовується у відповідь на повідомлення')
            return
        try:
            sans_all = get_sans(sans)
        except Exception as e:
            bot.send_message(m.chat.id, f'Неправильний сан\n{e}')
            return
        bill = 0
        us_rights = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        pass_rights = [0, 0, 0, 0, 0]
        for i in sans_all:
            bill += i[2]
            us_rights_buf = i[3].split()
            pass_rights_buf = i[4].split()
            for j in range(len(us_rights_buf)):
                us_rights[j] = str(int(us_rights_buf[j]) | int(us_rights[j]))
            for j in range(len(pass_rights_buf)):
                pass_rights[j] = str(int(pass_rights_buf[j]) | int(pass_rights[j]))

        passport[12] = ' '.join(pass_rights)
        user_s[6] = ' '.join(us_rights)
        old_san = passport[8]
        passport[8] = new_san
        passport[11] = bill
        bot.send_message(m.chat.id, 'Сан змінено')
        out = f'{user_link(passport[1], passport[2], passport[3])}\n{old_san} ⟹ {new_san}'
        # bot.send_message(-1001268255961, out, parse_mode='HTML')
        insert_passport_a(passport)
        insert_user_a(user_s)
        return

    if m.text.split()[0] == '!пін':
        if m.from_user.id != CREATOR:
            return
        chat_to_pin = m.text.split()[1]
        message_to_pin = m.text.split()[2]
        bot.pin_chat_message(chat_to_pin, message_to_pin)

    if m.text == "!закон":
        if f_queue(m):
            return
        bot.send_message(m.chat.id, '<a href="https://t.me/ZakonYach">Законодавство Ячмінії</a>', parse_mode='HTML')

    '''if m.text == '!розсилка':
        if m.from_user.id != CREATOR:
            return
        all_id = get_vote()
        all_passports = get_all_passports()
        passports_id = all_passports[1]
        keyboard = types.InlineKeyboardMarkup()
        button = types.InlineKeyboardButton(text='🗳 Голосування', callback_data='golos')
        keyboard.add(button)
        msg = ''
        for i in range(len(passports_id)):
            if passports_id[i] not in all_id:
                if all_passports[10][i] == '1':
                    try:
                        # bot.forward_message(int(passports_id[i]), -1001320320609, 192)
                        bot.send_message(int(passports_id[i]), mes, reply_markup=keyboard)
                        msg += f'<a href="tg://user?id={passports_id[i]}">підорас не проголосував\n</a>'
                    except:
                        msg += f'<a href="tg://user?id={passports_id[i]}">підорас не зареганий\n</a>'
        bot.send_message(m.chat.id, msg, parse_mode='HTML')'''

    if m.text.split()[0] == '!розсилка_н':
        if m.from_user.id != CREATOR:
            return
        users = get_all_users()
        n = int(mess[1])
        if n == -1:
            bot.forward_message(CREATOR, -1001320320609, 189)
            return

        for i in range(n * 50, (n + 1) * 50):
            try:
                bot.forward_message(int(users[i][2]), -1001320320609, 189)
            except Exception as e:
                print(e)

    if m.text.split()[0] == '!хтмл':
        if m.from_user.id != CREATOR:
            return
        bot.send_message(CREATOR, ' '.join(m.text.split()[1:]), parse_mode='HTML')

    # TODO бан і мут

    if m.text == '!жандармерія':
        if m.chat.type == 'private':
            return
        chat = get_chat(m.chat.id)
        if chat[4] == 'NoneURL':
            return
        out = f'<a href="tg://user?id={m.from_user.id}">{html(name(m.from_user))}</a>\n' \
              f'<a href="{chat[4]}/{m.message_id}">{m.chat.title}</a>'
        # bot.send_message(-1001422128910, out, parse_mode='HTML')
        bot.send_message(m.chat.id, 'Жандармерію успішно викликано')
        return

    if m.text == '!команди':
        bot.send_message(m.chat.id,
                         f'<a href="https://telegra.ph/Spisok-komand-Sistemi-YAchm%D1%96n%D1%96ya-02-01">Список команд '
                         f'Системи</a>',
                         parse_mode='HTML', disable_web_page_preview=True)

    if m.text.split()[0] == '!тег':
        try:
            id = mess[1]
            text = mess[2:]
            bot.send_message(m.chat.id, f'<a href="tg://user?id={id}">{" ".join(text)}</a>', parse_mode='HTML')
        except:
            pass

    if mess[0] == '!підприємство':
        if len(m.text.split()) < 2:
            bot.send_message(m.chat.id, 'Неправильний формат!')
            return
        pidp_id = ' '.join(mess[1:])

        business_out = get_str_business(pidp_id)

        bot.send_message(m.chat.id, business_out, parse_mode='HTML', disable_web_page_preview=True)
        return

    if mess[0] == '!рід':

        if len(m.text.split()) < 2:
            bot.send_message(m.chat.id, 'Неправильний формат!')
            return
        rid_id = ' '.join(m.text.split()[1:])

        rid_out = get_str_rid(rid_id)
        bot.send_message(m.chat.id, rid_out, parse_mode='HTML', disable_web_page_preview=True)
        if m.chat.id == -1001329014820:
            bot.send_message(m.chat.id, time.time() - tt)
        return

    if mess[0] == '!установа':
        if len(m.text.split()) < 2:
            bot.send_message(m.chat.id, 'Неправильний формат!')
            return
        ust_id = ' '.join(mess[1:])

        inst_out = get_str_institution(ust_id)

        bot.send_message(m.chat.id, inst_out, parse_mode='HTML', disable_web_page_preview=True)
        return

    if m.chat.id == -1001486037908:
        mess = m.text.split('\n')
        mess_words = m.text.split()
        if {'Форма', 'для', 'оформлення', 'громадянства', "Ім'я:", 'Прізвище:', 'Стать:'}.issubset(set(mess_words)):
            try:
                namep = None
                surname = None
                acc_name = None
                acc_surname = None
                sex = None
                for i in mess:
                    if i.split()[0] == "Ім'я:":
                        namep = ' '.join(i.split()[1:])
                    elif i.split()[0] == "Прізвище:":
                        surname = ' '.join(i.split()[1:])
                    elif ' '.join(i.split()[0:4]) == "Ім'я у знахідному відмінку:":
                        acc_name = ' '.join(i.split()[4:])
                    elif ' '.join(i.split()[0:4]) == "Прізвище у знахідному відмінку:":
                        acc_surname = ' '.join(i.split()[4:])
                    elif i.split()[0] == "Стать:":
                        sex = ' '.join(i.split()[1:])
                if not (namep and surname and acc_name and acc_surname and sex):
                    bot.reply_to(m,
                                 "Ви неправильно ввели форму. Перевірте будь ласка:\n1. Чи ви скопіювали саме форму, "
                                 "а не все повідомлення?\n2. Чи стоять пропуски після пунктів форми?")
                    return
                full_name = namep + surname

                # name_i = mess.index("Ім'я:")
                # surname_i = mess.index("Прізвище:")
                # gen_name_i ==
                # sex_i = mess.index("Стать:")
                # namep = ' '.join(mess[name_i + 1:surname_i])
                # surname = ' '.join(mess[surname_i + 1:sex_i])
                # sex = str(mess[sex_i + 1])
                if len(namep) > 25:
                    bot.send_message(m.chat.id, "Ім'я не може містити більше 25 символів")
                    return
                elif len(surname) > 30:
                    bot.send_message(m.chat.id, "Прізвище не може містити більше 30 символів")
                    return
                if len(namep) < 2:
                    bot.send_message(m.chat.id, "Закоротке ім'я")
                    return
                elif len(surname) < 2:
                    bot.send_message(m.chat.id, "Закоротке прізвище")
                    return
                elif len(full_name) > 45:
                    bot.send_message(m.chat.id, "Сума довжин прізвища та імені не може бути довша за 40 символів")
                    return
                elif len(re.split('[- ]', namep)) > 2:
                    bot.send_message(m.chat.id, "Ім'я не може містити більше двох слів")
                    return
                elif len(re.split('[- ]', surname)) > 3:
                    bot.send_message(m.chat.id, "Прізвище не може містити більше трьох слів")
                    return
                spl_name = re.split('[- ]', namep)
                spl_acc_name = re.split('[- ]', acc_name)
                spl_surname = re.split('[- ]', surname)
                spl_acc_surname = re.split('[- ]', acc_surname)
                for i in range(len(spl_name)):
                    if len(spl_name[i]) < 4:
                        if spl_name[i][0:len(spl_name) - 2] != spl_acc_name[i][0:len(spl_name) - 2]:
                            bot.send_message(m.chat.id, "Ім'я у називному та знахідному відмінку не збігаються")
                            return
                    else:
                        if spl_name[i][0:len(spl_name[i]) - 3] != spl_acc_name[i][0:len(spl_name[i]) - 3]:
                            bot.send_message(m.chat.id, "Ім'я у називному та знахідному відмінку не збігаються")
                            return
                for i in range(len(spl_surname)):
                    if len(spl_surname[i]) < 4:
                        if spl_surname[i][0:len(spl_surname[i]) - 1] != spl_acc_surname[i][0:len(spl_surname[i]) - 1]:
                            bot.send_message(m.chat.id, "Прізвище у називному та знахідному відмінку не збігаються")
                            return
                    else:
                        if spl_surname[i][0:len(spl_surname[i]) - 2] != spl_acc_surname[i][0:len(spl_surname[i]) - 2]:
                            bot.send_message(m.chat.id, "Прізвище у називному та знахідному відмінку не збігаються")
                            return

                for i in full_name.lower():
                    if i not in alphabet:
                        bot.send_message(m.chat.id,
                                         "Ім'я та прізвище повинні містити тільки кириличні букви, дефіс та апостроф.")
                        return
                if sex.lower() != 'чоловіча' and sex.lower() != 'жіноча':
                    bot.send_message(m.chat.id, 'Стать може бути тільки чоловіча або жіноча')
                    return

                passport_out = f'<b>Шаблон паспорта</b>\n'
                passport_out += f'<i>Громадянина Ячмінії</i>\n\n'
                passport_out += f'''<b>Ім'я:</b> '''
                '''<i><a href="tg://user?id={m.from_user.id}">{namep} {surname}</a></i>\n'''
                passport_out += f"<b>Сан:</b> <i>Без сану</i>\n"
                passport_out += f"<b>Стать:</b> <i>{sex}</i>\n"
                passport_out += f"<b>Статус:</b> <i>Без статусу</i>\n"
                passport_out += f"\n<i>Дата видачі:</i>"
                passport_out += f"\n<i>0000-00-00 00:00:00</i>"
                passport_out += f'''\n\n<b>Ім'я у знахідному відмінку:</b> '''
                passport_out += f'''<i><a href="tg://user?id={m.from_user.id}">{acc_name} {acc_surname}</a></i>\n'''
                bot.reply_to(m, passport_out, parse_mode='HTML')
            except Exception as e:
                print(e)
                bot.reply_to(m,
                             '''Ви неправильно ввели форму. Перевірте будь ласка:\n1. Чи ви скопіювали саме форму, а не 
                             все повідомлення?\n2. Чи стоять пропуски після пунктів форми?''')

        if m.text == '!реєстрація':
            ms = m.reply_to_message
            passport = get_passport(ms.from_user.id)
            if passport is not None:
                bot.send_message(m.chat.id,
                                 f'{user_link(passport[1], passport[2], passport[3])} вже має '
                                 f'громадянство Ячмінії!',
                                 parse_mode='HTML')
                return
            try:
                namep = None
                surname = None
                acc_name = None
                acc_surname = None
                sex = None
                for i in mess:
                    if i.split()[0] == "Ім'я:":
                        namep = ' '.join(i.split()[1:])
                    elif i.split()[0] == "Прізвище:":
                        surname = ' '.join(i.split()[1:])
                    elif ' '.join(i.split()[0:4]) == "Ім'я у знахідному відмінку:":
                        acc_name = ' '.join(i.split()[4:])
                    elif ' '.join(i.split()[0:4]) == "Прізвище у знахідному відмінку:":
                        acc_surname = ' '.join(i.split()[4:])
                    elif i.split()[0] == "Стать:":
                        sex = ' '.join(i.split()[1:])
                if not (namep and surname and acc_name and acc_surname and sex):
                    bot.reply_to(m,
                                 '''Ви неправильно ввели форму. Перевірте будь ласка:\n1. Чи ви скопіювали саме форму, 
                                 а не все повідомлення?\n2. Чи стоять пропуски після пунктів форми?''')
                    return
            except:
                bot.send_message(m.chat.id, 'Неправильний формат даних')
                return

            new_passport(ms.from_user, namep, surname, sex, acc_name, acc_surname)
            passport = get_str_passport(ms.from_user.id)
            bot.send_message(m.chat.id, passport, parse_mode='HTML')
            keyboard = types.InlineKeyboardMarkup()
            but = types.InlineKeyboardButton(text="Основний Чат Ячмінії", url='t.me/Yachminiya')
            keyboard.add(but)
            bot.send_message(m.chat.id,
                             f'Ти отримав(ла) громадянство із статусом "Початковий". '
                             f'Щоб отримати "Повний" статус, виконай відповідні умови із '
                             f'<a href="https://telegra.ph/Zakon-pro-gromadyanstvo-01-24">Закону про громадянство</a>, '
                             f'та звернись сюди в Графство з відповідним проханням.\n\nЩоб перевірити активність, '
                             f'надсилай окремим повідомленням команду !а. Для того, щоб подивитись паспорт - !п.\n',
                             disable_web_page_preview=True, parse_mode='HTML', reply_markup=keyboard,
                             reply_to_message_id=ms.message_id)
            return

        if m.text == '!оновити_паспортні_дані':
            mess = m.reply_to_message.text.split('\n')
            if m.reply_to_message is None:
                bot.send_message(m.chat.id, 'Ця команда може бути використана тільки у відповідь на повідомлення')
                return
            graf = get_passport(m.from_user.id)
            if graf is None:
                bot.send_message(m.chat.id, f'Ви не маєте громадянства Ячмінії!')
                return
            graf = get_user(m.from_user.id)
            if graf is None:
                non_reg(m.from_user, m)
                return
            if not int(graf[6].split()[0]):
                bot.send_message(m.chat.id, 'Ви не маєте права на використання цієї команди')
                return
            passport = get_passport(m.reply_to_message.from_user.id)
            if passport is None:
                bot.send_message(m.chat.id, f'{name(m.reply_to_message.from_user)} не має громадянства Ячмінії!')
                return

            try:
                namep = None
                surname = None
                acc_name = None
                acc_surname = None
                sex = None
                for i in mess:
                    if i.split()[0] == "Ім'я:":
                        namep = ' '.join(i.split()[1:])
                    elif i.split()[0] == "Прізвище:":
                        surname = ' '.join(i.split()[1:])
                    elif ' '.join(i.split()[0:4]) == "Ім'я у знахідному відмінку:":
                        acc_name = ' '.join(i.split()[4:])
                    elif ' '.join(i.split()[0:4]) == "Прізвище у знахідному відмінку:":
                        acc_surname = ' '.join(i.split()[4:])
                    elif i.split()[0] == "Стать:":
                        sex = ' '.join(i.split()[1:])
                if not (namep and surname and acc_name and acc_surname and sex):
                    bot.reply_to(m,
                                 '''Ви неправильно ввели форму. Перевірте будь ласка:\n1. 
                                 Чи ви скопіювали саме форму, а не все повідомлення?\n2. 
                                 Чи стоять пропуски після пунктів форми?''')
                    return
            except:
                bot.send_message(m.chat.id, 'Неправильний формат даних')
                return

            passport[2] = namep
            passport[3] = surname
            passport[6] = sex
            passport[16] = acc_name
            passport[17] = acc_surname
            bot.send_message(m.chat.id, 'Паспортні дані оновлено')
            insert_passport_a(passport)

        if m.text == '!відмова_від_громадянства':
            passport = get_passport(m.from_user.id)
            if passport is None:
                bot.send_message(m.chat.id, f'Ви не маєте громадянства Ячмінії!')
                return
            keyboard = types.InlineKeyboardMarkup()
            button = types.InlineKeyboardButton(text='❌ Відмовитись від громадянства', callback_data='vidmova')
            keyboard.add(button)
            button = types.InlineKeyboardButton(text='🚫 Відмінити процедуру відмови від громадянства',
                                                callback_data='stop_vidmova')
            keyboard.add(button)
            bot.send_message(m.chat.id,
                             text=f'{user_link(passport[1], passport[2], passport[3])}, '
                                  f'Ви справді відмовляєтесь від громадянства Ячмінії? Ви втратите всі '
                                  f'свої статки. Для підтвердження натисніть кнопку нижче.',
                             reply_markup=keyboard, parse_mode='HTML')

        if m.text == '!вилучити_громадянство':
            if m.reply_to_message is None:
                bot.send_message(m.chat.id, 'Ця команда може бути використана тільки у відповідь на повідомлення')
                return
            graf = get_passport(m.from_user.id)
            if graf is None:
                bot.send_message(m.chat.id, f'Ви не маєте громадянства Ячмінії!')
                return
            graf = get_user(m.from_user.id)
            if graf is None:
                non_reg(m.from_user, m)
                return
            if not int(graf[6].split()[0]):
                bot.send_message(m.chat.id, 'Ви не маєте права на використання цієї команди')
                return
            passport = get_passport(m.reply_to_message.from_user.id)
            if passport is None:
                bot.send_message(m.chat.id, f'{name(m.reply_to_message.from_user)} не має громадянства Ячмінії!')
                return

            all_passports = get_all_passports()
            del (all_passports[passport[0] - 1])
            for i in range(len(all_passports)):
                all_passports[i][0] = i + 1
            del_table_passports()
            db.insert(table_passports)
            insert_all_passports_l(all_passports)
            amount = get_amount_of_passports()
            bot.send_message(m.chat.id, f'{name(m.reply_to_message.from_user)} втрачає громадянство Ячмінії!')
            del_passport_g(all_passports, amount)
            # TODO рід та бізнес

        if mess_words[0] == '!статус':
            if len(mess_words) < 2:
                return
            if m.reply_to_message is None:
                bot.send_message(m.chat.id, 'Ця команда може бути використана тільки у відповідь на повідомлення!')
                return
            graf = get_passport(m.from_user.id)
            if graf is None:
                bot.send_message(m.chat.id, f'Ви не маєте громадянства Ячмінії!')
                return
            graf = get_user(m.from_user.id)
            if graf is None:
                non_reg(m.from_user, m)
                return
            if not int(graf[6].split()[0]):
                bot.send_message(m.chat.id, 'Ви не маєте права на використання цієї команди')
                return
            if mess_words[1] not in ('Повний', 'Початковий'):
                bot.send_message(m.chat.id, f'Неправильний статус громадянства!')
                return
            passport = get_passport(m.reply_to_message.from_user.id)
            if passport is None:
                bot.send_message(m.chat.id, f'{name(m.reply_to_message.from_user)} не має громадянства Ячмінії!')
                return
            user = get_user(m.reply_to_message.from_user.id)

            if (mess_words[1] == 'Повний') and (
                    time.time() - datetime.strptime(passport[7], '%Y-%m-%d %H:%M:%S').timestamp() < 259200 or user[
                7] < 300):
                keyboard = types.InlineKeyboardMarkup()
                button = types.InlineKeyboardButton(text='✅ Підтвердити', callback_data='up_status')
                keyboard.add(button)
                bot.send_message(m.chat.id,
                                 f'{user_link(passport[1], passport[2], passport[3])} не виконав усі '
                                 f'підстави для отримання повного статусу громадянства. Для отримання цього статусу '
                                 f'необхідне підтвердження Старшого Жандарма або Протектора.',
                                 parse_mode='HTML', reply_markup=keyboard)
                return

            passport[10] = mess_words[1]
            bot.send_message(m.chat.id,
                             f'Статус громадянства <a href="tg://user?id={passport[1]}">{passport[2]} {passport[3]}'
                             f'</a> змінено на {passport[10]}!',
                             parse_mode='HTML')
            insert_passport_a(passport)

        if m.text == '!форми':
            out = 'Форма для паспорта – <code>!паспорт</code>\nФорма для партії –  <code>!партія</code>'
            bot.send_message(m.chat.id, out, parse_mode='HTML')
            return

        if m.text == '!партія':
            out = '<code>Партія Ячмінії\n"Назва партії"\n\nКерівник — @\n\n1. @\n2. @\n3. @\n4. @\n</code>'
            bot.send_message(m.chat.id, out, parse_mode='HTML')
            return

        if m.text == '!паспорт':
            bot.send_message(m.chat.id, pass_form, parse_mode='HTML')

    if m.chat.id == -1001262104547 or m.chat.id == -1001457025006:
        if mess[0] == '!відмова' and m.reply_to_message is not None:
            passport = get_passport(m.from_user.id)
            if passport is None:
                return
            try:
                bot.send_message(m.reply_to_message.entities[0].user.id,
                                 f'Вам відмовлено у задоволенні позову\nПричина:\n{" ".join(m.text.split()[1:])}\nВам '
                                 f'відмовив Суддя {user_link(passport[1], passport[2], passport[3])}',
                                 parse_mode='HTML')
                bot.send_message(m.chat.id, 'Відмова доставлена')
            except Exception as e:
                bot.send_message(m.chat.id, f'щось пішло не так...\n{e}')
            return

        if m.text.split()[0] == '!відповідь':
            if m.reply_to_message is None:
                return
            try:
                bot.send_message(m.reply_to_message.entities[0].user.id, m.text.split()[1:], parse_mode='HTML')
                bot.send_message(m.chat.id, 'Відповідь доставлена')
            except Exception as e:
                bot.send_message(m.chat.id, f'щось пішло не так...\n{e}')
            return

    if m.chat.id == -1001157589989:
        if m.text == '!початок_засідання':
            rech = get_passport(m.from_user.id)
            if rech is None:
                return
            if not int(rech[12].split()[0]):
                bot.send_message(m.chat.id, 'Ви не маєте права на використання цієї команди')
                return

            keyboard = types.InlineKeyboardMarkup()
            callback_button = types.InlineKeyboardButton(text="Присутній", callback_data="kvorum")
            keyboard.add(callback_button)

            bot.send_message(m.chat.id, f'Перевірка кворуму\n\nПрисутні:', reply_markup=keyboard)


@bot.message_handler(content_types=['photo', 'audio', 'document', 'video', 'voice', 'sticker', 'video_note'])
def media(m):
    chat = get_chat(m.chat.id)
    if m.chat.type != 'private':
        if not chat:
            bot.leave_chat(m.chat.id)
            return
        if not chat[8]:
            return

    if m.from_user.id == 777000:
        if not chat[14]:
            return
        channel_id = m.forward_from_chat.id
        m_id = m.forward_from_message_id
        chat_id = str(m.chat.id)[4:]
        post = get_post(channel_id, m_id)
        if not post:
            return
        keyboard = types.InlineKeyboardMarkup()
        if post[3] == 'None':
            return
        else:
            react = eval(post[3])
            """react_spl = post[3].split('\n')
            for i in range(len(react_spl)):
                react.append([])
                for j in react_spl[i].split('|'):
                    react[i].append(j)"""
            for i in range(len(react)):
                keyboard.keyboard.append([])
                for j in range(len(react[i])):
                    keyboard.keyboard[i].append(types.InlineKeyboardButton(f'{react[i][j]} 0',
                                                                           callback_data=f'react_{i}_{j}'))
        but = types.InlineKeyboardButton(text='💬 Коментарі', url=f'https://t.me/c/{chat_id}/1?thread={m.message_id}')
        keyboard.add(but)
        bot.edit_message_reply_markup(channel_id, m_id, reply_markup=keyboard)


@bot.channel_post_handler()
def channel_handler(m):
    channel = get_channel(m.chat.id)
    if not channel:
        admins = [0, 0]
        cr = 0
        for j in bot.get_chat_administrators(m.chat.id):
            user = j.user
            if j.status == 'creator':
                cr = user.id
            else:
                if not get_user(user.id):
                    continue
            admins.append(user.id)
        # admins.remove(BOT_USER)
        admins = list(map(lambda x: str(x), admins))
        if cr:
            new_channel(m.chat, 'Приватний', cr, admins)
            keyboard = types.InlineKeyboardMarkup()
            but = types.InlineKeyboardButton(text='До меню Простору Ячмінії',
                                             callback_data='prostir_menu')
            keyboard.add(but)
            try:
                bot.send_message(cr, f'Канал {m.chat.title} доданий до приватного Простору Ячмінії. '
                                     f'Для коректної роботи бота ви маєте ввімкнути бота в меню'
                                     f'Простору Ячмінії. Якщо виникли проблеми, '
                                     f'зверніться до {user_link(CREATOR, "Назарія фон Герсте")}.',
                                 reply_markup=keyboard, parse_mode='HTML')
            except:
                pass
        else:
            bot.leave_chat(m.chat.id)
            return

    """if m.chat.id == -1001227651426:
        if m.text.lower() == 'ввімкнути захист':
            script_on_func()
        elif m.text.lower() == 'вимкнути захист':
            script_off_func()
        elif m.text.lower() == 'ввімкнути захист тест':
            script_on_func(True)
        elif m.text.lower() == 'вимкнути захист тест':
            script_off_func(True)"""


def main():
    while True:
        try:
            bot.polling()
        except Exception:
            t = StringIO()
            print_exc(file=t)
            t = html(t.getvalue())
            link = 'telegra.ph/file/84f9fe5ef05fa6c9edf80.png'
            out = f'<a href="{link}">{chr(8205)}</a>@yachminiya_test_bot:\n{t}'
            bot.send_message(419596848, out, parse_mode='HTML')
            main()


if __name__ == '__main__':
    main()
