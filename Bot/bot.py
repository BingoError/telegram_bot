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

    # inline_keyboard = InlineKeyboardMarkup(row_width=2)  
    # button1 = InlineKeyboardButton("BTC", callback_data='button1')  
    # button2 = InlineKeyboardButton("ETH", callback_data='button2')  
    # inline_keyboard.add(button1, button2) 

    # @dp.message_handler()
    # async def echo(message: types.Message):
    #     await bot.send_message(chat_id= message.chat.id, text='Виберіть кнопку:', reply_markup=inline_keyboard)


    # @dp.callback_query_handler(lambda c: True)
    # async def process_callback_button1(callback_query: CallbackQuery):
    #     button_data = callback_query.data
    #     await bot.send_message(chat_id=callback_query.message.chat.id, text=f'Ви натиснули кнопку {button_data}')
        

    # executor.start_polling(dp, skip_updates=True)

