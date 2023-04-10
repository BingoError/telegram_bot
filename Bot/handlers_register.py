from aiogram import  Dispatcher, types, Bot
from aiogram.dispatcher.filters import Text
from aiogram.utils.markdown import bold
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
import mark as key
from aiogram.dispatcher import FSMContext

from Bot.commandAbstract import *
from aiogram.types.message import ParseMode
from GetApi.getApi import *
from DataBase.DatabaseConn import *
import re

class HandlersRegisterBot:
    def __init__(self, dp: Dispatcher):
        self.checkButton = False
        self.COIN_AMOUNT_REGEX = re.compile(r'^([A-Za-z0-9]+)\s+(\d+(\.\d+)?)$')
        self.db = PostgreSQL()
        self.button1 = KeyboardButton('Add coin 🟡')
        self.button2 = KeyboardButton('Show portfolio 📈')
        self.button3 = KeyboardButton('Update portfolio 🔄')
        self.button4 = KeyboardButton('Delete coin ❌')
        
        self.reply_keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        self.reply_keyboard.add(self.button1, self.button2, self.button3, self.button4)
        self.user = None
        self.getPrice = GetPrice()
        self.dp = dp

    def register_handlers(self):
        self.dp.register_message_handler(self.handle_start, commands=['start'], state='*')     
           
        self.dp.register_message_handler(self.handle_button1, text='Add coin 🟡')
        self.dp.register_message_handler(self.handle_coin_add, state=AddCoin.waiting_for_coin)
        
        self.dp.register_message_handler(self.handle_button3, text='Update portfolio 🔄')
        self.dp.register_message_handler(self.handle_coin_update, state=AddCoin.waiting_for_update)
        
        self.dp.register_message_handler(self.handle_button4, text='Delete coin ❌')
        self.dp.register_message_handler(self.handle_coin_delete, state=AddCoin.waiting_for_delete)
        
        self.dp.register_message_handler(self.show_portfolio, text='Show portfolio 📈')
        
        self.dp.register_message_handler(self.user_message)
        
        
        # self.dp.register_message_handler(self.getPriceReq, types.Message)

    async def user_message(self, message: types.Message):
        await message.answer(f"Choose the button please🗿", parse_mode=ParseMode.MARKDOWN, reply_markup = self.reply_keyboard)

    async def handle_start(self, message: types.Message):
        self.user = message.from_user.username
        await message.answer(f"Hello this bot will help you control your portfolio on the crypto market.\nChoose the button and start add your portfolio💹", parse_mode=ParseMode.MARKDOWN, reply_markup = self.reply_keyboard)
       
    def checkCoin(self, name):
        id_coin = self.db.add_coin(name)        
        return id_coin
    def checkUser(self, username):        
        id_user = self.db.add_user(username)   
        return id_user
#----------------------------------------------------------------------------------------        
    async def handle_button1(self, message: types.Message):            
        await message.answer(f"Write the coin you want to add your portfolio \n{bold('Example')}: ETH 1.1 ❗where 1.1 is quantity❗", parse_mode= ParseMode.MARKDOWN)
        await AddCoin.waiting_for_coin.set()
        
    async def handle_coin_add(self, message: types.Message, state: FSMContext):
        
        if not self.COIN_AMOUNT_REGEX.match(message.text.strip()):
            await message.answer(f"Invalid format. Please enter the coin name and amount separated by space.\n{bold('Example')}: ETH 1.1", parse_mode=ParseMode.MARKDOWN, reply_markup = self.reply_keyboard)
            await state.finish()
            return
        
        await self.AddToPortfolio(message)
        await state.finish()
        
    async def AddToPortfolio(self, message: types.Message):
        text = message.text.strip()
        self.db.connect()
        coin, amount = text.split()
        amount = float(amount)
        data = {'coin': coin.upper(), 'amount': amount}
        coinId = self.checkCoin(data['coin'])
        userId = self.checkUser(message.from_user.username)
        self.db.add_to_portfolio(userId, coinId, data['amount'])                 
        self.db.close_connection()
        
        await message.answer('Coin added to portfolio!')
        self.checkButton = True
#----------------------------------------------------------------------------------------        
    async def handle_button3(self, message: types.Message):  
        self.db.connect()
        if self.db.checkPortfolio(self.user):
            await message.answer(f"Write the coin you want to update \n{bold('Example')}: BTC 1.5", parse_mode= ParseMode.MARKDOWN)
            await AddCoin.waiting_for_update.set()
        else:
            self.db.close_connection()
            await message.answer(f"Your portfolio is empty please add your portfolio and try again", parse_mode= ParseMode.MARKDOWN)
            
    async def handle_coin_update(self, message: types.Message, state: FSMContext):
        
        if not self.COIN_AMOUNT_REGEX.match(message.text.strip()):
            await message.answer(f"Invalid format. Please enter the coin name and amount separated by space.\n{bold('Example')}: ETH 1.1", parse_mode=ParseMode.MARKDOWN, reply_markup = self.reply_keyboard)
            await state.finish()
            return
       
        await self.update_portfolio(message)
        await state.finish()

    async def update_portfolio(self, message: types.Message):     
        text = message.text.strip()
        coin, amount = text.split()
        amount = float(amount)
        data = {'coin': coin.upper(), 'amount': amount}
        coinId = self.checkCoin(data['coin'])
        userId = self.checkUser(message.from_user.username)
        self.db.update_portfolio(coinId, userId)     
        self.db.add_to_portfolio(userId, coinId, data['amount'])                                                            
        self.db.close_connection()
        await message.answer('Coin Update to portfolio!')
            
        #----------------------------------------------------------------------------------
#----------------------------------------------------------------------------------
   
    async def handle_button4(self, message: types.Message):   
        self.db.connect()
        if self.db.checkPortfolio(message.from_user.username):     
            await message.answer(f"Write the coin you want to delete \n{bold('Example')}: BTC 1.5 ❗where 1.5 is quantity❗", parse_mode= ParseMode.MARKDOWN)
            await AddCoin.waiting_for_delete.set()
        else:
            await message.answer(f"Your portfolio is empty please add your portfolio and try again", parse_mode= ParseMode.MARKDOWN)
            self.db.close_connection()

       
    async def handle_coin_delete(self, message: types.Message, state: FSMContext):
        if not self.COIN_AMOUNT_REGEX.match(message.text.strip()):
                await message.answer(f"Invalid format. Please enter the coin name and amount separated by space.\n{bold('Example')}: ETH 1.1 ❗where 1.1 is quantity❗", parse_mode=ParseMode.MARKDOWN, reply_markup = self.reply_keyboard)
                await state.finish()
                return
        
        await self.delete_portfolio(message)
        await state.finish()
      
    async def delete_portfolio(self, message: types.Message):
        text = message.text.strip()
        self.db.connect()
        coin, amount = text.split()
        amount = float(amount)
        data = {'coin': coin.upper(), 'amount': amount}
        coinId = self.checkCoin(data['coin'])
        userId = self.checkUser(message.from_user.username)
        res = self.db.delete_to_portfolio(userId, coinId, data['amount'])                                                            
        self.db.close_connection()
        await message.answer(f"You have {coin} {res}")
        await message.answer('Coin deleted from portfolio!')

#----------------------------------------------------------------------------------
        
    async def show_portfolio(self, message: types.Message):     
        
        self.db.connect() 
        if self.db.checkPortfolio(self.user):

            userId = self.checkUser(message.from_user.username)
            data = self.db.getPortfolio(userId)
            self.db.close_connection()
        
            coin_dict = {}
            for coin, quantity in data:
                coin_dict[coin] = coin_dict.get(coin, 0) + quantity

            output = ''
            for coin, quantity in coin_dict.items():
                output += f"{coin}: {quantity}\n"
            await message.answer(output)
        else: 
            self.db.close_connection()
            await message.answer("Your portfolio is empty please add your portfolio and try again")

        
        
   
   
    
