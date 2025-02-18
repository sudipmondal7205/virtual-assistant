import speech_recognition as speech 
import win32com.client
import webbrowser
import cohere 
from config import cohere_apikey as apikey

co = cohere.Client(
  api_key = apikey, 
) 

def ai(prompt) :
    try :    
        response = co.generate(
            model='command-r-plus',
            prompt=prompt,
            temperature=0.3,
            max_tokens=400 
        )
        return response.generations[0].text.strip()
    except Exception as e:
        print(f"Error during AI request: {e}")
        return "I encountered an error while processing your request."

def say(text) :
   speaker = win32com.client.Dispatch("SAPI.SpVoice")
   speaker.Voice = speaker.Getvoices().Item(1)
   speaker.speak(text)

def command() :
    while(True) :
        try :
            sr = speech.Recognizer()
            sr.pause_threshold = 1.0
            sr.energy_threshold = 500
            with speech.Microphone() as source :
                print("Listening....")
                audio = sr.listen(source)
            print("Recognizing....")
            say("Recognizing")
            query = sr.recognize_google(audio,language = "en_IN")
            return query
        except Exception as e :
            print("Please say again....")
            say("Please say again")

print("Hello! I am alexa.")
say("Hello! I am alexa.")
while(True) :
    query = command()
    if  "alexa".lower() in query.lower() :
        print("How can i help you?")
        say("How can i help you?")
        while(True) :
            query = str(command())
            if any(keyword in query.lower() for keyword in ["how", "why", "what", "when", "who"]):
                print(query)
                text = ai(query)
                print(text)
                say(text) 
            elif "open".lower() in query.lower() :
                print(query)
                sites = query.split(" ")
                site = str(sites[-1])
                print(f"opening {site}....")
                say(f"opening {site}")
                webbrowser.open(f"http://www.{site}.com/")
                break
            elif ("alexa".lower() and "exit".lower()) in query.lower() :
                print(("Okay! Goodbye."))
                say("Okay! Goodbye.")
                print("exiting....")
                break
        break