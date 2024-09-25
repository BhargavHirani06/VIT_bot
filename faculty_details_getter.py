import speech_recognition as sr
import pyttsx3
import pandas as pd

# load the faculty data
faculty_data = pd.read_csv("faculty.csv")

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

# function to get faculty details by name
def get_faculty_details(name):
    matches = faculty_data[faculty_data["Name of the Faculty"].str.lower().str.contains(name.lower())]
    if not matches.empty:
        if len(matches) == 1:
            row = matches.iloc[0]
            speak(f"The cabin number of {row['Name of the Faculty']} is {row['Cabin No']} and the contact number is {row['Mobile No']}.")
        else:
            speak(f"There are multiple faculty members with the name {name}. Please provide the complete name.")
    else:
        speak("Sorry, we could not find any faculty members with that name.")

# main program loop
def run():
    while True:
        speak("Please provide the name of the faculty member.")
        name = listen().strip()
        if len(name.split()) == 1:
            matches = faculty_data[faculty_data["Name of the Faculty"].str.lower().str.startswith(name.lower())]
            if len(matches) == 1:
                row = matches.iloc[0]
                speak(f"The cabin number of {row['Name of the Faculty']} is {row['Cabin No']} and the contact number is {row['Mobile No']}.")
            else:
                speak(f"There are multiple faculty members with the name {name}. Please provide the complete name.")
        else:
            get_faculty_details(name)

        speak("Do you want to try again?")
        choice = listen()
        if "yes" not in choice.lower():
            speak("Thank you for using our service.")
            break


