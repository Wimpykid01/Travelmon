import streamlit as st
import json

from proxy import lts_proxy

proxy = lts_proxy.Proxy()

tabs = ["Questions & Answers", "Learning Assistance"]

tab_1, tab_2 = st.tabs(tabs)

tab_1.title(tabs[0])
tab_1.header("Generate Practice Test Question")

topic = tab_1.text_area("Please input the topic you want a list of questions & answers for: ")

answer = ""

if tab_1.button("Generate") and topic:
        
#        proxy.system_role = "You're a teacher for 15 year olds, Result in JSON format."
#
 #       proxy.question = "Generate multiple quuestion and answers about: "

 #      proxy.topic = topic

 #      questions_answers = proxy.get_questions_and_answers()

  #     tab_1.write(questions_answers)

    #    tab_1.download_button(label="Download",
 #                             data=json.dumps(questions_answers),
   #                           file_name="download.json", 
 #                             mime="text/json")

        role = "behave like a drunkard who has a failing liver and has consumed 3 bottles of moonshine in the hour, make him socially unacceptable"
        prompt = topic
        answer = proxy.get_answer(role, prompt)
        proxy.get_image(prompt)

tab_1.download_button(label="Download",
                       data=json.dumps(proxy.get_image(prompt)),
                       file_name="download.png", 
                       mime="text/json")
tab_2.write(answer) 
st.image(proxy.get_image(prompt))