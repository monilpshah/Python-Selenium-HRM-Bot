from __future__ import print_function
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from google.oauth2 import service_account

SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
SERVICE_ACCOUNT_FILE = 'key.json'
credentials = None
credentials = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES)

# The ID and range of a sample spreadsheet.
SAMPLE_SPREADSHEET_ID = '199TtxUfqbgwrPfzfzvsC3zxwsn_TUJjW3Ahlh2LOH7Y'
SAMPLE_RANGE_NAME = 'Sheet1!A2:H3'

try:
    service = build('sheets', 'v4', credentials=credentials)
    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                                range=SAMPLE_RANGE_NAME).execute()
    values = result.get('values', [])
    # print(result)
    if not values:
        print('No data found.')


    print('Name, Major:')
    for row in values:
            # Print columns A and E, which correspond to indices 0 and 4.
            print('%s, %s' % (row[0], row[4]))
except HttpError as err:
    print(err)
