import speech_recognition as sr
import ui_lib, os, requests, pyttsx3, webbrowser

engine = pyttsx3.init()
ui_lib.Center_Amount = 30
ui_lib.Clear()
ui_lib.TopLines()
ui_lib.Title("Zuros Assistant v1.0")
ui_lib.CreateOption("(1) Weather"), ui_lib.CreateOption("(2) Open Google")
ui_lib.Credits("ArilisDev")
ui_lib.BottomLines()

engine.setProperty('rate', 170)
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)

engine.say("Welcome to Zuros Assistant v1.0")
engine.runAndWait()

cwd = os.getcwd()



api_key_file = open(cwd + "\\weather_api_key.txt", "r")
api_key = api_key_file.read()

zip_code_file = open(cwd + "\\weather_zip_code.txt", "r")
zip_code = zip_code_file.read()

weather_api_url = f'https://samples.openweathermap.org/data/2.5/weather?zip={zip_code},us&appid={api_key}'

beep = lambda x: os.system("echo -n '\a';sleep 0.2;" * x)

def openURL(url):
    webbrowser.open(url)

def retry():
    ui_lib.Center_Amount = 30
    ui_lib.Clear()
    ui_lib.TopLines()
    ui_lib.Title("Zuros Assistant v1.0")
    ui_lib.CreateOption("(1) Weather"), ui_lib.CreateOption("(2) Open Google")
    ui_lib.Credits("ArilisDev")
    ui_lib.BottomLines()
    r = sr.Recognizer()
    with sr.Microphone() as source:
        engine.say("What is your command?")
        engine.runAndWait()
        r.adjust_for_ambient_noise(source)
        audio = r.listen(source)
        try:
            text = r.recognize_google(audio)
            if text == "weather":
                json_data = requests.get(weather_api_url).json()
                condition = json_data['weather'][0]["description"]
                humidity = json_data["main"]["humidity"]
                city = json_data["name"]
                engine.say(f"There is currently {condition}, with a humidity of {humidity} in {city}")
                engine.runAndWait()
                engine.say("would you like to do another command?")
                engine.runAndWait()
                r.adjust_for_ambient_noise(source)
                audio = r.listen(source)
                retrytext = r.recognize_google(audio)
                if retrytext == "yes":
                    retry()
            elif text == "open google":
                webbrowser.open('https://google.com')
                engine.say("Command executed, would you like to do another command?")
                engine.runAndWait()
                r.adjust_for_ambient_noise(source)
                audio = r.listen(source)
                retrytext = r.recognize_google(audio)
                if retrytext == "yes":
                    retry()            
            else:
                engine.say(f"{text} is an invalid command.")
                engine.runAndWait()
                retry()
        except:
            engine.say("I was unable to hear your command, please try again.")
            engine.runAndWait()
            retry()
            
retry()
ui_lib.Debug()