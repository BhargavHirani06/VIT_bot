import speech_recognition as sr
import pyttsx3
import random
from google.oauth2 import service_account
from google.api_core.exceptions import InvalidArgument
from google.cloud import dialogflow_v2
import wikipedia

engine = pyttsx3.init()


def speak(text):
    engine.say(text)
    engine.runAndWait()


def listen():
    r = sr.Recognizer()
    r.energy_threshold = 1000 
    with sr.Microphone() as source:
        print("Speak now...")
        audio = r.listen(source, phrase_time_limit=10) 
    try:
        text = r.recognize_google(audio)
        print(f"You said: {text}")
        return text
    except:
        print("Sorry, could not recognize your voice.")
        return ""

def detect_intent(project_id, session_id, text):
    credentials = service_account.Credentials.from_service_account_file("C:\\Users\\hp\\Downloads\\chatbot-ylkl-9959a6982fbe.json")
    session_client = dialogflow_v2.SessionsClient(credentials=credentials)
    session_path = session_client.session_path(project_id, session_id)

    if not text:
        return None

    text_input = dialogflow_v2.types.TextInput(text=text, language_code='en-US')
    query_input = dialogflow_v2.types.QueryInput(text=text_input)

    try:
        response = session_client.detect_intent(session=session_path, query_input=query_input)
        return response.query_result.intent.display_name
    except InvalidArgument:
        raise


while True:
    choice = listen().lower()

   
    session_id = f"session{random.randint(1,1000)}"

    intent_name = detect_intent('chatbot-ylkl', session_id, choice)

    if intent_name == 'University_Prediction':
        import University_prediction
        result = University_prediction.admission_service()
        speak(f"The predicted university is {result}")
        break

    elif intent_name == 'faculty_details':
        import faculty_details_getter
        faculty_details_getter.run()
        break
    elif intent_name == 'Min_credits':
        import get_min_credit_branchwise
        get_min_credit_branchwise.run2()
        break

    else:
        try:
            
            page = wikipedia.page(choice)
            summary = wikipedia.summary(choice, sentences=2)
            speak(summary)
        except wikipedia.exceptions.PageError:
            speak("Sorry, I couldn't find any information on that topic. Please try again.")
        except wikipedia.exceptions.DisambiguationError as e:
            
            options = ", ".join(e.options[:5])
            speak(f"I found multiple pages that might match, including {options}. Could you please be more specific?")
        break


    
        
       












