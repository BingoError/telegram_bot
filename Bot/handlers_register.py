from aiogram import  Dispatcher, types, Bot

from aiogram.utils.markdown import bold, code
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
import mark as key
from aiogram.types.message import ParseMode
from GetApi.getApi import *
from DataBase.DatabaseConn import *
import re

class HandlersRegisterBot:
    def __init__(self, dp: Dispatcher):
        self.COIN_AMOUNT_REGEX = re.compile(r'^([A-Za-z0-9]+)\s+(\d+(\.\d+)?)$')
        self.waiting_for_coin = False
        self.db = PostgreSQL()
        self.button1 = KeyboardButton('Add coin 💩')
        self.button2 = KeyboardButton('Show portfolio 🥸')
        self.reply_keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)

        self.reply_keyboard.add(self.button1, self.button2)
        self.getPrice = GetPrice()
        self.dp = dp

    def register_handlers(self):
        self.dp.register_message_handler(self.handle_start, commands=['start'])
        self.dp.register_message_handler(self.handle_button1, text="Add coin 💩")
        self.dp.register_message_handler(self.process_message, types.Message)

        # self.dp.register_callback_query_handler(self.handle_button2, lambda c: c.data == 'button2')
        # self.dp.register_message_handler(self.getPriceReq, types.Message)

    async def handle_start(self, message: types.Message):
        await message.answer(f"Hello this bot will help you control your portfolio on the crypto market.\nWrite {bold('BTCUSDT')} or {bold('BTC')} and get price this coin💹", parse_mode=ParseMode.MARKDOWN, reply_markup = self.reply_keyboard)
       
    
    def checkCoin(self, name):
        id_coin = self.db.add_coin(name)        
        return id_coin
        
    
    def checkUser(self, message):
        user = message.from_user
        username = user.username
        id_user = self.db.add_user(username)   
        return id_user
    
#----------------------------------------------------------------------------------

    async def handle_button1(self, message: types.Message):      
        self.waiting_for_coin = True
        await message.answer(f"Write the coin you want to add your portfolio \n{bold('Example')}: ETH 1.1", parse_mode= ParseMode.MARKDOWN)

    async def process_message(self, message: types.Message):
        
        if self.waiting_for_coin: 
            text = message.text.strip()
            if self.COIN_AMOUNT_REGEX.match(text):   
                
                self.db.connect()
                
                coin, amount = text.split()
                amount = float(amount)
                data = {'coin': coin.upper(), 'amount': amount}
                coinId = self.checkCoin(data['coin'])
                userId = self.checkUser(message)
                self.db.add_to_portfolio(userId, coinId, data['amount'])
                 
                self.db.close_connection()
                
                await message.answer("Add to portfolio")
            else:
                await message.answer(f"Invalid format. Please enter the coin name and amount separated by space.\n{bold('Example')}: ETH 1.1", parse_mode=ParseMode.MARKDOWN)
        else :
            await message.answer("Please choose the button", parse_mode=ParseMode.MARKDOWN)
            
    
    

   
    # async def getPriceReq(self,message: types.Message):
    #     user_massage = message.text
    #     if user_massage.lower():
    #         user_massage = user_massage.upper()
    #     await message.answer(self.getPrice.GetSymbol(user_massage), parse_mode= ParseMode.MARKDOWN)

