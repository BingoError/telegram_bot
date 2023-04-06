from aiogram import Bot, Dispatcher, executor, types
from dotenv import load_dotenv

import Bot.handlers_register as handlers_register
import os


class TgBot:
    def __init__(self):
        load_dotenv()
        self.API_token = os.getenv("API_token")           
        self.bot = Bot(self.API_token)
        self.dp = Dispatcher(self.bot) 
        self.handlers_register = handlers_register.HandlersRegisterBot(self.dp)
        self.handlers_register.register_handlers()
        
    def start_bot(self):
        executor.start_polling(self.dp, skip_updates=True)


