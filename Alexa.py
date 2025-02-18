from openai import OpenAI 
from queue import Queue
from config import openai_apikey as apikey
import speech_recognition as speech 
import win32com.client
import webbrowser
import pyttsx3
import threading


queue = Queue()                          
speaker = win32com.client.Dispatch("SAPI.SpVoice")
speaker.Voice = speaker.Getvoices().Item(1)
engine = pyttsx3.init()
openai = OpenAI(
    api_key = apikey,
    base_url = "https://api.deepinfra.com/v1/openai",
)
stream = True 


def printtext(text):
  print(text, end='')


def say1(text) :
   speaker.speak(text)


def say() :
  while(True) :
    text = queue.get()                 # get sentences from queue and say one by one
    if text is None :
      break
    speaker.speak(text)             
    queue.task_done()


def ai(prompt) :
    completion = openai.chat.completions.create(
    model="meta-llama/Meta-Llama-3-8B-Instruct",
    messages=[{"role": "user", "content": prompt}],
    stream=stream,
    )
    sentence = ''
    task1 = threading.Thread(target = say)
    task1.start()
    for chunk in completion :
        if chunk.choices[0].delta.content is not None :
            text = chunk.choices[0].delta.content
            text = text.strip('*')                                       
            task2 = threading.Thread(target = printtext, args = [text])   # to print text 
            task2.start()
            text = text.strip('-')
            text = text.strip('#')
            sentence += text
            if any(char in sentence for char in ['.','!',':']) :          # put a complete sentence in the queue
                queue.put(sentence)
                sentence = ''
    queue.put(None)
    task1.join()                                                          # wait till the task of say function is not complete


def command() :
    while(True) :
        try :
            sr = speech.Recognizer()
            sr.pause_threshold = 1.0
            sr.energy_threshold = 500
            with speech.Microphone() as source :
                print("Listening....")
                audio = sr.listen(source)         # listen audio
            print("Recognizing....")
            say1("Recognizing")
            query = sr.recognize_google(audio,language = "en_IN")    # extract text from the audio using google's engine
            return query
        except Exception as e :
            print("Please say again....")
            say1("Please say again")

if __name__ == '__main__' :
    print("Hello! I am alexa.")
    say1("Hello! I am alexa.")
    while(True) :
        query = command()
        if  "alexa".lower() in query.lower() :
            print("How can i help you?")
            say1("How can i help you?")
            while(True) :
                query = str(command())
                if any(keyword in query.lower() for keyword in ["how", "why", "what", "when", "who", "about"]):
                    print(query)
                    ai(query)
                elif "open".lower() in query.lower() :
                    print(query)
                    sites = query.split(" ")
                    site = str(sites[-1])
                    print(f"opening {site}....")
                    say1(f"opening {site}")
                    webbrowser.open(f"http://www.{site}.com/")
                    break
                elif ("alexa".lower() and "exit".lower()) in query.lower() :
                    print(("Okay! Goodbye."))
                    say1("Okay! Goodbye.")
                    print("exiting....")
                    break
            break
