from __future__ import print_function
from googleapiclient.discovery import build
from google.oauth2 import service_account


#Global variables
alph = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

#Google Sheets class to then create and object
class GoogleSheet:

    #Google API Variables to fill:
    SERVICE_ACCOUNT_FILE = ""
    SCOPES = []
    SAMPLE_SPREADSHEET_ID = ""
    creds = None
    service = None
    sheet = None

    #On the constructor, the standar load of rthe service account and the 
    #credentials are made automatically, to change to another google sheets just simply
    #change the .json path and the SAMPLE_SPREADSHEET_ID.
    def __init__(self):
        
        #Set Permits: 
        self.SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
        self.SERVICE_ACCOUNT_FILE = '/home/kron/Documents/kronDev/kronPy/SaltaServices/SaltaServiceBash/keys.json'

        self.creds = None
        self.creds = service_account.Credentials.from_service_account_file(
        self.SERVICE_ACCOUNT_FILE, scopes=self.SCOPES)

        # The ID and range of a sample spreadsheet.
        self.SAMPLE_SPREADSHEET_ID = '1UGu1bBWuS-J6lmuxuCMwv_GL8LUPlpXzTZ3VGR4Nyz0'

        self.service = build('sheets', 'v4', credentials=self.creds)

        # Call the Sheets API and create the object as a sheet
        self.sheet = self.service.spreadsheets()

    #The single value disregards the listed property of the values.
    def returnValue(self, hoja="Stock", range_values="A1"): 
        result = self.sheet.values().get(spreadsheetId=self.SAMPLE_SPREADSHEET_ID, 
                                    range=f"{hoja}!{range_values}").execute()
        values = result.get('values', [])
        return values[0][0]
    
    #As the google API returns 2D lists it is mandatory to convert to singe dimensional lists
    def returnColumn(self, hoja="Stock", range_values="A2:A150"): 
        result = self.sheet.values().get(spreadsheetId=self.SAMPLE_SPREADSHEET_ID, range=f"{hoja}!{range_values}").execute()
        values = result.get('values', [])
 
        ret = []
        for value in values: 
            try: 
                ret.append(value[0])
            except: 
                ret.append("") #The Google API returns error if !value
                
        return ret

    #Once again the last step passes from 2D to 1D list
    def returnRow(self,hoja="Stock", range_values="A1:Z1"): 
        result = self.sheet.values().get(spreadsheetId=self.SAMPLE_SPREADSHEET_ID, 
                                    range=f"{hoja}!{range_values}").execute()
        values = result.get('values', [])
        return values[0]
    
    #The simplest of them all as it returns and effective 2D list
    #however, as the API works, if there is no value in the request it would return None
    def returnRangeValues(self, hoja="Stock", range_values="A1:G5"): 
        result = self.sheet.values().get(spreadsheetId=self.SAMPLE_SPREADSHEET_ID, 
                                    range=f"{hoja}!{range_values}").execute()
        values = result.get('values', [])
        return values
    #This very last function only returns properly when the data is actually complete, 
    #otherwise there can be problems.
    
    def findY(self, hoja = "Stock"):
        return len(self.returnColumn(hoja))+1

    def findX(self, hoja = "Stock"):
        return alph[len(self.returnRow(hoja))-1]
    
    def findRangeValues(self, hoja = "Stock"): 
        return f"A1:{self.findX(hoja)}{self.findY(hoja)}"

    #returns all the values in an specific page inside the google sheets archive:
    def getSheet(self, hoja="Stock", range_values="A1:G20"):       
        range_values = self.findRangeValues(hoja)
        result = self.sheet.values().get(spreadsheetId=self.SAMPLE_SPREADSHEET_ID, 
                                    range=f"{hoja}!{range_values}").execute()
        values = result.get('values', [])

        return values
    
    #Change one single specified value using data and teh range of values.
    def setSingleValue(self, data, range_values="A17", hoja="Stock"):
        data = [[data]]
        request = self.sheet.values().update(spreadsheetId=self.SAMPLE_SPREADSHEET_ID,
                            range=f"{hoja}!{range_values}", 
                            valueInputOption="USER_ENTERED", 
                            body={"values":data}).execute()
    
        return request
    
    ##Replace the column with empty values
    def deleteColumn(self, hoja = "Stock", column = "A"): #HOJA!A1:G3
        request = self.sheet.values().update(spreadsheetId=self.SAMPLE_SPREADSHEET_ID,
                            range=f"{hoja}!{column}2:{column}150", 
                            valueInputOption="USER_ENTERED",
                            body={"values":[[""] for i in range(150)]}).execute()
        return request
    
    #Replace the row with empty values
    def deleteRow(self, row = 2, hoja = "Stock"):
        range_values = self.findX(hoja)
        request = self.sheet.values().update(spreadsheetId=self.SAMPLE_SPREADSHEET_ID,
                            range=f"{hoja}!A{row}:Z{row}",
                            valueInputOption="USER_ENTERED",
                            body={"values":[["" for i in range(26)]]}).execute()
        return request

    #All of the functions on here are enherit to the self made GoogleSheet class and 
    #are aimed to make it easier to implement on another module to manage everything.
