import speech_recognition as sr  # This import allows for the function to be used multiple times.
import webbrowser as wb
import time
import random
import pyttsx3
from weather import *
from translate import Translator


def translate():
    print("Speak the text you want to translate below.")
    lang_select = input("1) English to Spanish\n"
                        "2) English to Portuguese\n"
                        "3) English to Chinese\n"
                        "4) English to French\n"
                        "Your Input: ")
    if lang_select == "1":
        lang = "es"
    elif lang_select == "2":
        lang = "pt"
    elif lang_select == "3":
        lang = "zh"
    elif lang_select == "4":
        lang = "fr"
    translator = Translator(to_lang= lang)
    say(translator.translate(speech()))


def speech():
    r = sr.Recognizer()
    with sr.Microphone() as source:  # This enables the microphone to be used.
        r.adjust_for_ambient_noise(source)
        print("Speak Now: ")
        audio = r.listen(source)  # Listening to the audio source and saving it under the variable source.
        try:  # Used to verify that the audio is clear
            dictation = r.recognize_google(audio)
            return dictation
        except sr.RequestError:  # This prevents the code from exiting out on an error.
            print("Could not recognize that input, because of an error with the Google Speech API")

# Did you say?: Defensive programming for misinterpreted statements, and also including a text

def message_recorder():
    print("This is the message recording section. Please enter your file name below, wait for the prompt and begin"
          "speaking.")
    filename = input(str("File Title: "))
    user_file = open(filename, "w")
    user_file.write(speech())


def search():
    wb.open_new_tab('https://www.google.com/search?q=%s' % speech())  # The % appends the string onto the search
    '''
    This search works due to the way that a google search URL is formatted. The start of every google search is the
    same, and appending allows me to let the user search their desired query through google. Also, the speech function
    is accessed here in order to have the user verbally input their search. 
    '''

'''
def date():
    print("Enter Your Location: ")
    user_location = input(str("Here: "))
    # localtime = time.asctime(time.localtime(time.time()))
    # print("Today's Date and Your Local Time: " + localtime)
    weather = Weather(unit=Unit.CELSIUS)
    location = weather.lookup_by_location(user_location)
    forecasts = location.forecast
    print("Note: All temperatures are in Celsius")
    for forecast in forecasts:
        print("On " + forecast.date + ", in " + user_location + " the forecast calls for " + forecast.text +
              ". The high will be " + forecast.high + "\u00b0. The low will be " + forecast.low + "\u00b0.")
'''
# At this point, the code is commented out because the API is currently retired. I am in the process of trying to obtain
# a license.


def question_picker(numbers, count):
    number_list = list(numbers)  # This creates a list the length of the parameter numbers
    random.shuffle(number_list)  # This use of the random function mixes the order of this created list
    return number_list[:count]
    '''
    This returns the list cut down to the length of the count parameter. Also, the return function is used here
    because I do not want the user to see this list. This would confuse any user. Although the list is vital in
    having random questions. Therefore, returning it bounds it to the function for later use in my code.
    '''


def spelling():
    print("Write the instructions here")
    time.sleep(0.5)
    # Incorporate a restate word functionality
    words = open("Words.txt", "r")
    solution = words.readlines()
    indexes = question_picker(range(0, 14), 10)
    words.seek(0)
    questions = words.readlines()
    score = 0
    for index in indexes:
        say(questions[index].strip())
        answer = input(str("Your answer: ")).lower()
        if solution[index].strip("\n") == answer:
            print("Correct")
            score += 1
        else:
            print("Incorrect\nCorrect Answer: " + solution[index].strip("\n"))
    print("Your score was " + str(score))


def say(statement):
    engine = pyttsx3.init()  # Initializing, or engaging the pyttsx3 package.
    rate = engine.getProperty('rate')  # This is acessing the property of speaking rate.
    engine.setProperty('rate', rate - 50)  # This drops the default speaking rate by 50 WPM, as the default was 200.
    engine.say(statement)  # This uses the parameter within the function to say what is requested.
    engine.runAndWait()  # This engages the engine, allowing it to speak.
    '''
    This function allows for me to only need one line to initialize and run TTS witin my code. As well, a parameter is used
    in order for the engine to interpret what is entered.
    '''


def restart():
    restart_q = input("(Y/N) Do you want to start again? ").lower()
    if restart_q == "y":
        menu()
    else:
        print("Thanks for using Leo's speech recognition application.")
        exit()


def menu():
    print("Options:\n"
          "1) Message Recorder\n"
          "2) Spelling Bee\n"
          "3) Google Search\n"
          "4) Time of Day and Weather\n"
          "Please Dictate Your Choice: ")
    time.sleep(1.25)
    selection = (speech())
    if len(selection) > 1:
        print("Try that again")
        time.sleep(0.5)
        menu()
    if selection == "1":
        time.sleep(0.5)
        print("Launching Message Recorder")
        message_recorder()
    elif selection == "2":
        time.sleep(0.5)
        print("Launching Spelling Bee")
        spelling()
    elif selection == "3":
        time.sleep(0.5)
        print("Launching Google Search")
        search()
    elif selection == "4":
        time.sleep(0.5)
        print("Launching Date and Weather")
        date()

translate()

# COULD BE USED
# NEED TO DIFFERENTIATE BETWEEN TYPED AND DICTATED INPUTS
# Learn how to change languages
