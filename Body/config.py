import httplib2
from apiclient import discovery
from oauth2client.service_account import ServiceAccountCredentials


Token = '1875045403:AAF5-WPgN1ZmK6A1Pu-Cm3UpX19pYMs5OCA'
CREATOR = 419596848

CREDENTIALS_FILE = 'credentials.json'
spreadsheet_id = '1y7OBRqTqqLRtsNRYgsFKfcAtT0XDBWlAr_Pfo40OfmY'                    # авторизую сервісний акк
credentials = ServiceAccountCredentials.from_json_keyfile_name(
    CREDENTIALS_FILE,
    ['https://www.googleapis.com/auth/spreadsheets',
     'https://www.googleapis.com/auth/drive'])
httpAuth = credentials.authorize(httplib2.Http())
service = discovery.build('sheets', 'v4', http=httpAuth)

"""        if len(mess) == 1:
            word_vars = None
            day = False
            week = False
            am_n = 10
        elif len(mess) == 2:
            if mess[1].isdigit():
                word_vars = None
                am_n = int(mess[1])
                day = False
                week = False
            else:
                if mess[1].lower() == 'тиждень':
                    word_vars = 'тиждень'
                    day = False
                    week = True
                    am_n = 10
                else:
                    try:
                        word_vars = weekdays[mess[1].lower()]
                        day = True
                        week = False
                        am_n = 10
                    except:
                        bot.send_message(m.chat.id, 'Неправильний формат!')
                        return
        elif len(mess) == 3:
            if mess[1].isdigit():
                n = 1
                d = 2
            elif mess[2].isdigit():
                n = 2
                d = 1
            else:
                bot.send_message(m.chat.id, 'Неправильний формат!')
                return
            am_n = int(mess[n])
            if mess[d].lower() == 'тиждень':
                word_vars = 'тиждень'
                day = False
                week = True
            elif mess[d].lower() == 'сьогодні':
                word_vars = (datetime.today().weekday(), 'сьогодні')
                day = True
                week = False
            elif mess[d].lower() == 'вчора':
                day = datetime.today().weekday() - 1
                if day < 0:
                    day += 7
                word_vars = (day, 'вчора')
                day = True
                week = False
            elif mess[d].lower() == 'позавчора':
                day = datetime.today().weekday() - 2
                if day < 0:
                    day += 7
                word_vars = (day, 'позавчора')
                day = True
                week = False
            elif mess[d].lower() == 'завтра':
                time.sleep(0.2)
                bot.send_message(m.chat.id, 'Я, по твоєму, схожа на Вангу?')
                return
            elif mess[d].lower() == 'післязавтра':
                time.sleep(0.2)
                bot.send_message(m.chat.id, 'Ну це вже не лізе в жодні рамки. Що ти хочеш від мене?')
                return
            else:
                try:
                    word_vars = weekdays[mess[d].lower()]
                    day = True
                    week = False
                except:
                    bot.send_message(m.chat.id, 'Неправильний формат!')
                    return
        else:
            bot.send_message(m.chat.id, 'Неправильний формат!')
            return

        users = get_all_users()
        if am_n > len(users):
            am_n = len(users)
        elif am_n > 30:
            am_n = 30

        if week:
            msg_out = 'Найактивніші за тиждень\n'
            all_msgs = 0
            all_words = 0
            akt = []
            for i in range(len(users)):
                akt.append([users[i][2], 0, 0, 0, users[i][5]])
                for j in users[i][11].split():
                    all_msgs += int(j)
                    akt[i][1] += int(j)
                for j in users[i][12].split():
                    all_words += int(j)
                    akt[i][2] += int(j)
        elif day:
            msg_out = f'Найактивніші за {word_vars[1]}\n'
            all_msgs = 0
            all_words = 0
            akt = []
            for i in range(len(users)):
                akt.append([users[i][2], 0, 0, 0, users[i][5]])
                msg_list = users[i][11].split()
                word_list = users[i][12].split()
                all_msgs += int(msg_list[word_vars[0]])
                akt[i][1] = int(msg_list[word_vars[0]])
                all_words += int(word_list[word_vars[0]])
                akt[i][2] = int(word_list[word_vars[0]])
        else:
            msg_out = f'Найактивніші\n'
            all_msgs = 0
            all_words = 0
            akt = []
            for i in range(len(users)):
                akt.append([users[i][2], 0, 0, 0, users[i][5]])
                all_msgs += int(users[i][7])
                akt[i][1] = int(users[i][7])
                all_words += int(users[i][8])
                akt[i][2] = int(users[i][8])

        for i in range(len(users)):
            akt[i][3] = ((akt[i][1] / all_msgs) + (akt[i][2] / all_words)) * 50
        for i in range(len(users)):
            for j in range(i, len(users)):
                if akt[i][3] < akt[j][3]:
                    akt[i], akt[j] = akt[j], akt[i]
        long = False
        for i in range(am_n):
            buf = str(round(akt[i][3], 2))
            if len(buf) == 5:
                long = True
            if long:
                prob = ' '
            else:
                prob = ''
            if len(buf) == 3:
                ins = f'{prob}{buf}0'
            elif len(buf) == 4:
                ins = f'{prob}{buf}'
            else:
                ins = buf
            msg_out += f'<code>{ins}% </code><a href="t.me/{akt[i][4]}">{html(akt[i][0])}</a>\n'

        bot.send_message(m.chat.id, msg_out, parse_mode='HTML', disable_web_page_preview=True)
"""