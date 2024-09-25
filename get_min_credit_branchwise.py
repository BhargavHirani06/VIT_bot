import speech_recognition as sr
import pyttsx3
import pandas as pd


min_credit = pd.read_csv("Curriculum.csv")

# initialize the text-to-speech engine
engine = pyttsx3.init()

# function to convert text to speech
def speak(text):
    engine.say(text)
    engine.runAndWait()
    print(text)

# function to convert speech to text
def listen():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Speak now...")
        audio = r.listen(source)
    try:
        text = r.recognize_google(audio)
        print(f"You said: {text}")
        return text
    except:
        print("Sorry, could not recognize your voice.")
        return ""
		
def get_min_credit(branch):
    matches = min_credit[min_credit["Name of the Branch"].str.lower().str.contains(branch.lower())]
    if not matches.empty:
        if len(matches) == 1:
            row = matches.iloc[0]
            speak(f"The minimum number of credit in {row['Name of the Branch']} is {row['University Core']},{row['Programme Core']},{row['University Elective']},{row['Programme Elective']} and total is {row['Total']}.")
        else:
            speak(f"Please provide your branch name properly.")
    else:
        speak("Sorry, we could not find minimum credit for your branch.")
		


def run():
    while True:
        speak("Please provide the name of your branch.")
        branch = listen().strip()
        if len(branch.split()) == 1:
            matches = min_credit[min_credit["Name of the Branch"].str.lower().str.startswith(branch.lower())]
            if len(matches) == 1:
                row = matches.iloc[0]
                speak(f"The minimum number of credit in {row['Name of the Branch']} is {row['University Core']},{row['Programme Core']},{row['University Elective']},{row['Programme Elective']} and total is {row['Total']}.")
            else:
                speak(f"Please provide your branch name properly.")
        else:
            get_min_credit(branch)

        speak("Do you want to try again?")
        choice = listen()
        if "yes" not in choice.lower():
            speak("Thank you for using our service.")
            break
