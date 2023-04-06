from aiogram import  Dispatcher, types
from aiogram.utils.markdown import bold, code
import mark as key
from aiogram.types.message import ParseMode

from GetApi.getApi import *

class HandlersRegisterBot:
    def __init__(self, dp: Dispatcher):
        self.getPrice = GetPrice()
        self.dp = dp

    def register_handlers(self):
        self.dp.register_message_handler(self.handle_start, commands=['start'])
        self.dp.register_message_handler(self.getPriceReq, types.Message)

    async def handle_start(self, message: types.Message):
        await message.answer("Hello this bot will help you control the price of crypto currency.\nWrite BTCUSDT or SHIBUSDT and get price this coin💹")

    async def getPriceReq(self,message: types.Message):
        user_massage = message.text
        
        if user_massage.lower():
            user_massage = user_massage.upper()
            
        await message.answer(self.getPrice.GetSymbol(user_massage), parse_mode= ParseMode.MARKDOWN)

