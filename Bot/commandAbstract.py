from aiogram.dispatcher.filters import Text
from aiogram.types import ParseMode
from aiogram.types import ReplyKeyboardRemove
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

class AddCoin(StatesGroup):
    waiting_for_coin = State()
    waiting_for_delete= State()
    waiting_for_update= State()
    
