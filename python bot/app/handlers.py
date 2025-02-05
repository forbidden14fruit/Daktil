from aiogram import F, Router
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, FSInputFile, InputFile, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup,  InlineKeyboardButton
from aiogram.types.input_file import BufferedInputFile
from aiogram.utils.markdown import hbold, hitalic, hunderline, hstrikethrough, hlink
from aiogram.utils.callback_answer import CallbackQuery
import os
import random
import pickle

from app.utils.UserStates import UserStates
from app.utils.constants import get_test_by_number
from app.utils.Tests import TestInfo
from config import ADMIN

router = Router()
userStates = UserStates()

def getRandomImage(directory):
    pictures = os.listdir(directory)
    random_picture = random.choice(pictures)

    with open (f"{directory}/{random_picture}", "rb") as photo:
        return BufferedInputFile(photo.read(), "smth.jpg")

# directory = "images/bukvy_govor"
# letters = os.listdir(directory)
# letters = [i.split('.', 1)[0] for i in letters]

# #Доступные буквы в папке images

# #кнопки из букв
# buttons = []
# for letter in letters:
#     buttons.append(KeyboardButton(text=letter))

# #разбиваем на списки по 9 элементов максимум, чтобы они поместились на клавиатуру
# chunk_size = 9
# chunks = [buttons[i:i + chunk_size] for i in range(0, len(buttons), chunk_size)]

# #добавляем кнопку /help в начало списка, чтобы она была вверху
# start_rkm = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text="/help")]] + chunks)

START_COMMAND= f"""
Этот бот поможет Вам закрепить знания по дактилологии.✋🏻
Тест отправляет различные буквы, слоги, слова и предложения на дактильной форме речи.🤓
Ваша главная задача узнать и ответить правильно.✍️
Если Вы не проходили обучение, то предлагаю Вам ссылку на курс: (ссылка)👋
/test - начать тест
/help - помощь или обращайтесь @hdieeodkdb
/statistics - посмотреть статистику
"""

@router.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    await message.answer(f"Привет, {hbold(message.from_user.full_name)}!" + START_COMMAND)

HELP_COMMAND= """
По вопросам работы бота можно обратиться @hdieeodkdb.

/test - начать тест
/statistics - посмотреть статистику
"""

@router.message(Command("help"))
async def command_help(message: Message) -> None:
    await message.reply(text = HELP_COMMAND)



@router.message(Command("save"))
async def command_start_handler(message: Message) -> None:
    global userStates
    #save it
    if message.from_user.id == ADMIN:
        with open(f'test.pickle', 'wb') as file:
            pickle.dump(userStates, file) 
        await message.answer("Текущие результаты тестов сохранены")
    else:
        await message.answer("У вас нет прав на сохранение результатов тестов")

@router.message(Command("load"))
async def command_start_handler(message: Message) -> None:
    global userStates
    #load it
    if message.from_user.id == ADMIN:
        with open(f'test.pickle', 'rb') as file2:
            userStates = pickle.load(file2)
        await message.answer("Тесты загружены")
    else:
        await message.answer("У вас нет прав на загрузку результатов тестов")

@router.message(Command("clear"))
async def command_start_handler(message: Message) -> None:
    global userStates
    userStates = UserStates()
    #save it
    if message.from_user.id == ADMIN:
        with open(f'test.pickle', 'wb') as file:
            pickle.dump(userStates, file) 
        await message.answer("Результаты тестов сброшены")
    else:
        await message.answer("У вас нет прав на очистку тестов")


# statistics = 0

# def upstatistics():
#     global statistics
#     statistics = statistics + 1
#     pass

# @router.message(Command("statistics"))
# async def command_help(message: Message) -> None:
#     upstatistics()
#     await message.reply(text = str(statistics))

@router.message(Command("test"))
async def command_test(message: Message) -> None:
    test_buttons = [[KeyboardButton(text="алфавит"), KeyboardButton(text="слоги")], 
                    [KeyboardButton(text="слова"), KeyboardButton(text="текст")],
                    [KeyboardButton(text="статистика")]]
    test_ikm = ReplyKeyboardMarkup(keyboard=test_buttons)

    await message.answer(text="Выберите задание, которое Вас интересует", reply_markup=test_ikm)

@router.message(F.text == "назад")
async def how_are_you(message: Message) -> None:
    test_buttons = [[KeyboardButton(text="алфавит"), KeyboardButton(text="слоги")], 
                    [KeyboardButton(text="слова"), KeyboardButton(text="текст")],
                    [KeyboardButton(text="статистика")]]
    test_ikm = ReplyKeyboardMarkup(keyboard=test_buttons)
    userStates.stop_test(message.chat.id)
    await message.answer(text="Выберите задание, которое Вас интересует", reply_markup=test_ikm)



@router.message(F.text == "алфавит")
async def how_are_you(message: Message) -> None:
    test_buttons = [[KeyboardButton(text=get_test_by_number(1))],
                    [KeyboardButton(text=get_test_by_number(2))],
                    [KeyboardButton(text=get_test_by_number(3))],
                    [KeyboardButton(text=get_test_by_number(4))],
                    [KeyboardButton(text="назад")]]
    test_ikm = ReplyKeyboardMarkup(keyboard=test_buttons)
    await message.answer(text="Выберите тип задания в разделе алфавит", reply_markup=test_ikm)

async def start_test(message: Message, number: int):
    userStates.start_test(message.chat.id, number)
    question = userStates.get_next_question(message.chat.id)
    
    if number == 9:
        test_buttons = [[KeyboardButton(text="назад")],
                    [KeyboardButton(text="статистика")]]
    else:
        test_buttons = [[KeyboardButton(text=get_test_by_number(number + 1))],
                    [KeyboardButton(text="назад")],
                    [KeyboardButton(text="статистика")]]
        
    test_ikm = ReplyKeyboardMarkup(keyboard=test_buttons)
    if question is None:
        await message.answer(text="Поздравляю, Вы справились с заданиями, можете переходить на следующий тест", reply_markup=test_ikm)
    else:
        await question.send_question(message)

@router.message(F.text == get_test_by_number(1))
async def how_are_you(message: Message) -> None:
    await start_test(message, 1)

@router.message(F.text == get_test_by_number(2))
async def how_are_you(message: Message) -> None:
    await start_test(message, 2)

@router.message(F.text == get_test_by_number(3))
async def how_are_you(message: Message) -> None:
    await start_test(message, 3)

@router.message(F.text == get_test_by_number(4))
async def how_are_you(message: Message) -> None:
    await start_test(message, 4)


@router.message(F.text == "слоги")
async def how_are_you(message: Message) -> None:
    test_buttons = [[KeyboardButton(text=get_test_by_number(5))],
                    [KeyboardButton(text=get_test_by_number(6))],
                    [KeyboardButton(text=get_test_by_number(7))],
                    [KeyboardButton(text="назад")]]
    test_ikm = ReplyKeyboardMarkup(keyboard=test_buttons)
    await message.answer(text="Выберите тип задания в разделе слоги", reply_markup=test_ikm)



@router.message(F.text == get_test_by_number(5))
async def how_are_you(message: Message) -> None:
    await start_test(message, 5)

@router.message(F.text == get_test_by_number(6))
async def how_are_you(message: Message) -> None:
    await start_test(message, 6)

@router.message(F.text == get_test_by_number(7))
async def how_are_you(message: Message) -> None:
    await start_test(message, 7)



@router.message(F.text == "слова")
async def how_are_you(message: Message) -> None:
    test_buttons = [[KeyboardButton(text=get_test_by_number(8))],
                    [KeyboardButton(text="назад")]]
    test_ikm = ReplyKeyboardMarkup(keyboard=test_buttons)
    await message.answer(text="Выберите тип задания в разделе слова", reply_markup=test_ikm)



@router.message(F.text == get_test_by_number(8))
async def how_are_you(message: Message) -> None:
    await start_test(message, 8)



@router.message(F.text == "текст")
async def how_are_you(message: Message) -> None:
    test_buttons = [[KeyboardButton(text=get_test_by_number(9))],
                    [KeyboardButton(text="статистика")],
                    [KeyboardButton(text="назад")]]
    test_ikm = ReplyKeyboardMarkup(keyboard=test_buttons)
    await message.answer(text="Выберите тип задания в разделе текст", reply_markup=test_ikm)



@router.message(F.text == get_test_by_number(9))
async def how_are_you(message: Message) -> None:
    await start_test(message, 9)



@router.message(Command("statistics"))
async def command_test(message: Message) -> None:
    statistics = userStates.get_user_statistics(message.chat.id)
    await message.answer(text=statistics)
@router.message(F.text == "статистика")
async def command_test(message: Message) -> None:
    statistics = userStates.get_user_statistics(message.chat.id)
    await message.answer(text=statistics)


@router.callback_query(TestInfo.filter())
async def vote_callback(query: CallbackQuery, callback_data):
    test = userStates.get_user_test(query.message.chat.id, callback_data.test_number)
    answered = test.check_answer(callback_data.question_number, callback_data.answer)

    if answered == False:
        await query.message.answer(text="Это неправильный ответ")
        #await query.message.answer_photo(caption="Это неправильный ответ", photo=getRandomImage("images/not_fanny_pictures"))
    else:
        await query.message.answer(text="Это правильный ответ")
        #await query.message.answer_photo(caption="Это правильный ответ", photo=getRandomImage("images/fanny_pictures"))
        await query.message.delete()
        
        question = userStates.get_next_question(query.message.chat.id)
        user_state = userStates.get_user_state(query.message.chat.id)
        test_ikm = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text=get_test_by_number(user_state + 1))],
                                                 [KeyboardButton(text="статистика")],
                                                 [KeyboardButton(text="назад")]])
        if question is None:
            await query.message.answer(text="Поздравляю, Вы справились с заданиями, можете переходить на следующий тест", reply_markup=test_ikm)
        else:
            await question.send_question(query.message)

@router.message()
async def command_test(message: Message) -> None:
    user_state = userStates.get_user_state(message.chat.id)

    if user_state == 6 or user_state == 8 or user_state == 9:
        test_number = user_state
        test = userStates.get_user_test(message.chat.id, test_number)
        answered = test.check_answer(message.text)

        if answered == False:
            await message.answer(text="Это неправильный ответ")
            #await message.answer_photo(caption="Это неправильный ответ", photo=getRandomImage("images/not_fanny_pictures"))
        else:
            await message.answer(text="Это неправильный ответ")
            #await message.answer_photo(caption="Это правильный ответ", photo=getRandomImage("images/fanny_pictures"))
            
            question = userStates.get_next_question(message.chat.id)
            user_state = userStates.get_user_state(message.chat.id)

            if question is None:
                if test_number == 9:
                    test_ikm = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text="статистика")],
                                                 [KeyboardButton(text="назад")]])
                else:
                    test_ikm = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text=get_test_by_number(user_state + 1))],
                                                 [KeyboardButton(text="статистика")],
                                                 [KeyboardButton(text="назад")]])
                await message.answer(text="Поздравляю, Вы справились с заданиями, можете переходить на следующий тест", reply_markup=test_ikm)
            else:
                await question.send_question(message)