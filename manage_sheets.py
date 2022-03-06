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
        self.SERVICE_ACCOUNT_FILE = '/home/kron/Documents/kronDev/kronPy/SaltaServices/SaltaServicesSrc/keys.json'

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
    
    #Giving the request a 2D list in to place it as pleased
    def setRangeValues(self, data, hoja="Stock", range_values="A1:A10"): 
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
                            body={"values":[[""] for i in range(149)]}).execute()
        return request
    
    #Replace the row with empty values
    def deleteRow(self, row = 2, hoja = "Stock"):
        request = self.sheet.values().update(spreadsheetId=self.SAMPLE_SPREADSHEET_ID,
                            range=f"{hoja}!A{row}:Z{row}",
                            valueInputOption="USER_ENTERED",
                            body={"values":[["" for i in range(26)]]}).execute()
        return request
    
    def deleteRangeValues(self, hoja="Stock", range_values="E127:F127"): 
        
        #Getting the index of the ':' character as it is the universal separator of values
        index_mid = range_values.find(":")     
        
        #Getting both sizes from the characteristics of the range values in relationshio with their coordinates 
        range_x = alph.find(range_values[index_mid+1]) - alph.find(range_values[0]) + 1
        range_y =  int(range_values[index_mid+2:]) - int(range_values[1:index_mid]) + 1 
        
        # Nested loop to make every value in the range == ""
        request = self.sheet.values().update(spreadsheetId=self.SAMPLE_SPREADSHEET_ID,
                            range=f"{hoja}!{range_values}", 
                            valueInputOption="USER_ENTERED",
                            body={"values":[["" for i in range(range_x)] for j in range(range_y)]}).execute()
        return request
    
    # Joining a couple of preious methods to add the functionality of moving values as a Ctl + X
    def moveRangeValues(self, hoja="Stock", range_values="E127:F127", mov_x = 1, mov_y = 1):
        values = self.returnRangeValues(hoja, range_values)
        
        #Getting the index of the ':' character as it is the universal separator of values
        index_mid = range_values.find(":")     
        
        #Getting both sizes from the characteristics of the range values in relationship with their coordinates 
        extremes = [range_values[:index_mid], range_values[index_mid+1:]]
        
        #Getting the new possition of the array
        for i in range(len(extremes)): 
            column = alph[alph.find(extremes[i][0])+mov_x]
            row = str(int(extremes[i][1:]) + mov_y)
            extremes[i] = column+row
        
        #Update of the values in the new possition
        self.deleteRangeValues(hoja, range_values)
        self.setRangeValues(values, hoja, f"{extremes[0]}:{extremes[1]}")

    #All of the functions on here are enherit to the self made GoogleSheet class and 
    #are aimed to make it easier to implement on another module to manage everything.