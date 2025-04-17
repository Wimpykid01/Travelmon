import base64
import json
import random
import requests
import streamlit as st

class Proxy:
    
    BASE_URL = 'https://ai.techschool.lu:8080/'

    CHAT_URL_SUFFIX = 'chat'
    IMAGE_URL_SUFFIX = 'image'
    SPEECH_URL_SUFFIX = 'speech'

    def __init__(self):
        self.lts_secret = st.secrets.lts_secret

   # def __build_query1(self):
   #     self.query = f"""{self.question}\n'{self.user_data}\n Response 
   #     Specifications: 
   #     - 3-5 diverse questions (can also include additional information)'
   #     - Each response should include some context or explanation.
   #     - Response should be a RFC8259 compliant JSON output in 
   #     the following format: 
   #     "1. What is the meaning of life?": "To find it for yourself.",
   #     "2. How can one find purpose in life?": "By making connections.",
   #     "3. What are some important life skills?": "Knowing how to adapt to change."
   #     """
 
   # def __build_query2(self):
   #     self.query = f"""
   #     Evaluate this answer '{self.answer}' to this question 
   #     '{self.question}'\n and its data:'{self.user_data}'\n\n
   #     Your evaluation should explain what the question did well, 
   #     while highlighting missing details and suggestions for how the 
   #     question could be further improved. In the case that the 
   #     answer does not relate to the question, make this clear and 
   #     generate an example of an acceptable answer. Finally, generate 
   #     a score for the supplied answer on a 10-point scale 
   #     (in the format: 'Score: x out of 10), where a 10 represents a 
   #     complete and accurate answer.
   #     """ 

    def _get_questions_and_answers(self) -> str:
        payload = {
            'lts_secret': self.lts_secret,
            'user_message': self.query,
            'system_message': self.system_role
        }
        headers = {}
        response = requests.post(self.BASE_URL+self.CHAT_URL_SUFFIX, 
                                headers=headers, 
                                data=payload)
        try:
            return response.json()["response"]
        except Exception as e:
            print(f"Error: {response.status_code} - {response.text} - For query: {self.query}")
            return None
    
    def get_questions_and_answers(self) -> str:
        self.__build_query1()
        json_answer: dict = {'content': self.user_data}
        tries = 0
        while tries < 3:
            print(tries)
            try:
                answer = self._get_questions_and_answers()
                print(answer)
                _json_answer = json.loads(answer)
                json_answer.update(_json_answer)
                return json_answer
            except Exception as e:
                tries += 1
                print(f"{tries}:Error parsing JSON: {e}")

    def get_evaluation(self) -> str:
        self.__build_query2()
        answer = self._get_questions_and_answers()
        return answer
    
    def get_answer(self, role: str, prompt: str) -> str:
        self.system_role = role
        self.query = prompt
        return self._get_questions_and_answers()

    def get_random_question(self, file_json: dict):
        if 'questions' in file_json:
            file_json = file_json['questions']
            return random.choice(list(file_json.keys())[1:])
        else:
            return random.choice(list(file_json.keys())[1:])
        
    def get_image(self, prompt) -> str:
        payload = {
            'lts_secret': self.lts_secret,
            'prompt': prompt
        }
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }        
        try:
            response = requests.post(self.BASE_URL+self.IMAGE_URL_SUFFIX, 
                        headers=headers, 
                        data=payload)
            return response.json().get('image')
        except Exception as e:
            print(f"Error: {response.status_code} - {response.text} - For prompt: {prompt}")
            return None
    
    def get_speech(self, input) -> str:
        payload = {
            'lts_secret': self.lts_secret,
            'input': input
        }
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        try:
            response = requests.post(self.BASE_URL+self.SPEECH_URL_SUFFIX, 
                            headers=headers, 
                            data=payload)
            return response.json().get('speech')
        except Exception as e:
            print(f"Error: {response.status_code} - {response.text} - For input: {input}")
            return None
