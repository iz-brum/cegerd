# config.py

from dotenv import load_dotenv
import os

load_dotenv()

SENDER_EMAIL = os.environ.get('NAME_EMAIL')
SENDER_PASSWORD = os.environ.get('PASSWORD_EMAIL')
SPREADSHEET_ID = os.getenv('SPREADSHEET_ID')
CREDENTIALS_FILE = os.getenv('CREDENTIALS_FILE')
TOKEN_FILE = os.getenv('TOKEN_FILE')

SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
