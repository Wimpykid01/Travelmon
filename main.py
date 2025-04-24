import streamlit as st
import json
import base64
import io
from PIL import Image
import pathlib
import random

from proxy import lts_proxy

proxy = lts_proxy.Proxy()
role = " Your goal is to determine the perfect vacation destination of the user of the website you are part of, using the users preferences on pokemon esque creatures. there are 11 different types, and 1 image of each type will be presented throughout the course of the quiz. You will be given a list of the previously asked questions thus far, with a number out of 100 representing which mon they prefer more, (eg 0 being maximum preference towards type 1 and 100 being maximum preference towards type 2), the last mentioned type in the prompt is the type that your choice will be compared with. you will be given a list of remaining types that have not be asked about and you will, after deliberation, output 1 word from the list of remaining types EXACTLY, no more and no less"
typeExplanation = " Here is an explanation of what each mon type represents, use these representations as a basis for your decisions, Dragon: this type prefers blends of cultures but does not like to overstay their welcome, Ice: this type prefers colder climates and more solitary locations, Fire: this type prefers hotter climates and more active locations, Water: this type prefers locations closer to large water bodies like islands or the beach, Grass: this type prefers locations with greenery and nature, Fairy: this type enjoys locations with cultural and historical significance, Steel: this type is awed by highly developed countries, Rock: this type enjoys hikes through mountaneous regions like caves or beaches or mountains, Electric: this type enjoys activity and tourism, Pyschic: this type is amazed by famous attractions of the world, Normal: this type does not like moving around and is lazy so they would prefer a calmer relaxing vacation. "

DATA_FORMAT = 'image/png'
#image_base641 = proxy.get_image(prompt)
#image_base642 = proxy.get_image(prompt)
if "init" not in st.session_state:
  st.session_state.init = 1
  st.session_state.Types = [["Dragon", "0.png", 0],["Ice", "1.png", 0],["Fire", "2.png", 0],["Water", "3.png", 0],["Grass", "4.png", 0],["Fairy", "5.png", 0],["Steel", "6.png", 0],["Rock", "7.png", 0],["Electric", "8.png", 0],["Pyschic", "9.png", 0],["Normal", "10.png", 0]]
  st.session_state.Preferences = []
  st.session_state.Page = -1
  st.session_state.AIType = 0
  st.session_state.prompt = ""


@st.fragment
def AI_fragment():
  for i, sublist in enumerate(st.session_state.Types):
    if proxy.get_answer(role=role+typeExplanation, prompt=st.session_state.prompt) in sublist:
      if st.session_state.Types[i][2] == 1:
        print("watesiggma")
        st.rerun(scope="app")
     
      else:
        st.session_state.AIType = i


def load_CSS(file_path):
  with open(file_path) as f:
    st.html(f"<style{f.read()}</style>")

CSS_path = pathlib.Path("main.css")
load_CSS(CSS_path)

if st.session_state.Page == -1:

  if st.button("Start", key="start"):
    st.session_state.Page = 0
    st.rerun(scope="app")

elif st.session_state.Page == 0:

  with st.form(f"Page{st.session_state.Page}"):
    Random_1 = random.randint(0,10)
    Random_2 = random.randint(0,10)

    if Random_1 == Random_2:
      st.rerun(scope="app")
    else:

      col1, col2, = st.columns(2, gap="small",vertical_alignment="center")

      col1.image(st.session_state.Types[Random_1][1])
      col2.image(st.session_state.Types[Random_2][1])

      Slider = st.slider("Which do you prefer?", 0, 100, 50)

    if st.form_submit_button("Next"):
      st.session_state.Types[Random_1][2] = 1
      st.session_state.Types[Random_2][2] = 1
      st.session_state.Preferences.append([st.session_state.Types[Random_1][0], st.session_state.Types[Random_2][0], Slider])
      st.session_state.Page = 1
      print(st.session_state.Preferences)
      print(st.session_state.Types)
      print(st.session_state.Page)
      st.rerun(scope="app")

elif st.session_state.Page > 0 and st.session_state.Page < 11:

  for i in range(len(st.session_state.Preferences)):
    st.session_state.prompt += f"The preference between {st.session_state.Preferences[i][0]} and type {st.session_state.Preferences[i][1]} is {st.session_state.Preferences[i][2]}, "

  st.session_state.prompt += "The remaining types are: "

  for i in range(len(st.session_state.Types)):
    if st.session_state.Types[i][2] == 0:
      st.session_state.prompt += f" {st.session_state.Types[i][0]},"
 
  AI_fragment()

  with st.form(f"Page{st.session_state.Page}"):

    

    col1, col2, = st.columns(2, gap="small",vertical_alignment="center")

    for i, sublist in enumerate(st.session_state.Types):
      if st.session_state.Preferences[-1][1] in sublist:
        PrevType = i

    st.session_state.Types[st.session_state.AIType][2] = 1

    st.write(f"{st.session_state.Page+1}/11")

    print(PrevType)
    print(st.session_state.AIType)

    col1.image(st.session_state.Types[PrevType][1])
    col2.image(st.session_state.Types[st.session_state.AIType][1])

    Slider = st.slider("Which do you prefer?", 0, 100, 50)

    if st.form_submit_button("Next"):

      st.session_state.Preferences.append([st.session_state.Types[PrevType][0], st.session_state.Types[st.session_state.AIType][0], Slider])
      st.session_state.Page += 1
      print(st.session_state.Preferences)
      print(st.session_state.Types)
      print(st.session_state.Page)
      st.rerun(scope="app")