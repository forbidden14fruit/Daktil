from app.utils.UserState import UserState


class UserStates: 
    def __init__(self):
        self.user_states = []

    def __get_user_state(self, chatId) -> UserState:
        user_state = list(filter(lambda x: x.chatId == chatId, self.user_states))

        if len(user_state) == 0:
            new_user_state = UserState(chatId)
            self.user_states.append(new_user_state)
            return new_user_state
        else:
            return user_state[0]
        
    def get_user_state(self, chatId) -> int:
        user_state = self.__get_user_state(chatId)
        return user_state.state
    
    def get_user_test(self, chatId, number):
        user_state = self.__get_user_state(chatId)
        return user_state.get_user_test(number)
    
    def get_user_statistics(self, chatId) -> str:
        user_state = self.__get_user_state(chatId)
        return user_state.get_user_statistics()


    def start_test(self, chatId, number):
        user_state = self.__get_user_state(chatId)
        user_state.start_test(number)

    def stop_test(self, chatId):
        user_state = self.__get_user_state(chatId)
        user_state.stop_test()

    def check_answer(self, chatId, test_number, question_number, answer):
        user_state = self.__get_user_state(chatId)
        user_state.check_answer(test_number, question_number, answer)

    def get_next_question(self, chatId):
        user_state = self.__get_user_state(chatId)
        return user_state.get_next_question()