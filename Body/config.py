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
