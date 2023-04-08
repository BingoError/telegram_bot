# from dotenv import load_dotenv
from aiogram.utils.markdown import bold, code
import GetApi.confg as confg  
import requests as rq 
import re

# load_dotenv()

class GetPrice:
    # api_key = os.getenv("API_KEY")    
    def __init__(self):
        self.response = rq
        
    def get_data_from_api(self, getsymbol):
        payload = {'symbol': getsymbol} #for example BTCUSDT, SHIBUSDT etc...
        self.response = rq.get(confg.url_api, params = payload)  
        self.response.raise_for_status()
        data = self.response.json()
        return data
    
    def checkSymbol(self, symbol):
        if 'USDT' not in symbol:
            symbol += 'USDT'
        return symbol
    
    def process_data(self,data):
        price = code(data['price']) 
        price = price.replace('\\', '')
        return f"Symbol: {code(data['symbol'])}\nPrice: {price}💲"
    
    def GetSymbol(self, symbol):
        try:
            data = self.get_data_from_api(self.checkSymbol(symbol))
            text = self.process_data(data)
        except:
            text = str(f"{symbol} I'll add this symbol as soon as possible")
        return text

   

   