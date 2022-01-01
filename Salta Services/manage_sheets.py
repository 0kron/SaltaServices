from __future__ import print_function
from googleapiclient.discovery import build
from google.oauth2 import service_account

def get_range_values(hoja = "Experimentos"): 
    range_values = ""
    if hoja == "Experimentos": range_values = "A1:G21"
    elif hoja == "Stock": range_values = "A1:E1"
    elif hoja == "Production": range_values = "A1:E5"
    elif hoja == "Ventas": range_values = "A1:F26"
    elif hoja == "Clientes": range_values = "A1:C16"
    else:
        print("\n\n\t\t--Hoja no existente.--")
        range_values = "A1:E5"
    return range_values

def get_range_column(hoja="Experimentos"): 
    range_values = 0
    if hoja == "Experimentos": range_values = 21
    elif hoja == "Stock": range_values = 28
    elif hoja == "Production": range_values = 5
    elif hoja == "Ventas": range_values = 26
    elif hoja == "Clientes": range_values = 16
    else:
        print("\n\n\t\t--Hoja no existente.--")
        range_values = 5
    return range_values

def get_range_row(hoja="Experimentos"): 
    range_values = ""
    if hoja == "Experimentos": range_values = "H"
    elif hoja == "Stock": range_values = "F"
    elif hoja == "Production": range_values = "I"
    elif hoja == "Ventas": range_values = "G"
    elif hoja == "Clientes": range_values = "C"
    else:
        print("\n\n\t\t--Hoja no existente.--")
        range_values = "E"
    return range_values

alph = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
num_ventas = 0

#ValueError: Authorized user info was not in the expected format, missing fields client_secret, refresh_token.
class GoogleSheet:

    SERVICE_ACCOUNT_FILE = ""
    SCOPES = []
    SAMPLE_SPREADSHEET_ID = ""
    creds = None
    service = None
    sheet = None

    def __init__(self):
        #Set Permits: 
        self.SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
        self.SERVICE_ACCOUNT_FILE = 'kronPy/Salta Services/keys.json'

        self.creds = None
        self.creds = service_account.Credentials.from_service_account_file(
        self.SERVICE_ACCOUNT_FILE, scopes=self.SCOPES)

        # The ID and range of a sample spreadsheet.
        self.SAMPLE_SPREADSHEET_ID = '1UGu1bBWuS-J6lmuxuCMwv_GL8LUPlpXzTZ3VGR4Nyz0'

        self.service = build('sheets', 'v4', credentials=self.creds)

            # Call the Sheets API
        self.sheet = self.service.spreadsheets()

    def get_sheet(self, hoja="Experimentos", range_values="A1:G20"):       
        range_values = get_range_values(hoja)
        result = self.sheet.values().get(spreadsheetId=self.SAMPLE_SPREADSHEET_ID, 
                                    range=f"{hoja}!{range_values}").execute()
        values = result.get('values', [])

        return values
    
    def set_single_value(self, data, range_values="A17", hoja="Experimentos"):
        data = [[data]]
        request = self.sheet.values().update(spreadsheetId=self.SAMPLE_SPREADSHEET_ID,
                            range=f"{hoja}!{range_values}", 
                            valueInputOption="USER_ENTERED", 
                            body={"values":data}).execute()
    
        return request
    
    def delete_column(self, column = "A", hoja = "Experimentos"): #HOJA!A1:G3
        range_values = get_range_row
        request = self.sheet.values().update(spreadsheetId=self.SAMPLE_SPREADSHEET_ID,
                            range=f"{hoja}!{column}2:{column}{str(range_values)}", 
                            valueInputOption="USER_ENTERED",
                            body={"values":[[""] for i in range(range_values)]}).execute()
        return request
    
    def delete_row(self, row = 2, hoja = "Experimentos"):
        range_values = get_range_row(hoja)
        request = self.sheet.values().update(spreadsheetId=self.SAMPLE_SPREADSHEET_ID,
                            range=f"{hoja}!A{row}:{range_values}{row}",
                            valueInputOption="USER_ENTERED",
                            body={"values":[["" for i in range(alph.find(range_values))]]}).execute()
        return request

    def return_column(self, column = "A", hoja="Experimentos"): 
        range_values = get_range_column(hoja)
        result = self.sheet.values().get(spreadsheetId=self.SAMPLE_SPREADSHEET_ID, 
                                    range=f"{hoja}!{column}1:{column}{range_values}").execute()
        values = result.get('values', [])
        return values

    def return_row(self, row = 1, hoja="Experimentos"): 
        range_values = get_range_row(hoja)
        result = self.sheet.values().get(spreadsheetId=self.SAMPLE_SPREADSHEET_ID, 
                                    range=f"{hoja}!A{row}:{range_values}{row}").execute()
        values = result.get('values', [])
        return values
    
    def return_single_value(self, hoja="Experimentos", range_values="A1"): 
        result = self.sheet.values().get(spreadsheetId=self.SAMPLE_SPREADSHEET_ID, 
                                    range=f"{hoja}!{range_values}").execute()
        values = result.get('values', [])
        return values[0][0]

    def return_range_values(self, hoja="Experimentos", range_values="A1:G5"): 
        result = self.sheet.values().get(spreadsheetId=self.SAMPLE_SPREADSHEET_ID, 
                                    range=f"{hoja}!{range_values}").execute()
        values = result.get('values', [])
        return values


