import time

reputation = {'хвала', 'шана', 'дяка', 'аве', 'уу', 'хвала!', 'шана!', 'дяка!', 'аве!', 'уу!', 'хвала.', 'шана.',
              'дяка.', 'аве.', 'уу.'}
bad_reputation = {'зневага', 'ганьба', 'зневага!', 'ганьба!', 'зневага.', 'ганьба.'}
queue = [0, 0, 0]
t_queue = time.time()
aktyv = {}
lakt = 0
zhandarm = 0
voting_q = set()
welcome_m = {}
del_pass = 0
queue_call = [0, 0, 0]
t_queue_call = time.time()
weekdays = {'понеділок': (0, 'понеділок', 'Понеділкова'), 'вівторок': (1, 'вівторок', 'Вівторкова'),
            'середа': (2, 'середу', 'Середова'), 'четвер': (3, 'четвер', 'Четвергова'),
            "п'ятниця": (4, "п'ятницю", "П'ятнична"), 'субота': (5, 'суботу', 'Суботня'),
            'неділя': (6, 'неділю', 'Недільна')}
business_seans = {}
thrash = -1001453786861
pass_form = '''
Уважно заповніть форму перед надсиланням. Скопіюйте форму і вписуйте дані уже в неї, це важливо. Ім'я і прізвище можуть бути вигадані.

(натисніть на форму, і вона скопіюється)
<code>Форма для оформлення громадянства
Ім'я: 
Прізвище: 
Стать: Чоловіча/Жіноча
</code>
'''
business_form = '''
Уважно заповніть форму перед надсиланням. Скопіюйте форму і вписуйте дані уже в неї, це важливо.
Тег записуйте у форматі <code>TAG</code>. У тегу можна використовувати тільки великі латинські літери, числа та нижні підкреслювання.

Якщо ви хочете відмінити процедуру реєстрації, напишіть <code>СТОП</code>

(натисніть на форму, і вона скопіюється)
<code>Форма для власної справи
Назва: 
Тег: 
Рід діяльності: .
</code>
'''
alphabet = "йцукенгшщзхїфівапролджєячсмитьбюґ-()'`"
mes = ''