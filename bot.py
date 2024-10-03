import pyttsx3
import speech_recognition as sr
import webbrowser  
import datetime  
import wikipedia
from AppOpener import open
from AppOpener import close
import streamlit as st
import os

# Initialize Streamlit page configuration
st.set_page_config(page_title="AI Voice Assistant", page_icon="🤖", layout="centered")

# Streamlit UI for AI Avatar
st.markdown("""
    <style>
        /* Robot Avatar Container */
        .robot-container {
            width: 150px;
            height: 300px;
            position: relative;
            margin: 40px auto;
        }

        /* Robot Head */
        .head {
            width: 80px;
            height: 80px;
            background: radial-gradient(circle, #b8b8b8, #707070); /* Metallic gradient */
            border-radius: 50%;
            position: relative;
            margin: 0 auto;
            box-shadow: 0 4px 10px rgba(0, 0, 0, 0.6), inset 0 5px 10px rgba(255, 255, 255, 0.2);
        }

        /* Robot Eyes with Blinking Effect */
        .head::before, .head::after {
            content: '';
            position: absolute;
            width: 10px;
            height: 10px;
            background: radial-gradient(circle, #00ffcc, #007f7f); /* Glowing green-to-dark eyes */
            border-radius: 50%;
            top: 35%;
            box-shadow: 0 0 10px #00ffcc, 0 0 20px #00ffcc;
        }

        .head::before {
            left: 20px;
            animation: blink 5s infinite;
        }

        .head::after {
            right: 20px;
            animation: blink 5s infinite 2s; /* Delayed blink for the second eye */
        }

        /* Robot Mouth */
        .mouth {
            position: absolute;
            bottom: 15px;
            left: 50%;
            transform: translateX(-50%);
            width: 25px;
            height: 5px;
            background: linear-gradient(90deg, #ff1a1a, #ff4d4d, #ff1a1a); /* Gradient mouth for shine */
            border-radius: 5px;
            box-shadow: 0 0 8px rgba(255, 0, 0, 0.8);
             animation: blink 3s infinite 5s;       
        }

        /* Robot Neck */
        .neck {
            width: 30px;
            height: 20px;
            background: linear-gradient(145deg, #5e5e5e, #303030); /* Metallic neck */
            border-radius: 5px;
            margin: -5px auto 0;
        }

        /* Robot Body */
        .body {
            width: 100px;
            height: 100px;
            background: linear-gradient(145deg, #b8b8b8, #707070); /* Metallic body */
            border-radius: 15px;
            margin: 10px auto;
            box-shadow: 0 4px 10px rgba(0, 0, 0, 0.6), inset 0 5px 10px rgba(255, 255, 255, 0.2);
        }

        /* Robot Arms */
        .left-arm, .right-arm {
            width: 20px;
            height: 60px;
            background: linear-gradient(145deg, #9e9e9e, #707070); /* Metallic arms */
            border-radius: 10px;
            position: absolute;
            top: 130px;
            box-shadow: 0 4px 10px rgba(0, 0, 0, 0.6), inset 0 5px 10px rgba(255, 255, 255, 0.2);
        }

        .left-arm {
            left: -30px;
            animation: arm-move 3s infinite alternate;
        }

        .right-arm {
            right: -30px;
            animation: arm-move 3s infinite alternate-reverse;
        }

        /* Robot Legs */
        .legs {
            display: flex;
            justify-content: space-between;
            width: 80px;
            margin: 0 auto;
        }

        .left-leg, .right-leg {
            width: 25px;
            height: 100px;
            background: linear-gradient(145deg, #9e9e9e, #707070); /* Metallic legs */
            border-radius: 10px;
            box-shadow: 0 4px 10px rgba(0, 0, 0, 0.6), inset 0 5px 10px rgba(255, 255, 255, 0.2);
        }

        /* Animations */

        /* Blink Animation */
        @keyframes blink {
            0%, 90%, 100% {
                opacity: 1;
            }
            92%, 98% {
                opacity: 0;
            }
        }

        /* Arm Movement Animation */
        @keyframes arm-move {
            0% {
                transform: rotate(15deg);
            }
            100% {
                transform: rotate(-15deg); /* Arm swing */
            }
        }
    </style>

    <!-- Mini Robot Full-Body Avatar -->
    <div class="robot-container">
        <!-- Robot Head -->
        <div class="head">
            <div class="mouth"></div>
        </div>
        <!-- Robot Neck -->
        <div class="neck"></div>
        <!-- Robot Body -->
        <div class="body"></div>
        <!-- Robot Arms -->
        <div class="left-arm"></div>
        <div class="right-arm"></div>
        <!-- Robot Legs -->
        <div class="legs">
            <div class="left-leg"></div>
            <div class="right-leg"></div>
        </div>
    </div>
""", unsafe_allow_html=True)
st.markdown("""
<div style="text-align: center; font-size:24px; color:gray;"> JAAM AI YOUR DESKTOP ASSISTANT </div>
""",unsafe_allow_html=True)
#st.subheader("Speak 'open apps name' from your desktop to lunch the particular app.")
asks=st.selectbox("LISTS OF COMMANDS:",["Which day it is/ today is.","Tell me the time","Tell me about yourself","your name","Search/from wikipedia -(as per your requirement text)"," Bye/stop/exit to exit","Open -app name to lunch the app","Close -app name to close the particular app","Who made you"])

# Function to handle text-to-speech
def speak(audio):
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[0].id)
    engine.say(audio)
    engine.runAndWait()

# Function to recognize user's voice
def take_command():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.pause_threshold = 0.8
        audio = r.listen(source, phrase_time_limit=5)
        try:
            query = r.recognize_google(audio, language='en-in')
            return query.lower()
        except sr.UnknownValueError:
            return None  # Keep listening silently
        except sr.RequestError as e:
            st.write(f"Error with the speech recognition service: {e}")
            return None

# Function to get current day
def tell_day():
    day = datetime.datetime.today().weekday() + 1
    Day_dict = {1: 'Monday', 2: 'Tuesday', 3: 'Wednesday', 4: 'Thursday', 5: 'Friday', 6: 'Saturday', 7: 'Sunday'}
    day_of_the_week = Day_dict.get(day, 'Unknown day')
    st.write(f"Today is {day_of_the_week}")
    speak(f"Today is {day_of_the_week}")

# Function to get current time
def tell_time():
    now = datetime.datetime.now()
    hour = now.strftime("%H")
    minute = now.strftime("%M")
    speak(f"The time is {hour} hours and {minute} minutes")

# Main loop to listen to user commands continuously
def take_query():
    speak("Hi , I am jaam ai at your service 24 7, how may i help you ")
    st.write("Listening...")  # Only print once when starting
    while True:
        query = take_command()
        if query is None:
            continue

        if "open youtube" in query:
            speak("Opening YouTube")
            webbrowser.open("http://www.youtube.com")
            break
        elif "close youtube" in query:
            speak("closiing youtube")
            webbrowser.close("http://www.youtube.com")
            break
        elif "open google" in query:
            speak("Opening Google")
            webbrowser.open("http://www.google.com")
            break
        elif "close google" in query:
            speak("closing Google")
            webbrowser.close("http://www.google.com")
            break
        elif "which day it is" in query or "today is" in query:
            tell_day()
        elif "tell me the time" in query or "time" in query:
            tell_time()
        elif "bye" in query or "exit" in query or "stop" in query:
            speak("Goodbye! Have a nice day.")
            break
        elif"your name" in query:
            speak("i am Jaam ai")
            break
        elif "open calculator" in query or "calculator" in query:
            speak("Opening Calculator")
            open("calculator")
            break
        elif "close calculator" in query:
            speak("closing calculator")
            close("calculator")
            break
        elif "open whatsapp" in query:
            speak("Opening WhatsApp")
            open("whatsapp")
            break
        elif "close whatsapp"in query:
            speak("closing whatsapp")
            close("whatsapp")
            break
        elif "search" in query or "from wikipedia" in query:
            query = query.replace("wikipedia", "").strip()
            if query:
                speak("Searching Wikipedia")
                try:
                    result = wikipedia.summary(query, sentences=3)
                    speak("According to Wikipedia")
                    speak(result)
                    st.write(result)
                except wikipedia.exceptions.DisambiguationError as e:
                    speak(f"Multiple results found: {e.options}")
                except wikipedia.exceptions.PageError:
                    speak("No page found for the query.")
                    break
        elif "tell me about yourself" in query:
            speak("I am an intelligent voice assistant created to help you with a variety of tasks, including answering questions, searching the web, and performing simple actions like opening apps or telling you the time and date")
            break
        elif "open camera" in query:
            speak("opening camera")
            open("camera")
            break
        elif"close camera" in query:
            speak("closing camera")
            close("camera")
            break
        elif"open photos" in query:
            speak("opening photos")
            open("photos")
            break
        elif "close photos" in  query:
            speak("closing photos")
            close("photos")
        elif "who made you" in query:
            speak("I was created by Jamaal.")

# Button to restart the assistant
if st.button('Start Assistant'):
    take_query()

