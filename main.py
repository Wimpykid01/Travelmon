import streamlit as st
import json
import base64
import io
from PIL import Image
import pathlib
import random
import pandas as pd

from proxy import lts_proxy

proxy = lts_proxy.Proxy()
role = " Your goal is to determine the perfect vacation destination of the user of the website you are part of, using the users preferences on pokemon esque creatures. there are 11 different types, and 1 image of each type will be presented throughout the course of the quiz. You will be given a list of each asked question, with a number out of 100 representing which mon they prefer more, (eg 0 being maximum preference towards type 1 and 100 being maximum preference towards type 2), you will be given a list of types and their significances and you will, after deliberation, say 'Country:[your chosen country]#' and then give a short explanation on why you picked this country. "
typeExplanation = " Here is an explanation of what each mon type represents, use these representations as a basis for your decisions, Dragon: this type prefers blends of cultures but does not like to overstay their welcome, Ice: this type prefers colder climates and more solitary locations, Fire: this type prefers hotter climates and more active locations, Water: this type prefers locations closer to large water bodies like islands or the beach, Grass: this type prefers locations with greenery and nature, Fairy: this type enjoys locations with cultural and historical significance, Steel: this type is awed by highly developed countries, Rock: this type enjoys hikes through mountaneous regions like caves or beaches or mountains, Electric: this type enjoys activity and tourism, Pyschic: this type is amazed by famous attractions of the world, Normal: this type does not like moving around and is lazy so they would prefer a calmer relaxing vacation. "

# variables

DATA_FORMAT = 'image/png'
#image_base641 = proxy.get_image(prompt)
#image_base642 = proxy.get_image(prompt)
if "init" not in st.session_state:
  st.session_state.init = 1
  st.session_state.Types = [["Dragon", "0.png", 0],["Ice", "1.png", 0],["Fire", "2.png", 0],["Water", "3.png", 0],["Grass", "4.png", 0],["Fairy", "5.png", 0],["Steel", "6.png", 0],["Rock", "7.png", 0],["Electric", "8.png", 0],["Pyschic", "9.png", 0],["Normal", "10.png", 0]]
  st.session_state.Preferences = []
  st.session_state.MonOrder = [0,1,2,3,4,5,6,7,8,9,10]
  random.shuffle(st.session_state.MonOrder)
  st.session_state.Page = 0
  st.session_state.LatLong = ""
  st.session_state.verdict = ""
  st.session_state.prompt = ""



#for possible css-ing in the future
def load_CSS(file_path):
  with open(file_path) as f:
    st.html(f"<style{f.read()}</style>")

CSS_path = pathlib.Path("main.css")
load_CSS(CSS_path)

#a page for information + the start button
if st.session_state.Page == 0:
  with st.container():
    st.write("Welcome to the Travelmon quiz, you will be shown different monsters, move the slider towards the monster you like the most, then hit Next. We will then give you a vacation country youd enjoy!")
    if st.button("Start", key="start", use_container_width=True):
      st.session_state.Page = 1
      st.rerun(scope="app")

elif st.session_state.Page > 0 and st.session_state.Page < 11:

  with st.form(f"Page{st.session_state.Page}"):
      
    col1, col2, = st.columns(2, gap="small",vertical_alignment="center")

    st.write(f"{st.session_state.Page}/10")

    col1.image(st.session_state.Types[st.session_state.MonOrder[st.session_state.Page-1]][1])
    col2.image(st.session_state.Types[st.session_state.MonOrder[st.session_state.Page]][1])

    Slider = st.slider("Which do you prefer?", 0, 100, 50)

    if st.form_submit_button("Next", use_container_width=True):
        st.session_state.Types[st.session_state.MonOrder[st.session_state.Page-1]][2] = 1
        st.session_state.Types[st.session_state.MonOrder[st.session_state.Page]][2] = 1

      #then puts the users preference between the 2 types and the names of the 2 types into a variable to use to question the ai
        st.session_state.Preferences.append([st.session_state.Types[st.session_state.MonOrder[st.session_state.Page-1]][0], st.session_state.Types[st.session_state.MonOrder[st.session_state.Page]][0], Slider])

      #increase page by 1
        st.session_state.Page += 1

      #debug stuff

        st.rerun(scope="app")
     
else:
  if st.session_state.verdict == "":
    for i in range(len(st.session_state.Preferences)):
      st.session_state.prompt += f"The users preference between {st.session_state.Preferences[i][0]} and type {st.session_state.Preferences[i][1]} is {st.session_state.Preferences[i][2]}, "
    st.session_state.verdict = proxy.get_answer(role=role+typeExplanation, prompt=st.session_state.prompt).split("#")
    print(st.session_state.verdict)
    st.write(st.session_state.verdict[1])
    st.session_state.LatLong = proxy.get_answer(role="Give ONLY the latitude and the longitude of the inputted country as INTEGERS, with NO OTHER LETTERS, write both of them next to each other with no spaces in between except that they are separated by a singular /", prompt=st.session_state.verdict[0]).split("/")
    Data = {"Lat":[float(st.session_state.LatLong[0])],"Lon":[float(st.session_state.LatLong[1])]}
    Datafarme = pd.DataFrame(data=Data)
    Datafarme.rename(columns={'Lat': 'latitude', 'Lon': 'longitude'}, inplace=True)

    st.map(data=Datafarme,zoom=4,size=5000,color="#4cc54c")
    print(st.session_state.LatLong)

    

  
    

  