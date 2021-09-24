from config import *
from datetime import datetime
import sql_obj
from tables import *
from threading import Timer


done_operation = True
global_insert_queue = 0
dbname = ":memory:"
"""
try:
    path = os.path.join(os.path.abspath(os.path.dirname(__file__)), dbname)
    os.remove(dbname)
except:
    pass
"""
db = sql_obj.DB(dbname)


########################################################################################################################

db.insert(table_users)
db.insert(table_passports)
db.insert(table_chats)
db.insert(table_channels)
db.insert(table_admin)
db.insert(table_sans)
db.insert(table_businesses)
db.insert(table_rids)
db.insert(table_meta)
db.insert(table_institutions)
db.insert(table_zhandarmeria)
db.insert(table_graphstvo)
db.insert(table_bank)
db.insert(table_posts)


########################################################################################################################


def get_values_g(range_in):
    '''Функція для отримання даних з таблиці.
    Вхідними даними є діапазон вирізання, вихідними — список у списку'''
    global done_operation
    while True:
        if done_operation:
            done_operation = False
            values = service.spreadsheets().values().get(
                spreadsheetId=spreadsheet_id,
                range=range_in,
                majorDimension='ROWS'
            ).execute()['values']
            done_operation = True
            break
    for i in range(len(values)):
        for j in range(len(values[i])):
            try:
                values[i][j] = int(values[i][j])
            except:
                pass
    return values


def get_values_v(range_in):
    '''Функція для отримання даних з таблиці.
    Вхідними даними є діапазон вирізання, вихідними — список у списку'''
    global done_operation
    while True:
        if done_operation:
            done_operation = False
            values = service.spreadsheets().values().get(
                spreadsheetId=spreadsheet_id,
                range=range_in,
                majorDimension='COLUMNS'
            ).execute()['values']
            done_operation = True
            break
    for i in range(len(values)):
        for j in range(len(values[i])):
            try:
                values[i][j] = int(values[i][j])
            except:
                pass
    return values


########################################################################################################################


def update_all_users():
    users = get_values_g('users!A7:M')
    db.insert_many(f'''
    insert into users 
    values 
    (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''', tuple(map(lambda x: tuple(x), users)))


def update_all_passports():
    passports = get_values_g('passports!A7:Y')
    db.insert_many(f'''
        insert into passports 
        values 
        (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''', tuple(map(lambda x: tuple(x), passports)))


def update_all_chats():
    chats = get_values_g('chats!A7:O')
    db.insert_many(f'''
        insert into chats 
        values 
        (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''', tuple(map(lambda x: tuple(x), chats)))


def update_all_channels():
    channels = get_values_g('channels!A7:I')
    db.insert_many(f'''
        insert into channels
        values 
        (?, ?, ?, ?, ?, ?, ?, ?, ?)''', tuple(map(lambda x: tuple(x), channels)))


def update_all_admin():
    admin = get_values_g('admin!A7:C')
    db.insert_many(f'''
        insert into admin 
        values 
        (?, ?, ?)''', tuple(map(lambda x: tuple(x), admin)))


def update_all_sans():
    sans = get_values_g('sans!A7:E')
    db.insert_many(f'''
        insert into sans 
        values 
        (?, ?, ?, ?, ?)''', tuple(map(lambda x: tuple(x), sans)))


def update_all_businesses():
    businesses = get_values_g('businesses!A7:J')
    db.insert_many(f'''
        insert into businesses 
        values 
        (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''', tuple(map(lambda x: tuple(x), businesses)))


def update_all_rids():
    rids = get_values_g('rids!A7:F')
    db.insert_many(f'''
        insert into rids 
        values 
        (?, ?, ?, ?, ?, ?)''', tuple(map(lambda x: tuple(x), rids)))


def update_all_meta():
    meta = get_values_g('meta!A7:C')
    db.insert_many(f'''
            insert into meta 
            values 
            (?, ?, ?)''', tuple(map(lambda x: tuple(x), meta)))


def update_all_institutions():
    institutions = get_values_g('institutions!A7:I')
    db.insert_many(f'''
            insert into institutions 
            values 
            (?, ?, ?, ?, ?, ?, ?, ?, ?)''', tuple(map(lambda x: tuple(x), institutions)))


def update_all_zhandarmeria():
    zhandarmeria = get_values_g('zhandarmeria!A7:E')
    db.insert_many(f'''
            insert into zhandarmeria 
            values 
            (?, ?, ?, ?, ?)''', tuple(map(lambda x: tuple(x), zhandarmeria)))


def update_all_graphstvo():
    graphstvo = get_values_g('graphstvo!A7:E')
    db.insert_many(f'''
            insert into graphstvo 
            values 
            (?, ?, ?, ?, ?)''', tuple(map(lambda x: tuple(x), graphstvo)))


def update_all_bank():
    bank = get_values_g('bank!A7:E')
    db.insert_many(f'''
            insert into bank 
            values 
            (?, ?, ?, ?, ?)''', tuple(map(lambda x: tuple(x), bank)))


def update_all_posts():
    posts = get_values_g('posts!A7:E')
    db.insert_many(f'''
            insert into posts
            values 
            (?, ?, ?, ?, ?)''', tuple(map(lambda x: tuple(x), posts)))


########################################################################################################################


update_all_users()
update_all_passports()
update_all_chats()
update_all_channels()
update_all_admin()
update_all_sans()
update_all_businesses()
update_all_rids()
update_all_meta()
update_all_institutions()
update_all_zhandarmeria()
update_all_graphstvo()
update_all_bank()
update_all_posts()


########################################################################################################################


def update_all_db():
    db.insert('''drop table users''')
    db.insert('''drop table passports''')
    db.insert('''drop table chats''')
    db.insert('''drop table channels''')
    db.insert('''drop table admin''')
    db.insert('''drop table sans''')
    db.insert('''drop table businesses''')
    db.insert('''drop table rids''')
    db.insert('''drop table meta''')
    db.insert('''drop table institutions''')
    db.insert('''drop table zhandarmeria''')
    db.insert('''drop table graphstvo''')
    db.insert('''drop table bank''')
    db.insert('''drop table posts''')

    db.insert(table_users)
    db.insert(table_passports)
    db.insert(table_chats)
    db.insert(table_channels)
    db.insert(table_admin)
    db.insert(table_sans)
    db.insert(table_businesses)
    db.insert(table_rids)
    db.insert(table_meta)
    db.insert(table_institutions)
    db.insert(table_zhandarmeria)
    db.insert(table_graphstvo)
    db.insert(table_bank)
    db.insert(table_posts)

    update_all_users()
    update_all_passports()
    update_all_chats()
    update_all_channels()
    update_all_admin()
    update_all_sans()
    update_all_businesses()
    update_all_rids()
    update_all_meta()
    update_all_institutions()
    update_all_zhandarmeria()
    update_all_graphstvo()
    update_all_bank()
    update_all_posts()


def name(user):
    """Повертає ім'я або ім'я та прізвище. ПРІЗВИЩА САСАААААТЬ"""
    if user.last_name is not None:
        return f'{user.first_name} {user.last_name}'
    return user.first_name


def insert_values(range_in, values_in, horizontal):
    """
    Функція для внесення даних у таблицю.
    Вхідними даними є діапазон внесення та дані для внесення. Вихідних даних нема
    """
    global done_operation, global_insert_queue
    if horizontal:
        dim = 'ROWS'
    else:
        dim = 'COLUMNS'
    while True:
        if done_operation:
            done_operation = False
            values = service.spreadsheets().values().batchUpdate(
                spreadsheetId=spreadsheet_id,
                body={
                    "valueInputOption": "USER_ENTERED",
                    "data": [
                        {"range": range_in,
                         "majorDimension": dim,
                         "values": values_in}
                    ]
                }
            ).execute()
            done_operation = True
            break
    if not global_insert_queue:
        global_insert_queue -= 1
    # return values


def insert_values_v(range_in, values_in):
    global global_insert_queue
    global_insert_queue += 1
    if global_insert_queue < 7:
        q_in = 0
    else:
        q_in = global_insert_queue - 6
    Timer(q_in, insert_values, args=(range_in, values_in, False)).start()


def insert_values_h(range_in, values_in):
    global global_insert_queue
    global_insert_queue += 1
    if global_insert_queue < 7:
        q_in = 0
    else:
        q_in = global_insert_queue - 6
    Timer(q_in, insert_values, args=(range_in, values_in, True)).start()


def test_new_timer(bot, m):
    global global_insert_queue
    bot.send_message(m.chat.id, 'хуй')
    global_insert_queue -= 1


def test_new_timer_pre(bot, m):
    global global_insert_queue
    global_insert_queue += 1
    if global_insert_queue < 7:
        q_in = 0
    else:
        q_in = global_insert_queue - 6
    Timer(q_in, test_new_timer, args=(bot, m)).start()


def clear_range(range_in):
    '''очищує діапазон'''
    global done_operation
    while True:
        if done_operation:
            done_operation = False
            values = service.spreadsheets().values().batchClear(
                spreadsheetId=spreadsheet_id,
                body={
                    'ranges': [range_in]}
            ).execute()
            done_operation = True
            break
    return


def new_passport(u, namep, surname, sex, acc_name, acc_surname):
    amount = get_amount_of_passports()
    date = str(datetime.now())[:-7]
    if u.username is None:
        u_username = 'None'
    else:
        u_username = u.username
    passport = [amount + 1, f'{u.id}', namep, surname, name(u),
                u_username, sex, date, 'Без сану', 0, 'Початковий', 0,
                '0 0 0 0 0', 'Самітник', 0, '0 0', acc_name, acc_surname]
    db.insert('''
    INSERT INTO passports
    (num, id, name, surname, nickname, tag, sex, date_create, san, balance, status, bill, rights, rid, rid_welc, work, acc_name, acc_surname, ident_code, reputation, rep_cooldown, msg_am, word_am, week_mag_am, week_word_am)
    VALUES 
    (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', tuple(passport))
    insert_values_h(f"passports!A{7 + amount}:Y{7 + amount}", [passport])


def new_user(u):
    amount = get_amount_of_users()
    if u.username is None:
        u_username = 'None'
    else:
        u_username = u.username
    user = [amount+1, u.id, name(u), 0, 0, u_username, '0 0 0 0 0 0 0 0 0 0', 0, 0, '0 0 1 2', '0 0 1 2 3 4 5 6 8', '0 0 0 0 0 0 0', '0 0 0 0 0 0 0']
    db.insert('''
    INSERT INTO users
    (num, id, name, rep, repcool, tag, rights, mess_amount, word_amount, chats, channels, mess_week, words_week)
    VALUES 
    (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', tuple(user))
    insert_values_h(f"users!A{7 + amount}:M{7 + amount}", [user])


def new_rid(u, namep, n):
    amount = get_amount_of_rids()
    rid = [amount + 1, namep, u.id, '0 0', 0, n]
    db.insert('''
    INSERT INTO rids
    (num, name, owner, members, assets, ch_num)
    VALUES 
    (?, ?, ?, ?, ?, ?)
    ''', tuple(rid))
    insert_values_h(f'rids!A{7 + amount}:F', rid)


def new_chat(chat, type_ch, owner, admins):
    amount = len(get_all_chats())
    chat_in = [amount + 1, chat.id, chat.title, 'None', 'NoneURL', "None", type_ch, owner, 0, "None", "None", "None",
               "None", ' '.join(admins), 0]
    db.insert('''
        INSERT INTO chats
        (num, id, name, welcome, link, open_img, type_ch, owner, is_on, rep_up, rep_down, trigers, trig_text, admins, 
        linked_channel)
        VALUES 
        (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', tuple(chat_in))
    insert_values_h(f'chats!A{amount + 7}:O{amount + 7}', [chat_in])


def new_channel(channel, type_ch, owner, admins):
    amount = len(get_all_channels())
    channel_in = [amount + 1, channel.id, channel.title, 'None', type_ch, owner, 0, ' '.join(admins), 0]
    db.insert('''
        INSERT INTO channels
        (num, id, name, link, type_ch, owner, is_on, admins, linked_chat)
        VALUES 
        (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', tuple(channel_in))
    insert_values_h(f'channels!A{amount + 7}:I{amount + 7}', [channel_in])


def new_business(u, namep, n, tag, about):
    amount = get_amount_of_businesses()
    business = [amount+1, tag, namep, u.id, 0, '0 0', '0 0', n, 0, about]
    db.insert('''
    INSERT INTO businesses
    (num, tag, name, owner, assets, employers, employers_bills, ch_num, financing, rid)
    VALUES 
    (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', tuple(business))
    insert_values_h(f'rids!A{7 + amount}:J', business)


def new_zhan(u):
    amount = get_amount_of_zhans()
    zhan = [amount + 1, u.id, 'Новобранець', 0, 0]
    db.insert('''
    INSERT INTO zhandarmeria
    (num, id, name, amount_of_st, amount_of_st_period)
    VALUES 
    (?, ?, ?, ?, ?)
    ''', tuple(zhan))
    insert_values_h(f"zhandarmeria!A{7 + amount}:E", [zhan])


def new_erl(u):
    amount = get_amount_of_erls()
    erl = [amount + 1, u.id, 'Віконт', 0, 0]
    db.insert('''
    INSERT INTO graphstvo
    (num, id, name, amount_of_doings, amount_of_doings_period)
    VALUES 
    (?, ?, ?, ?, ?)
    ''', tuple(erl))
    insert_values_h(f"graphstvo!A{7 + amount}:E", [erl])


def new_karb(u):
    amount = get_amount_of_karbs()
    karb = [amount + 1, u.id, 'Карб', 0, 0]
    db.insert('''
    INSERT INTO bank
    (num, id, name, amount_of_zvits, amount_of_zvits_period)
    VALUES 
    (?, ?, ?, ?, ?)
    ''', tuple(karb))
    insert_values_h(f"bank!A{7 + amount}:E", [karb])


def new_post(ch_id, m_id, react, votes):
    amount = get_amount_of_posts()
    post = [amount+1, ch_id, m_id, react, votes]
    db.insert('''
    INSERT INTO posts
    (num, ch_id, m_id, react, votes)
    VALUES 
    (?, ?, ?, ?, ?)
    ''', tuple(post))
    insert_values_h(f"posts!A{7 + amount}:E", [post])


def insert_user_l(user):
    # user.append(user[1])
    db.insert('''
    UPDATE users
    SET num = ?,
id = ?,
name = ?,
rep = ?,
repcool = ?,
tag = ?,
rights = ?,
mess_amount = ?,
word_amount = ?,
chats = ?,
channels = ?,
mess_week = ?,
words_week = ?
    WHERE 
    id = ?
    ''', user + [user[1]])


def insert_user_g(user):
    insert_values_h(f'users!A{6 + int(user[0])}:M{6 + int(user[0])}', [user])


def insert_user_a(user):
    insert_user_l(user)
    insert_user_g(user)


def insert_passport_l(passport):
    db.insert('''
    UPDATE passports
    SET num = ?,
id = ?,
name = ?,
surname = ?,
nickname = ?,
tag = ?,
sex = ?,
date_create = ?,
san = ?,
balance = ?,
status = ?,
bill = ?,
rights = ?,
rid = ?,
rid_welc = ?,
work = ?,
acc_name = ?,
acc_surname = ?,
ident_code = ?,
reputation = ?,
rep_cooldown = ?,
msg_am = ?,
word_am = ?,
week_msg_am = ?,
week_word_am = ?
    WHERE 
    id = ?
    ''', passport + [passport[1]])


def insert_passport_g(passport):
    insert_values_h(f'passports!A{6 + int(passport[0])}:Y{6 + int(passport[0])}', [passport])


def insert_passport_a(passport):
    insert_passport_l(passport)
    insert_passport_g(passport)


def insert_chat_l(chat):
    db.insert('''
    UPDATE chats
    SET num = ?,
id = ?,
name = ?,
welcome = ?,
link = ?,
open_img = ?,
type_ch = ?,
owner = ?,
is_on = ?,
rep_up = ?,
rep_down = ?,
trigers = ?,
trig_text = ?,
admins = ?,
linked_channel = ?
    WHERE 
    id = ?
    ''', chat + [chat[1]])


def insert_chat_g(chat):
    insert_values_h(f'chats!A{6 + chat[0]}:O{6 + chat[0]}', [chat])


def insert_chat_a(chat):
    insert_chat_l(chat)
    insert_chat_g(chat)


def insert_channel_l(channel):
    db.insert('''
    UPDATE channels
    SET num = ?,
id = ?,
name = ?,
link = ?,
type_ch = ?,
owner = ?,
is_on = ?,
admins = ?,
linked_chat = ?
    WHERE 
    id = ?
    ''', channel + [channel[1]])


def insert_channel_g(channel):
    insert_values_h(f'channels!A{6 + channel[0]}:I{6 + channel[0]}', [channel])


def insert_channel_a(channel):
    insert_channel_l(channel)
    insert_channel_g(channel)


def insert_business_l(business):
    db.insert('''
    UPDATE businesses
    SET num = ?,
tag = ?,
name = ?,
owner = ?,
assets = ?,
employers = ?,
employers_bills = ?,
ch_num = ?,
financing = ?,
rid = ?
    WHERE 
    num = ?
    ''', business + [business[0]])


def insert_business_g(business):
    insert_values_h(f'businesses!A{6 + int(business[0])}:J{6 + int(business[0])}', [business])


def insert_business_a(business):
    insert_business_l(business)
    insert_business_g(business)


def insert_rid_l(rid):
    db.insert('''
    UPDATE rids
    SET num = ?,
tag = ?,
name = ?,
owner = ?,
members = ?,
assets = ?,
ch_num = ?
    WHERE 
    num = ?
    ''', rid + [rid[0]])


def insert_rid_g(rid):
    insert_values_h(f'rids!A{6 + int(rid[0])}:F{6 + int(rid[0])}', [rid])


def insert_rid_a(rid):
    insert_rid_l(rid)
    insert_rid_g(rid)


def insert_institution_l(institution):
    db.insert('''
    UPDATE institutions
    SET num = ?,
name = ?,
genitive_name = ?,
assets = ?,
last_decree = ?,
decree_img_link = ?,
owner = ?,
report_date = ?,
ch_num = ?
    WHERE name = ?
    ''', institution + [institution[1]])


def insert_institution_g(institution):
    insert_values_h(f'institutions!A{6 + int(institution[0])}:I{6 + int(institution[0])}', [institution])


def insert_institution_a(institution):
    insert_institution_l(institution)
    insert_institution_g(institution)


def insert_zhan_l(zhan):
    db.insert('''
    UPDATE zhandarmeria
    SET num = ?,
id = ?,
name = ?,
amount_of_st = ?,
amount_of_st_period = ?
    WHERE id = ?
    ''', zhan + [zhan[1]])


def insert_zhan_g(zhan):
    insert_values_h(f'zhandarmeria!A{6 + int(zhan[0])}:E{6 + int(zhan[0])}', [zhan])


def insert_zhan_a(zhan):
    insert_zhan_l(zhan)
    insert_zhan_g(zhan)


def insert_erl_l(erl):
    db.insert('''
    UPDATE graphstvo
    SET num = ?,
id = ?,
name = ?,
amount_of_doings = ?,
amount_of_doings_period = ?
    WHERE id = ?
    ''', erl + [erl[1]])


def insert_erl_g(erl):
    insert_values_h(f'graphstvo!A{6 + int(erl[0])}:E{6 + int(erl[0])}', [erl])


def insert_erl_a(erl):
    insert_erl_l(erl)
    insert_erl_g(erl)


def insert_karb_l(karb):
    db.insert('''
    UPDATE bank
    SET num = ?,
id = ?,
name = ?,
amount_of_zvits = ?,
amount_of_zvits_period = ?
    WHERE id = ?
    ''', karb + [karb[1]])


def insert_karb_g(karb):
    insert_values_h(f'bank!A{6 + int(karb[0])}:E{6 + int(karb[0])}', [karb])


def insert_karb_a(karb):
    insert_karb_l(karb)
    insert_karb_g(karb)


def insert_post_l(post):
    db.insert('''
    UPDATE posts
    SET num = ?,
ch_id = ?,
m_id = ?,
react = ?,
votes = ?
    WHERE ch_id = ? and m_id = ?
    ''', post + [post[1], post[2]])


def insert_post_g(post):
    insert_values_h(f'posts!A{6 + int(post[0])}:E{6 + int(post[0])}', [post])


def insert_post_a(post):
    insert_post_l(post)
    insert_post_g(post)


def get_all_users():
    users = map(lambda x: list(x), db.get('''
    select *
    from users'''))
    return list(users)


def get_all_users_rep_order():
    users = map(lambda x: list(x), db.get('''
    select *
    from users
    order by rep'''))
    return list(users)


def get_all_passports():
    passports = map(lambda x: list(x), db.get('''
    select *
    from passports'''))
    return list(passports)


def get_all_chats(ident=0):
    if ident:
        text_in = f' where owner = {ident}'
    else:
        text_in = ''
    chats = map(lambda x: list(x), db.get(f'''
    select *
    from chats{text_in}'''))
    return list(chats)


def get_all_channels(ident=0):
    if ident:
        text_in = f' where owner = {ident}'
    else:
        text_in = ''
    channels = map(lambda x: list(x), db.get(f'''
    select *
    from channels{text_in}'''))
    return list(channels)


def get_all_admin():
    admin = map(lambda x: list(x), db.get('''
    select *
    from admin'''))
    return list(admin)


def get_all_sans():
    sans = map(lambda x: list(x), db.get('''
    select *
    from sans'''))
    return list(sans)


def get_all_businesses():
    businesses = map(lambda x: list(x), db.get('''
    select *
    from businesses'''))
    return list(businesses)


def get_all_rids():
    rids = map(lambda x: list(x), db.get('''
    select *
    from rids'''))
    return list(rids)


def get_all_meta():
    meta = map(lambda x: list(x), db.get('''
    select *
    from meta'''))
    return list(meta)


def get_all_institutions():
    institutions = map(lambda x: list(x), db.get('''
    select *
    from institutions'''))
    return list(institutions)


def get_all_zhandarmeria():
    zhandarmeria = map(lambda x: list(x), db.get('''
        select *
        from zhandarmeria'''))
    return list(zhandarmeria)


def get_all_graphstvo():
    graphstvo = map(lambda x: list(x), db.get('''
        select *
        from graphstvo'''))
    return list(graphstvo)


def get_all_bank():
    bank = map(lambda x: list(x), db.get('''
        select *
        from bank'''))
    return list(bank)


def get_all_posts():
    posts = map(lambda x: list(x), db.get('''
        select *
        from posts'''))
    return list(posts)


def get_user(ident):
    try:
        user = list(db.get('''
        SELECT * 
        FROM users
        WHERE id = ?''', (ident, ))[0])
    except:
        return None
    return user


def get_passport(ident):
    passport = db.get('''
    SELECT * 
    FROM passports
    WHERE id = ?''', (ident, ))
    if passport:
        passport = list(passport[0])
    else:
        passport = db.get('''
            SELECT * 
            FROM passports
            WHERE ident_code = ?''', (ident,))
        if passport:
            passport = list(passport[0])
        else:
            return None
    return passport


def get_chat(ident):
    chat = db.get('''
    SELECT * 
    FROM chats
    WHERE id = ?''', (ident, ))
    if chat:
        chat = list(chat[0])
    else:
        return None
    return chat


def get_channel(ident):
    channel = db.get('''
    SELECT * 
    FROM channels
    WHERE id = ?''', (ident, ))
    if channel:
        channel = list(channel[0])
    else:
        return None
    return channel


def get_institution(name):
    try:
        institution = list(db.get('''
        SELECT * 
        FROM institutions
        WHERE name = ?''', (name, ))[0])
    except:
        return None
    return institution


def get_zhan(ident):
    try:
        zhan = list(db.get('''
        SELECT * 
        FROM zhandarmeria
        WHERE id = ?''', (ident, ))[0])
    except:
        return None
    return zhan


def get_erl(ident):
    try:
        erl = list(db.get('''
        SELECT * 
        FROM graphstvo
        WHERE id = ?''', (ident, ))[0])
    except:
        return None
    return erl


def get_karb(ident):
    try:
        karb = list(db.get('''
        SELECT * 
        FROM bank
        WHERE id = ?''', (ident, ))[0])
    except:
        return None
    return karb


def get_sans(values):
    ins = ('?, ' * len(values))[:-2]
    sql = f'''
select *
from sans
where name in ({ins})'''
    sans = map(lambda x: list(x), db.get(sql, values))
    return list(sans)


def get_business_id(ident):
    try:
        business = list(db.get('''
        SELECT * 
        FROM businesses
        WHERE tag = ?''', (ident, ))[0])
    except:
        return None
    return business


def get_business_name(ident):
    try:
        business = list(db.get('''
        SELECT * 
        FROM businesses
        WHERE name = ?''', (ident, ))[0])
    except:
        return None
    return business


def get_business_owner(values):
    ins = ('?, '*len(values))[:-2]
    business = list(map(lambda x: list(x), (db.get(f'''
            SELECT * 
            FROM businesses
            WHERE owner in ({ins})''', values))))
    return business


def get_rid(ident):
    try:
        rid = list(db.get('''
        SELECT * 
        FROM rids
        WHERE name = ?''', (ident, ))[0])
    except:
        return None
    return rid


def get_post(c, m):
    try:
        post = list(db.get('''
        SELECT * 
        FROM posts
        WHERE ch_id = ? and m_id = ?''', (c, m))[0])
    except:
        return None
    return post


def get_amount_of_passports():
    passports = get_all_passports()
    amount = len(passports)
    return amount


def get_petition_last():
    return get_all_meta()[0][1]


def insert_petition_last(amount):
    db.insert('''
            insert into meta
            (petition_last)
            values 
            (?)
            ''', (amount,))
    insert_values_h('meta!B7:B7', [[amount]])


def insert_day_meta(amount):
    db.insert('''
            insert into meta
            (month_day)
            values 
            (?)
            ''', (amount,))
    insert_values_h('meta!A7:A7', [[amount]])


def get_amount_of_users():
    users = get_all_users()
    amount = len(users)
    return amount


def get_amount_of_rids():
    rids = get_all_rids()
    amount = len(rids)
    return amount


def get_amount_of_businesses():
    businesses = get_all_businesses()
    amount = len(businesses)
    return amount


def get_amount_of_zhans():
    zhans = get_all_zhandarmeria()
    amount = len(zhans)
    return amount


def get_amount_of_erls():
    erls = get_all_graphstvo()
    amount = len(erls)
    return amount


def get_amount_of_karbs():
    karbs = get_all_bank()
    amount = len(karbs)
    return amount


def get_amount_of_posts():
    posts = get_all_posts()
    amount = len(posts)
    return amount


def del_table_passports():
    db.insert('''drop table passports''')


def insert_all_passports_l(passports):
    db.insert_many(f'''
            insert into passports 
            values 
            (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''', tuple(map(lambda x: tuple(x), passports)))


def insert_all_passports_g(passports):
    insert_values_h('passports!A7:Y', passports)


def del_passport_g(all_passports, amount):
    insert_values_h('passports!A7:Y', all_passports)
    clear_range(f'passports!A{6+amount}:Y{6+amount}')


def del_table_businesses():
    db.insert('''drop table businesses''')


def insert_all_businesses_l(businesses):
    db.insert_many(f'''
            insert into businesses 
            values 
            (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''', tuple(map(lambda x: tuple(x), businesses)))


def insert_all_businesses_g(businesses):
    insert_values_h('businesses!A7:J', businesses)


def del_business_g(all_businesses, amount):
    insert_values_h('businesses!A7:J', all_businesses)
    clear_range(f'businesses!A{6+amount}:J{6+amount}')


def del_table_zhandarmeria():
    db.insert('''drop table zhandarmeria''')


def insert_all_zhandarmeria_l(zhandarmeria):
    db.insert_many(f'''
            insert into zhandarmeria 
            values 
            (?, ?, ?, ?, ?)''', tuple(map(lambda x: tuple(x), zhandarmeria)))


def insert_all_zhandarmeria_g(zhandarmeria):
    insert_values_h('zhandarmeria!A7:E', zhandarmeria)


def del_zhan_g(all_zhans, amount):
    insert_values_h('zhandarmeria!A7:E', all_zhans)
    clear_range(f'zhandarmeria!A{7+amount}:E{7+amount}')


def del_table_graphstvo():
    db.insert('''drop table graphstvo''')


def insert_all_graphstvo_l(graphstvo):
    db.insert_many(f'''
            insert into graphstvo 
            values 
            (?, ?, ?, ?, ?)''', tuple(map(lambda x: tuple(x), graphstvo)))


def insert_all_graphstvo_g(graphstvo):
    insert_values_h('graphstvo!A7:E', graphstvo)


def del_erl_g(all_erls, amount):
    insert_values_h('graphstvo!A7:E', all_erls)
    clear_range(f'graphstvo!A{7+amount}:E{7+amount}')


def del_table_bank():
    db.insert('''drop table bank''')


def insert_all_bank_l(bank):
    db.insert_many(f'''
            insert into bank 
            values 
            (?, ?, ?, ?, ?)''', tuple(map(lambda x: tuple(x), bank)))


def insert_all_bank_g(bank):
    insert_values_h('bank!A7:E', bank)


def del_karb_g(all_karbs, amount):
    insert_values_h('bank!A7:E', all_karbs)
    clear_range(f'bank!A{7+amount}:E{7+amount}')


"""def get():
    conn = sqlite3.connect(dbname)
    with conn:
        #conn.execute('''
        #CREATE TABLE User (
        #id NOT NULL PRIMARY KEY,
        #name TEXT
        #)
        #''')
        conn.execute('''
        UPDATE USER
        SET id = ?, name = ?
        WHERE 
        id = 0
        ''', [0, 'test'])
        t = conn.execute('''
        SELECT name 
        FROM user 
        WHERE id = 0
        ''').fetchall()[0][0]
    conn.close()
    return t


def new_table():
    conn = sqlite3.connect(dbname)
    try:
        with conn:
            conn.execute('''
            CREATE TABLE passports (
            num NOT NULL PRIMARY KEY,
            id not null,
            name TEXT,
            sex text,
            time text,
            san text,
            status text
            )
            ''')
        out = 'Таблиця успішно створена'
    except:
        out = 'Пішов нахуй, я вже створив таблицю'
    conn.close()
    return out"""

