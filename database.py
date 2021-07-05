from config import *
from datetime import datetime
import sql_obj
import os


done_operation = True
dbname = "yachdatabase.sqlite"
try:
    path = os.path.join(os.path.abspath(os.path.dirname(__file__)), dbname)
    os.remove(dbname)
except:
    pass
db = sql_obj.DB(dbname)

########################################################################################################################


def update_all_users():
    users = get_values_g('users!A7:M')
    db.insert_many(f'''
    insert into users 
    values 
    (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''', tuple(map(lambda x: tuple(x), users)))


def update_all_passports():
    passports = get_values_g('passports!A7:P')
    db.insert_many(f'''
        insert into passports 
        values 
        (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''', tuple(map(lambda x: tuple(x), passports)))


def update_all_chats():
    chats = get_values_g('chats!A7:E')
    db.insert_many(f'''
        insert into chats 
        values 
        (?, ?, ?, ?, ?)''', tuple(map(lambda x: tuple(x), chats)))


def update_all_channels():
    channels = get_values_g('channels!A7:D')
    db.insert_many(f'''
        insert into channels
        values 
        (?, ?, ?, ?)''', tuple(map(lambda x: tuple(x), channels)))


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


########################################################################################################################


def name(user):
    """Повертає ім'я або ім'я та прізвище. ПРІЗВИЩА САСАААААТЬ"""
    if user.last_name is not None:
        return f'{user.first_name} {user.last_name}'
    return user.first_name


def insert_values_v(range_in, values_in):
    """Функція для внесення даних у таблицю.
    Вхідними даними є діапазон внесення та дані для внесення. Вихідних даних нема"""
    global done_operation
    while True:
        if done_operation:
            done_operation = False
            values = service.spreadsheets().values().batchUpdate(
                spreadsheetId=spreadsheet_id,
                body={
                    "valueInputOption": "USER_ENTERED",
                    "data": [
                        {"range": range_in,
                         "majorDimension": "COLUMNS",
                         "values": values_in}
                    ]
                }
            ).execute()
            done_operation = True
            break
    return values


def insert_values_g(range_in, values_in):
    """Функція для внесення даних у таблицю.
    Вхідними даними є діапазон внесення та дані для внесення. Вихідних даних нема"""
    global done_operation
    while True:
        if done_operation:
            done_operation = False
            values = service.spreadsheets().values().batchUpdate(
                spreadsheetId=spreadsheet_id,
                body={
                    "valueInputOption": "USER_ENTERED",
                    "data": [
                        {"range": range_in,
                         "majorDimension": "ROWS",
                         "values": values_in}
                    ]
                }
            ).execute()
            done_operation = True
            break
    return values


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


def new_passport(u, namep, surname, sex):
    amount = get_amount_of_passports()
    date = str(datetime.now())[:-7]
    if u.username is None:
        u_username = 'None'
    else:
        u_username = u.username
    passport = [amount + 1, f'{u.id}', namep, surname, name(u),
                u_username, sex, date, 'Без сану', 0, 'Початковий', 0,
                '0 0 0 0 0', 'Самітник', 0, '0 0']
    db.insert('''
    INSERT INTO passports
    (num, id, name, surname, nickname, tag, sex, date_create, san, balance, status, bill, rights, rid, rid_welc, work)
    VALUES 
    (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', tuple(passport))
    insert_values_g(f"passports!A{7 + amount}:P{7 + amount}", [passport])


def new_user(u):
    amount = get_amount_of_users()
    if u.username is None:
        u_username = 'None'
    else:
        u_username = u.username
    user = [amount+1, f'{u.id}', f'{name(u)}', 0, 0, u_username, '0 0 0 0 0 0 0 0 0 0', 0, 0, '0 0 1 2', '0 0 1 2 3 4 5 6 8', '0 0 0 0 0 0 0', '0 0 0 0 0 0 0']
    db.insert('''
    INSERT INTO users
    (num, id, name, rep, repcool, tag, rights, mess_amount, word_amount, chats, channels, mess_week, words_week)
    VALUES 
    (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', tuple(user))
    insert_values_g(f"users!A{7 + amount}:M{7 + amount}", [user])


def new_rid(u, namep, n):
    amount = get_amount_of_rids()
    rid = [amount + 1, namep, u.id, '0 0', 0, n]
    db.insert('''
    INSERT INTO rids
    (num, name, owner, members, assets, ch_num)
    VALUES 
    (?, ?, ?, ?, ?, ?)
    ''', tuple(rid))
    insert_values_g(f'rids!A{7 + amount}:F', rid)


def new_chat(chat):
    amount = len(get_all_chats())
    chat_in = [amount + 1, chat.title, chat.id, 'None', 'NoneURL']
    db.insert('''
        INSERT INTO chats
        (num, name, id, welcome, link)
        VALUES 
        (?, ?, ?, ?, ?)
        ''', tuple(chat_in))
    insert_values_g(f'AX{amount + 7}:BB{amount + 7}', [chat_in])


def new_business(u, namep, n, tag, about):
    amount = get_amount_of_businesses()
    business = [amount+1, tag, namep, u.id, 0, '0 0', '0 0', n, 0, about]
    db.insert('''
    INSERT INTO businesses
    (num, tag, name, owner, assets, employers, employers_bills, ch_num, financing, rid)
    VALUES 
    (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', tuple(business))
    insert_values_g(f'rids!A{7 + amount}:F', business)


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
    insert_values_g(f'users!A{6+int(user[0])}:M{6+int(user[0])}', [user])


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
work = ?
    WHERE 
    id = ?
    ''', passport + [passport[1]])


def insert_passport_g(passport):
    insert_values_g(f'passports!A{6+int(passport[0])}:P{6+int(passport[0])}', [passport])


def insert_passport_a(passport):
    insert_passport_l(passport)
    insert_passport_g(passport)


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
    tag = ?
    ''', business + [business[1]])


def insert_business_g(business):
    insert_values_g(f'businesses!A{6+int(business[0])}:J{6+int(business[0])}', [business])


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
ch_num = ?,
    WHERE 
    name = ?
    ''', rid + [rid[1]])


def insert_rid_g(rid):
    insert_values_g(f'rids!A{6+int(rid[0])}:F{6+int(rid[0])}', [rid])


def insert_rid_a(rid):
    insert_rid_l(rid)
    insert_rid_g(rid)


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


def get_all_chats():
    chats = map(lambda x: list(x), db.get('''
    select *
    from chats'''))
    return list(chats)


def get_all_channels():
    channels = map(lambda x: list(x), db.get('''
    select *
    from channels'''))
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
    try:
        passport = list(db.get('''
        SELECT * 
        FROM passports
        WHERE id = ?''', (ident, ))[0])
    except:
        return None
    return passport


def get_chat(ident):
    try:
        chat = list(db.get('''
        SELECT * 
        FROM chats
        WHERE id = ?''', (ident, ))[0])
    except:
        return None
    return chat


def get_sans(values):
    ins = ('?, ' * len(values))[:-2]
    sql = f'''
select *
from sans
where name in ({ins})'''
    print(sql)
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
    insert_values_g('meta!B7:B7', [[amount]])


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


def del_table_passports():
    db.insert('''drop table passports''')


def insert_all_passports_l(passports):
    db.insert_many(f'''
            insert into passports 
            values 
            (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''', tuple(map(lambda x: tuple(x), passports)))


def insert_all_passports_g(passports):
    insert_values_g('passports!A7:P', passports)


def del_passport_g(all_passports, amount):
    insert_values_g('passports!A7:P', all_passports)
    clear_range(f'passports!A{6+amount}:P{6+amount}')


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

