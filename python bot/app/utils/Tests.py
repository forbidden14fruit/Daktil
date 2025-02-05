from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardMarkup,  InlineKeyboardButton, Message
from aiogram.types.input_file import BufferedInputFile
from aiogram.utils.media_group import MediaGroupBuilder
import os
import random
import datetime

from app.utils.constants import description_of_dactylemmas, syllables

class TestInfo(CallbackData, prefix="test"):
    test_number: int
    question_number: int
    answer: str

def get_statistics_text(questions, start_time, end_time):
    correct_answers = len(list(filter(lambda x: x.attempts == 1 and x.answered, questions)))

    try:
        time = (end_time - start_time)
        return f"Из {len(questions)} вопросов отвеченных с первой попытки {correct_answers}." + "\n" + f"Время прохождения теста {time}"
    except AttributeError:
        return f"Из {len(questions)} вопросов отвеченных с первой попытки {correct_answers}. Тест начат, но не завершён." 

class OneLetterImageFourLetterQuestion:
    def __init__(self, test_number, question_number, answer, answers, directory, image):
        self.test_number = test_number
        self.question_number = question_number
        self.answer = answer
        self.answers = answers
        self.directory = directory
        self.image = image
        self.answered = False
        self.attempts = 0

    def get_ikbm(self):
        def get_ikb(fakeAnswer):
            return InlineKeyboardButton (text = fakeAnswer, callback_data=TestInfo(test_number=self.test_number, question_number=self.question_number, answer=fakeAnswer).pack())
        
        return InlineKeyboardMarkup (
            inline_keyboard=[
                [
                    get_ikb(self.answers[0]),
                    get_ikb(self.answers[1]),
                    get_ikb(self.answers[2]),
                    get_ikb(self.answers[3]),
                ]
        ])
    
    async def send_question(self, message: Message):
        letter = self.answer
        ikb = self.get_ikbm()
        text = f"{self.question_number}. Какая дактилемма изображена?"

        with open (f"{self.directory}/{self.image}", "rb") as photo:
            photo_file = BufferedInputFile (photo.read(), f"{letter}.jpg")
            message = await message.answer_photo(caption=text, photo=photo_file, reply_markup=ikb)

    def check_answer(self, answer):
        self.attempts += 1
        self.answered = answer == self.answer
        return self.answered
    
class OneLetterImageFourLetterTest:
    def __init__(self, directory, number_of_questions, type):
        self.type = type
        self.letters = os.listdir(directory)
        self.current_question = 0
        self.start_time = datetime.datetime.now()

        self.questions = []

        #загаданы первые questions букв в перемешанном списке букв
        hidden_letters = self.letters
        random.shuffle(hidden_letters)

        for i in range(0, number_of_questions):
            answer = hidden_letters[i] #ответов больше чем вопросов
            answers = [answer.split('.', 1)[0]]
            #формируем варианты ответа
            while len(answers) != 4:
                fake_letter = random.choice(self.letters).split('.', 1)[0]
                if not answers.count(fake_letter):
                    answers.append(fake_letter)
            #перемещиваем список ответов
            random.shuffle(answers)
            number = i + 1
            self.questions.append(OneLetterImageFourLetterQuestion(type, number, answer.split('.', 1)[0], answers, directory, answer))

    def get_next_question(self) -> OneLetterImageFourLetterQuestion:
        if self.current_question >= len(self.questions):
            self.end_time = datetime.datetime.now()
            return None

        current_question = self.questions[self.current_question]
        self.current_question += 1
        current_question.number = self.current_question
        return current_question
    
    def check_answer(self, number, answer):
        question = self.questions[number - 1]
        return question.check_answer(answer)
    
    def get_user_statistics(self) -> str:
        return get_statistics_text(self.questions, self.start_time, self.end_time)



class OneLetterImageFourDescriptionQuestion:
    def __init__(self, test_number, question_number, answer, answers, directory, image):
        self.test_number = test_number
        self.question_number = question_number
        self.answer = answer
        self.answers = answers
        self.directory = directory
        self.image = image
        self.answered = False
        self.attempts = 0

    def get_ikbm(self):
        def get_ikb(fakeAnswer):
            return InlineKeyboardButton (text = fakeAnswer, callback_data=TestInfo(test_number=self.test_number, question_number=self.question_number, answer=fakeAnswer).pack())
        
        return InlineKeyboardMarkup (
            inline_keyboard=[
                [
                    get_ikb("1"),
                    get_ikb("2"),
                    get_ikb("3"),
                    get_ikb("4"),
                ]
        ])
    
    async def send_question(self, message: Message):
        letter = self.answer
        ikb = self.get_ikbm()
        text = f"{self.question_number}. Какая дактилемма изображена?" + f"\n1. {description_of_dactylemmas[self.answers[0]]}" + f"\n2. {description_of_dactylemmas[self.answers[1]]}" + f"\n3. {description_of_dactylemmas[self.answers[2]]}" + f"\n4. {description_of_dactylemmas[self.answers[3]]}"

        with open (f"{self.directory}/{self.image}", "rb") as photo:
            photo_file = BufferedInputFile (photo.read(), f"{letter}.jpg")
            message = await message.answer_photo(caption=text, photo=photo_file, reply_markup=ikb)

    def check_answer(self, answer):
        self.attempts += 1
        self.answered = self.answers[int(answer) - 1] == self.answer
        return self.answered

class OneLetterImageFourDescriptionTest:
    def __init__(self, directory, number_of_questions, type):
        self.type = type
        self.letters = os.listdir(directory)
        self.current_question = 0
        self.start_time = datetime.datetime.now()

        self.questions = []

        #загаданы первые questions букв в перемешанном списке букв
        hidden_letters = self.letters
        random.shuffle(hidden_letters)

        for i in range(0, number_of_questions):
            answer = hidden_letters[i] #ответов больше чем вопросов
            answers = [answer.split('.', 1)[0]]
            #формируем варианты ответа
            while len(answers) != 4:
                fake_letter = random.choice(self.letters).split('.', 1)[0]
                if not answers.count(fake_letter):
                    answers.append(fake_letter)
            #перемещиваем список ответов
            random.shuffle(answers)
            number = i + 1
            self.questions.append(OneLetterImageFourDescriptionQuestion(type, number, answer.split('.', 1)[0], answers, directory, answer))

    def get_next_question(self) -> OneLetterImageFourDescriptionQuestion:
        if self.current_question >= len(self.questions):
            self.end_time = datetime.datetime.now()
            return None

        current_question = self.questions[self.current_question]
        self.current_question += 1
        current_question.number = self.current_question
        return current_question
    
    def check_answer(self, number, answer):
        question = self.questions[number - 1]
        return question.check_answer(answer)
    
    def get_user_statistics(self) -> str:
        return get_statistics_text(self.questions, self.start_time, self.end_time)
    


class OneDescriptionFourLetterQuestion:
    def __init__(self, test_number, question_number, answer, answers):
        self.test_number = test_number
        self.question_number = question_number
        self.answer = answer
        self.answers = answers
        self.answered = False
        self.attempts = 0

    def get_ikbm(self):
        def get_ikb(fakeAnswer):
            return InlineKeyboardButton (text = fakeAnswer, callback_data=TestInfo(test_number=self.test_number, question_number=self.question_number, answer=fakeAnswer).pack())
        
        return InlineKeyboardMarkup (
            inline_keyboard=[
                [
                    get_ikb(self.answers[0]),
                    get_ikb(self.answers[1]),
                    get_ikb(self.answers[2]),
                    get_ikb(self.answers[3]),
                ]
        ])
    
    async def send_question(self, message: Message):
        letter = self.answer
        ikb = self.get_ikbm()
        text = f"{self.question_number}. Какая это дактилемма?" + f"\n{description_of_dactylemmas[letter]}"

        message = await message.answer(text=text, reply_markup=ikb)

    def check_answer(self, answer):
        self.attempts += 1
        self.answered = answer == self.answer
        return self.answered
    
class OneDescriptionFourLetterTest:
    def __init__(self, number_of_questions, type):
        self.type = type
        self.letters = list(description_of_dactylemmas.keys())
        self.current_question = 0
        self.start_time = datetime.datetime.now()

        self.questions = []

        #загаданы первые questions букв в перемешанном списке букв
        hidden_letters = self.letters
        random.shuffle(hidden_letters)

        for i in range(0, number_of_questions):
            answer = hidden_letters[i] #ответов больше чем вопросов
            answers = [answer]
            #формируем варианты ответа
            while len(answers) != 4:
                fake_letter = random.choice(self.letters)
                if not answers.count(fake_letter):
                    answers.append(fake_letter)
            #перемещиваем список ответов
            random.shuffle(answers)
            number = i + 1
            self.questions.append(OneDescriptionFourLetterQuestion(type, number, answer, answers))

    def get_next_question(self) -> OneDescriptionFourLetterQuestion:
        if self.current_question >= len(self.questions):
            self.end_time = datetime.datetime.now()
            return None

        current_question = self.questions[self.current_question]
        self.current_question += 1
        current_question.number = self.current_question
        return current_question
    
    def check_answer(self, number, answer):
        question = self.questions[number - 1]
        return question.check_answer(answer)
    
    def get_user_statistics(self) -> str:
        return get_statistics_text(self.questions, self.start_time, self.end_time)



class OneDescriptionFourLetterImagesQuestion:
    def __init__(self, test_number, question_number, answer, answers, directory, images):
        self.test_number = test_number
        self.question_number = question_number
        self.answer = answer
        self.answers = answers
        self.directory = directory
        self.images = images
        self.answered = False
        self.attempts = 0

    def get_ikbm(self):
        def get_ikb(fakeAnswer):
            return InlineKeyboardButton (text = fakeAnswer, callback_data=TestInfo(test_number=self.test_number, question_number=self.question_number, answer=fakeAnswer).pack())
        
        return InlineKeyboardMarkup (
            inline_keyboard=[
                [
                    get_ikb("1"),
                    get_ikb("2"),
                    get_ikb("3"),
                    get_ikb("4"),
                ]
        ])
    
    async def send_question(self, message: Message):
        ikb = self.get_ikbm()
        text = f"{self.question_number}. Какой слог соответствует описанию?"

        media_group = MediaGroupBuilder(caption=text)
        for image in self.images:
            with open (f"{self.directory}/{image}", "rb") as photo:
                photo_file = BufferedInputFile (photo.read(), f"{image}")
                media_group.add_photo(type="photo", media=photo_file)

        await message.answer_media_group(media=media_group.build())
        await message.answer(text=f"\n{description_of_dactylemmas[self.answer]}", reply_markup=ikb)

    def check_answer(self, answer):
        self.attempts += 1
        self.answered = self.answers[int(answer) - 1] == self.answer
        return self.answered
    
class OneDescriptionFourLetterImagesTest:
    def __init__(self, directory, number_of_questions, type):
        self.type = type
        self.letters = os.listdir(directory)
        self.current_question = 0
        self.start_time = datetime.datetime.now()

        self.questions = []

        #загаданы первые questions букв в перемешанном списке букв
        hidden_letters = self.letters
        random.shuffle(hidden_letters)

        for i in range(0, number_of_questions):
            answer = hidden_letters[i] #ответов больше чем вопросов
            answers = [answer.split('.', 1)[0]]
            #формируем варианты ответа
            while len(answers) != 4:
                fake_letter = random.choice(self.letters).split('.', 1)[0]
                if not answers.count(fake_letter):
                    answers.append(fake_letter)
            #перемещиваем список ответов
            random.shuffle(answers)
            number = i + 1
            images = list(filter(lambda x: x.split('.', 1)[0] in answers, hidden_letters))
            self.questions.append(OneDescriptionFourLetterImagesQuestion(type, number, answer.split('.', 1)[0], answers, directory, images))

    def get_next_question(self) -> OneDescriptionFourLetterImagesQuestion:
        if self.current_question >= len(self.questions):
            self.end_time = datetime.datetime.now()
            return None

        current_question = self.questions[self.current_question]
        self.current_question += 1
        current_question.number = self.current_question
        return current_question
    
    def check_answer(self, number, answer):
        question = self.questions[number - 1]
        return question.check_answer(answer)
    
    def get_user_statistics(self) -> str:
        return get_statistics_text(self.questions, self.start_time, self.end_time)



class OneDescriptionFourSyllableImagesQuestion:
    def __init__(self, test_number, question_number, answer, answers, directory, images):
        self.test_number = test_number
        self.question_number = question_number
        self.answer = answer
        self.answers = answers
        self.directory = directory
        self.images = images
        self.answered = False
        self.attempts = 0

    def get_ikbm(self):
        def get_ikb(fakeAnswer):
            return InlineKeyboardButton (text = fakeAnswer, callback_data=TestInfo(test_number=self.test_number, question_number=self.question_number, answer=fakeAnswer).pack())
        
        return InlineKeyboardMarkup (
            inline_keyboard=[
                [
                    get_ikb("1"),
                    get_ikb("2"),
                    get_ikb("3"),
                    get_ikb("4"),
                ]
        ])
    
    async def send_question(self, message: Message):
        ikb = self.get_ikbm()
        text = f"{self.question_number}. Какая дактилемма соответствует описанию?"

        media_group = MediaGroupBuilder(caption=text)
        for image in self.images:
            with open (f"{self.directory}/{image}", "rb") as photo:
                photo_file = BufferedInputFile (photo.read(), f"{image}")
                media_group.add_photo(type="photo", media=photo_file)

        await message.answer_media_group(media=media_group.build())

        answer = list(map(lambda x: description_of_dactylemmas[x], self.answer))

        await message.answer(text='\n\n'.join(answer), reply_markup=ikb)

    def check_answer(self, answer):
        self.attempts += 1
        self.answered = self.answers[int(answer) - 1] == self.answer
        return self.answered

# def generate_horizontal_image(from_image_directory, image_names, outpath, outname):
#     fileNames = list(map(lambda x: f"{from_image_directory}/{x}", image_names.reverse()))

#     doc = aw.Document()
#     builder = aw.DocumentBuilder(doc)

#     shapes = [builder.insert_image(fileName) for fileName in fileNames]

#     # Вычислить максимальную ширину и высоту и обновить настройки страницы, 
#     # чтобы обрезать документ по размеру изображений.
#     pageSetup = builder.page_setup
#     pageSetup.page_width = sum(shape.width for shape in shapes)
#     pageSetup.page_height = max(shape.height for shape in shapes)
#     pageSetup.top_margin = 0
#     pageSetup.left_margin = 0
#     pageSetup.bottom_margin = 0
#     pageSetup.right_margin = 0

#     doc.save(f"{outpath}/{outname}")

class OneDescriptionFourSyllableImagesTest:
    def __init__(self, directory, number_of_questions, type):
        # #1 шаг. Сгенерировать слоги в нужной папке
        # for syllable in syllables:
        #     letters = [x for x in syllable]
        #     directory_letters = os.listdir(from_image_directory)
        #     letter_image_names = list(filter(lambda x: x.split('.', 1)[0] in letters, directory_letters))
        #     generate_horizontal_image(from_image_directory, letter_image_names, directory, syllable + ".jpg")

        self.type = type
        self.syllables = os.listdir(directory)
        self.current_question = 0
        self.start_time = datetime.datetime.now()

        self.questions = []

        #загаданы первые questions слогов в перемешанном списке слогов
        hidden_syllables = self.syllables
        random.shuffle(hidden_syllables)

        for i in range(0, number_of_questions):
            answer = hidden_syllables[i] #ответов больше чем вопросов
            answers = [answer.split('.', 1)[0]]
            #формируем варианты ответа
            while len(answers) != 4:
                fake_letter = random.choice(self.syllables).split('.', 1)[0]
                if not answers.count(fake_letter):
                    answers.append(fake_letter)
            #перемещиваем список ответов
            random.shuffle(answers)
            number = i + 1
            images = list(filter(lambda x: x.split('.', 1)[0] in answers, hidden_syllables))
            # TODO other class!!!!!!!!
            self.questions.append(OneDescriptionFourSyllableImagesQuestion(type, number, answer.split('.', 1)[0], answers, directory, images))

    def get_next_question(self) -> OneDescriptionFourSyllableImagesQuestion:
        if self.current_question >= len(self.questions):
            self.end_time = datetime.datetime.now()
            return None

        current_question = self.questions[self.current_question]
        self.current_question += 1
        current_question.number = self.current_question
        return current_question
    
    def check_answer(self, number, answer):
        question = self.questions[number - 1]
        return question.check_answer(answer)
    
    def get_user_statistics(self) -> str:
        return get_statistics_text(self.questions, self.start_time, self.end_time)



class OneSyllableImageInputQuestion:
    def __init__(self, test_number, question_number, answer, directory, image):
        self.test_number = test_number
        self.question_number = question_number
        self.answer = answer
        self.directory = directory
        self.image = image
        self.answered = False
        self.attempts = 0
    
    async def send_question(self, message: Message):
        with open (f"{self.directory}/{self.image}", "rb") as photo:
            photo_file = BufferedInputFile (photo.read(), f"{self.image}")
            await message.answer_photo(photo=photo_file, caption=f"{self.question_number}. Какой слог изображён на фотографии? Напиши его")

    def check_answer(self, answer):
        self.attempts += 1
        self.answered = answer == self.answer
        return self.answered
    
class OneSyllableImageInputTest:
    def __init__(self, directory, number_of_questions, type):
        # #1 шаг. Сгенерировать слоги в нужной папке
        # for syllable in syllables:
        #     letters = [x for x in syllable]
        #     directory_letters = os.listdir(from_image_directory)
        #     letter_image_names = list(filter(lambda x: x.split('.', 1)[0] in letters, directory_letters))
        #     generate_horizontal_image(from_image_directory, letter_image_names, directory, syllable + ".jpg")

        self.type = type
        self.syllables = os.listdir(directory)
        self.current_question = 0
        self.start_time = datetime.datetime.now()

        self.questions = []

        #загаданы первые questions слогов в перемешанном списке слогов
        hidden_syllables = self.syllables
        random.shuffle(hidden_syllables)

        for i in range(0, number_of_questions):
            answer = hidden_syllables[i] #ответов больше чем вопросов
            number = i + 1
            self.questions.append(OneSyllableImageInputQuestion(type, number, answer.split('.', 1)[0], directory, answer))

    def get_next_question(self) -> OneSyllableImageInputQuestion:
        if self.current_question >= len(self.questions):
            self.end_time = datetime.datetime.now()
            return None

        current_question = self.questions[self.current_question]
        self.current_question += 1
        current_question.number = self.current_question
        return current_question
    
    def check_answer(self, answer):
        question = self.questions[self.current_question - 1]
        return question.check_answer(answer)
    
    def get_user_statistics(self) -> str:
        return get_statistics_text(self.questions, self.start_time, self.end_time)

class OneSyllableFourSyllableImagesQuestion:
    def __init__(self, test_number, question_number, answer, answers, directory, images):
        self.test_number = test_number
        self.question_number = question_number
        self.answer = answer
        self.answers = answers
        self.directory = directory
        self.images = images
        self.answered = False
        self.attempts = 0

    def get_ikbm(self):
        def get_ikb(fakeAnswer):
            return InlineKeyboardButton (text = fakeAnswer, callback_data=TestInfo(test_number=self.test_number, question_number=self.question_number, answer=fakeAnswer).pack())
        
        return InlineKeyboardMarkup (
            inline_keyboard=[
                [
                    get_ikb("1"),
                    get_ikb("2"),
                    get_ikb("3"),
                    get_ikb("4"),
                ]
        ])
    
    async def send_question(self, message: Message):
        ikb = self.get_ikbm()
        text = f"{self.question_number}. Найдите картинку с указанным слогом"

        media_group = MediaGroupBuilder(caption=text)
        for image in self.images:
            with open (f"{self.directory}/{image}", "rb") as photo:
                photo_file = BufferedInputFile (photo.read(), f"{image}")
                media_group.add_photo(type="photo", media=photo_file)

        await message.answer_media_group(media=media_group.build())

        await message.answer(text=self.answer, reply_markup=ikb)

    def check_answer(self, answer):
        self.attempts += 1
        self.answered = self.answers[int(answer) - 1] == self.answer
        return self.answered
    
class OneSyllableFourSyllableImagesTest:
    def __init__(self, directory, number_of_questions, type):
        # #1 шаг. Сгенерировать слоги в нужной папке
        # for syllable in syllables:
        #     letters = [x for x in syllable]
        #     directory_letters = os.listdir(from_image_directory)
        #     letter_image_names = list(filter(lambda x: x.split('.', 1)[0] in letters, directory_letters))
        #     generate_horizontal_image(from_image_directory, letter_image_names, directory, syllable + ".jpg")

        self.type = type
        self.syllables = os.listdir(directory)
        self.current_question = 0
        self.start_time = datetime.datetime.now()

        self.questions = []

        #загаданы первые questions слогов в перемешанном списке слогов
        hidden_syllables = self.syllables
        random.shuffle(hidden_syllables)

        for i in range(0, number_of_questions):
            answer = hidden_syllables[i] #ответов больше чем вопросов
            answers = [answer.split('.', 1)[0]]
            #формируем варианты ответа
            while len(answers) != 4:
                fake_letter = random.choice(self.syllables).split('.', 1)[0]
                if not answers.count(fake_letter):
                    answers.append(fake_letter)
            #перемещиваем список ответов
            random.shuffle(answers)
            number = i + 1
            images = list(filter(lambda x: x.split('.', 1)[0] in answers, hidden_syllables))
            # TODO other class!!!!!!!!
            self.questions.append(OneSyllableFourSyllableImagesQuestion(type, number, answer.split('.', 1)[0], answers, directory, images))

    def get_next_question(self) -> OneSyllableFourSyllableImagesQuestion:
        if self.current_question >= len(self.questions):
            self.end_time = datetime.datetime.now()
            return None

        current_question = self.questions[self.current_question]
        self.current_question += 1
        current_question.number = self.current_question
        return current_question
    
    def check_answer(self, number, answer):
        question = self.questions[number - 1]
        return question.check_answer(answer)
    
    def get_user_statistics(self) -> str:
        return get_statistics_text(self.questions, self.start_time, self.end_time)



class OneWordImageInputQuestion:
    def __init__(self, test_number, question_number, answer, directory, image):
        self.test_number = test_number
        self.question_number = question_number
        self.answer = answer
        self.directory = directory
        self.image = image
        self.answered = False
        self.attempts = 0
    
    async def send_question(self, message: Message):
        with open (f"{self.directory}/{self.image}", "rb") as photo:
            photo_file = BufferedInputFile (photo.read(), f"{self.image}")
            await message.answer_photo(photo=photo_file, caption=f"{self.question_number}. Какое слово загадано на фотографии? Напиши его")

    def check_answer(self, answer):
        self.attempts += 1
        self.answered = answer == self.answer
        return self.answered
    
class OneWordImageInputTest:
    def __init__(self, directory, number_of_questions, type):
        # #1 шаг. Сгенерировать слоги в нужной папке
        # for syllable in syllables:
        #     letters = [x for x in syllable]
        #     directory_letters = os.listdir(from_image_directory)
        #     letter_image_names = list(filter(lambda x: x.split('.', 1)[0] in letters, directory_letters))
        #     generate_horizontal_image(from_image_directory, letter_image_names, directory, syllable + ".jpg")

        self.type = type
        self.syllables = os.listdir(directory)
        self.current_question = 0
        self.start_time = datetime.datetime.now()

        self.questions = []

        #загаданы первые questions слогов в перемешанном списке слогов
        hidden_syllables = self.syllables
        random.shuffle(hidden_syllables)

        for i in range(0, number_of_questions):
            answer = hidden_syllables[i] #ответов больше чем вопросов
            number = i + 1
            self.questions.append(OneWordImageInputQuestion(type, number, answer.split('.', 1)[0], directory, answer))

    def get_next_question(self) -> OneWordImageInputQuestion:
        if self.current_question >= len(self.questions):
            self.end_time = datetime.datetime.now()
            return None

        current_question = self.questions[self.current_question]
        self.current_question += 1
        current_question.number = self.current_question
        return current_question
    
    def check_answer(self, answer):
        question = self.questions[self.current_question - 1]
        return question.check_answer(answer)
    
    def get_user_statistics(self) -> str:
        return get_statistics_text(self.questions, self.start_time, self.end_time)