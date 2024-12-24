from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build

from config import config

# Path to your service account key file
GOOGLE_API_KEY_FILE = config['GOOGLE_API_KEY_FILE']

# Define the required scopes
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

# The ID of your Google Sheet (from its URL)
SHEET_ID = config['SHEET_ID']


class RowData:
    def __init__(self, date: str, odometer: str, amount: str, lpgPrice: str, pbPrice: str):
        self.date = date
        self.odometer = odometer
        self.amount = amount
        self.lpgPrice = lpgPrice
        self.pbPrice = pbPrice

    date: str
    odometer: str
    amount: str
    lpgPrice: str
    pbPrice: str


def find_last_row_index(service):
    result = (
        service.spreadsheets()
        .values()
        .get(spreadsheetId=SHEET_ID, range='Arkusz1!A:A')
        .execute()
    )
    rows = result.get("values", [])
    return len(rows)


def update_value(service, last_row_index, data: RowData):
    index = last_row_index + 1
    requests = [
        {
            "range": f"Arkusz1!A{index}:B{index}",
            "values": [[data.date, data.odometer]]
        },
        {
            "range": f"Arkusz1!D{index}:E{index}",
            "values": [[data.amount, data.lpgPrice]]
        },
        {
            "range": f"Arkusz1!G{index}",
            "values": [[data.pbPrice]]
        },
    ]

    body = {
        "valueInputOption": "USER_ENTERED",  # Use USER_ENTERED for formulas or RAW for plain text
        "data": requests
    }

    service.spreadsheets().values().batchUpdate(
        spreadsheetId=SHEET_ID,
        body=body
    ).execute()


def add_row(data: RowData):
    credentials = Credentials.from_service_account_file(GOOGLE_API_KEY_FILE, scopes=SCOPES)
    service = build('sheets', 'v4', credentials=credentials)

    last_row_index = find_last_row_index(service)
    update_value(service, last_row_index, data)




