table_users = '''
CREATE TABLE IF NOT EXISTS users (
num INTEGER NOT NULL PRIMARY KEY UNIQUE,
id INTEGER,
name text,
rep integer,
repcool integer,
tag text,
rights text,
mess_amount integer,
word_amount integer,
chats text,
channels text,
mess_week text,
words_week text
)
'''

table_passports = '''
CREATE TABLE IF NOT EXISTS passports (
num INTEGER NOT NULL PRIMARY KEY UNIQUE,
id INTEGER,
name text,
surname text,
nickname text,
tag text,
sex text,
date_create text,
san text,
balance integer,
status text,
bill integer,
rights text,
rid text,
rid_welc integer,
work text
)
'''

table_chats = '''
CREATE TABLE IF NOT EXISTS chats (
num INTEGER NOT NULL PRIMARY KEY UNIQUE,
name text,
id integer,
welcome text,
link text
)
'''

table_channels = '''
CREATE TABLE IF NOT EXISTS channels (
num INTEGER NOT NULL PRIMARY KEY UNIQUE,
name text,
id integer,
link text
)
'''

table_admin = '''
CREATE TABLE IF NOT EXISTS admin (
num INTEGER NOT NULL PRIMARY KEY UNIQUE,
text text,
punishment integer
)
'''

table_sans = '''
CREATE TABLE IF NOT EXISTS sans (
num INTEGER NOT NULL PRIMARY KEY UNIQUE,
name text,
bill integer,
us_rights text,
pass_rights text
)
'''

table_businesses = '''
CREATE TABLE IF NOT EXISTS businesses (
num INTEGER NOT NULL PRIMARY KEY UNIQUE,
tag text,
name text,
owner integer,
assets integer,
employers text,
employers_bills text,
ch_num integer,
financing integer,
rid text
)
'''

table_rids = '''
CREATE TABLE IF NOT EXISTS rids (
num INTEGER NOT NULL PRIMARY KEY UNIQUE,
name text,
owner integer,
members text,
assets integer,
ch_num integer
)
'''

table_meta = '''
CREATE TABLE IF NOT EXISTS meta (
weekday text,
petition_last integer,
full_pass_amount integer
)
'''