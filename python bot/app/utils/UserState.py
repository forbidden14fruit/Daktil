from app.utils.Tests import OneLetterImageFourLetterTest, OneLetterImageFourDescriptionTest, OneDescriptionFourLetterTest, OneDescriptionFourLetterImagesTest, OneDescriptionFourSyllableImagesTest, OneSyllableImageInputTest, OneSyllableFourSyllableImagesTest, OneWordImageInputTest
from app.utils.constants import get_test_by_number
from aiogram.utils.markdown import hbold, hitalic, hunderline, hstrikethrough, hlink
import datetime

class UserState:
    def __init__(self, chatId):
        self.chatId = chatId
        self.test1 = None
        self.test2 = None
        self.test3 = None
        self.test4 = None
        self.test5 = None
        self.test6 = None
        self.test7 = None
        self.test8 = None
        self.test9 = None
        # 0 - Тест не начат
        # 1 - Дактилеммы со стороны говорящего (5)
        # 2 - Дактилеммы со стороны воспринимающего (5)
        # 3 - Найдите описание по дактилемме (картинка и 4 описаниz) (5)
        # 4 - У дактилеммы есть описание, какая это дактилемма? (4 дактилеммы) (5)
        # 5 - Описание длинное и 4 картинки слогов из дактилемм, какая картинка соответствует описанию (1, 2, 3, 4) (5)
        # 6 - Дается слог из картинок, напиши этот слог (5)
        # 7 - Даётся слог и 4 картинки слогов из дактилемм, какая картинка соответствует слогу (1, 2, 3, 4) (5)
        # 8 - Дается слово из картинок, напиши это слово (5)
        # 9 - Дается текст из дактилемм, напиши загаданное слово (4)
        #  - Статистика
        self.state = 0

    def get_user_test(self, number):
        if number == 1:
            return self.test1
        elif number == 2:
            return self.test2
        elif number == 3:
            return self.test3
        elif number == 4:
            return self.test4
        elif number == 5:
            return self.test5
        elif number == 6:
            return self.test6
        elif number == 7:
            return self.test7
        elif number == 8:
            return self.test8
        elif number == 9:
            return self.test9

    def start_test(self, number):
        if number == 1:
            self.state = 1
            self.test1 = OneLetterImageFourLetterTest("images/1_bukvy_govor", 5, 1)
        elif number == 2:
            self.state = 2
            self.test2 = OneLetterImageFourLetterTest("images/2_bukvy_vosprinim", 5, 2)
        elif number == 3:
            self.state = 3
            self.test3 = OneLetterImageFourDescriptionTest("images/1_bukvy_govor", 5, 3)
        elif number == 4:
            self.state = 4
            self.test4 = OneDescriptionFourLetterTest(5, 4)
        # elif number == 5:
        #     self.state = 5
        #     self.test5 = OneDescriptionFourLetterImagesTest("images/1_bukvy_govor", 5, 5)
        elif number == 5:
            self.state = 5
            self.test5 = OneDescriptionFourSyllableImagesTest("images/5_syllables", 5, 5)
        elif number == 6: 
            self.state = 6
            self.test6 = OneSyllableImageInputTest("images/5_syllables", 5, 6)
        elif number == 7: 
            self.state = 7
            self.test7 = OneSyllableFourSyllableImagesTest("images/5_syllables", 5, 7)
        elif number == 8: 
            self.state = 8
            self.test8 = OneWordImageInputTest("images/8_words", 5, 8)
        elif number == 9: 
            self.state = 9
            self.test9 = OneWordImageInputTest("images/9_text", 1, 9)

    def get_next_question(self):
        return self.get_user_test(self.state).get_next_question()

    def stop_test(self):
        if self.state != 0:
            if not hasattr(self.get_user_test(self.state), "end_time"):
                self.get_user_test(self.state).end_time = datetime.datetime.now()
        self.state = 0

    def check_answer(self, test_number, question_number, answer):
        return self.get_user_test(test_number).check_answer(question_number, answer)  
    
    def get_user_statistics(self) -> str:
        def __get_test_title(number):
            return hbold(f"Тест '{get_test_by_number(number)}'") + "\n"

        # def __get_test_time(number):
        #     if self.get_user_test(number) is None:
        #         return datetime.timedelta(seconds=0)
        #     elif self.get_user_test(number).end_time is None: 
        #         return datetime.timedelta(seconds=0)
        #     return self.get_user_test(number).end_time - self.get_user_test(number).start_time

        def __get_user_statistics(number):
            if self.get_user_test(number) is None:
                return f"Тест ещё не начат.\n"
            else:
                return self.get_user_test(number).get_user_statistics() + "\n"

        statistics1 = __get_test_title(1) + __get_user_statistics(1)
        statistics2 = __get_test_title(2) + __get_user_statistics(2)
        statistics3 = __get_test_title(3) + __get_user_statistics(3)
        statistics4 = __get_test_title(4) + __get_user_statistics(4)
        statistics5 = __get_test_title(5) + __get_user_statistics(5)
        statistics6 = __get_test_title(6) + __get_user_statistics(6)
        statistics7 = __get_test_title(7) + __get_user_statistics(7)
        statistics8 = __get_test_title(8) + __get_user_statistics(8)
        statistics9 = __get_test_title(9) + __get_user_statistics(9)

        # time1 = __get_test_time(1)
        # time2 = __get_test_time(2)
        # time3 = __get_test_time(1)
        # time4 = __get_test_time(1)
        # time5 = __get_test_time(2)
        # time6 = __get_test_time(1)
        # time7 = __get_test_time(2)
        # time8 = __get_test_time(1)
        # time9 = __get_test_time(2)

        # conclusion = f"Суммарное время прохождения всех тестов: {time1 + time2 + time3 + time4 + time5 + time6 + time7 + time8 + time9}"

        return statistics1 + statistics2 + statistics3 + statistics4 + statistics5 + statistics6 + statistics7 + statistics8 + statistics9 #+ conclusion