# sheets.py

import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow # pip install google-auth-oauthlib
from googleapiclient.discovery import build # pip install --upgrade google-api-python-client
from googleapiclient.errors import HttpError
from alert.config import SPREADSHEET_ID, SCOPES, CREDENTIALS_FILE, TOKEN_FILE
from datetime import datetime, date
from unidecode import unidecode # pip install unidecode

def autenticar():
    creds = None
    
    if os.path.exists(TOKEN_FILE):
        creds = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)
    
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            try:
                creds.refresh(Request())
                with open(TOKEN_FILE, 'w') as token:
                    token.write(creds.to_json())
            except Exception as e:
                print(f"Erro ao atualizar token: {e}")
                creds = None
        else:
            try:
                flow = InstalledAppFlow.from_client_secrets_file(
                    CREDENTIALS_FILE, SCOPES)
                creds = flow.run_local_server(port=0)
                
                with open(TOKEN_FILE, 'w') as token:
                    token.write(creds.to_json())
            except Exception as e:
                print(f"Erro ao autenticar: {e}")
                creds = None    
    return creds

def adicionar_valores_na_pagina(creds, nome_pagina, novos_valores):  # Adicionado 'nome_pagina' como argumento
    try:
        service = build('sheets', 'v4', credentials=creds)
        sheet = service.spreadsheets()

        result = sheet.values().get(spreadsheetId=SPREADSHEET_ID, range=f"'{nome_pagina}'!A1").execute()
        valores_atuais = result.get('values', [])

        if not valores_atuais:
            valores_atuais = []

        valores_atuais.extend(novos_valores)

        valores_ordenados = sorted(valores_atuais, key=lambda x: unidecode(x[0]))

        request_body = {
            "values": [["Cidade", "Estação", "(24h)"]] + valores_ordenados
        }

        result = sheet.values().update(
            spreadsheetId=SPREADSHEET_ID,
            range=f"'{nome_pagina}'!A1",
            valueInputOption="RAW",
            body=request_body
        ).execute()

        print(f'Valores adicionados e ordenados na página {nome_pagina}: {valores_ordenados}')
    except Exception as e:
        print(f"Ocorreu um erro ao adicionar valores na página: {e}")

def criar_nova_pagina(nome_pagina):
    creds = autenticar()

    if creds:
        try:
            service = build('sheets', 'v4', credentials=creds)
            sheet = service.spreadsheets()
            
            requests = [
                {
                    "addSheet": {
                        "properties": {
                            "title": nome_pagina
                        }
                    }
                }
            ]
            
            body = {"requests": requests}
            response = sheet.batchUpdate(
                spreadsheetId=SPREADSHEET_ID,
                body=body
            ).execute()

            print(f'Nova página criada: {nome_pagina}')

        except Exception as e:
            print(f"Ocorreu um erro ao criar a nova página: {e}")


def criar_nome_pagina():
    data_atual = datetime.now()
    data_arredondada = data_atual.replace(second=0, microsecond=0)
    return data_arredondada.strftime("hora_%H_%M_data_%d_%m_%Y")