# from dotenv import load_dotenv
import GetApi.confg as confg  
import requests as rq 

# load_dotenv()

class GetPrice:
    # api_key = os.getenv("API_KEY")    
    def GetSymbol(self, getsymbol):
       payload = {'symbol': getsymbol} #for example BTCUSDT, SHIBUSDT etc...
       response = rq.get(confg.url_api, params = payload)
       text = response.json()
       return text
   
   