import speech_recognition as sr
import pyttsx3
import pandas as pd

# load the admission data
admission_data = pd.read_csv("adm_data.csv")

# initialize text to speech engine
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

# function to determine the university rating and chance of getting admitted
def get_university_ratings(gre_score, toefl_score):
    matches = admission_data[(admission_data["GRE Score"] >= gre_score) & (admission_data["TOEFL Score"] >= toefl_score)]
    if not matches.empty:
        university_ratings = matches["University Rating"].unique()
        return university_ratings
    else:
        return None

# function that encloses all program functions
def admission_service():
    # main program loop
    while True:
        speak("What is your GRE score?")
        gre_score_text = listen()
        if not gre_score_text.isdigit():
            speak("Please provide a valid GRE score.")
            continue
        gre_score = int(gre_score_text)
        speak(f"Your GRE score is {gre_score}.")

        speak("What is your TOEFL score?")
        toefl_score_text = listen()
        if not toefl_score_text.isdigit():
            speak("Please provide a valid TOEFL score.")
            continue
        toefl_score = int(toefl_score_text)
        speak(f"Your TOEFL score is {toefl_score}.")

        university_ratings = get_university_ratings(gre_score, toefl_score)
        if university_ratings is not None:
            speak("You can apply to the following universities:")
            for rating in university_ratings:
                speak(f"University with a rating of {rating}")
        else:
            speak("Sorry, we could not find any universities that match your scores.")

        speak("Do you want to try again?")
        choice = listen()
        if "yes" not in choice.lower():
            speak("Thank you for using our service.")
            break



