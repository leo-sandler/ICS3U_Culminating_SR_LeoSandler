import speech_recognition as sr  # This import allows for the function to be used multiple times.
import webbrowser as wb
import time
import random
import pyttsx3
from translate import Translator
import requests
import datetime


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

# Option to enter an input via text, not dictation
# Include countdown before speaking
# Did you say?: Defensive programming for misinterpreted statements, and also including a text


def say(statement):
    engine = pyttsx3.init()  # Initializing, or engaging the pyttsx3 package.
    rate = engine.getProperty('rate')  # This is accessing the property of speaking rate.
    engine.setProperty('rate', rate - 90)  # This drops the default speaking rate by 90 WPM, as the default was 200.
    engine.say(statement)  # This uses the parameter within the function to say what is requested.
    engine.runAndWait()  # This engages the engine, allowing it to speak.
    '''
    This function allows for me to only need one line to initialize and run TTS witin my code. As well, a parameter is used
    in order for the engine to interpret what is entered.
    '''


def time_converter(time_entered):
    converted_time = datetime.datetime.fromtimestamp(
        int(time_entered)
    ).strftime('%I:%M %p')
    return converted_time


def date():
    localtime = time.asctime(time.localtime(time.time()))
    print("Today's Date and Your Local Time:\n" + localtime)
    try:
        city_name = input("Enter city name: ")
        url = "https://api.openweathermap.org/data/2.5/weather?appid=9eae8652756b8c816d040731d8a607d7&q=" + city_name
        json_data = requests.get(url).json()
        forecast = json_data['weather'][0]['description']  # Accessing the first dictionary within the list(In the API)
        low_temp = json_data['main']['temp_min']
        celsius_low = low_temp - 273.15
        high_temp = json_data['main']['temp_max']
        celsius_high = high_temp - 273.15
        current_temp = json_data['main']['temp']
        celsius_current = current_temp - 273.15
        wind_speed = json_data['wind']['speed']
        sunrise_time = json_data['sys']['sunrise']
        sunset_time = json_data['sys']['sunset']
        sunrise_final = time_converter(sunrise_time)
        sunset_final = time_converter(sunset_time)
        print("Today's Forecast:\n"
              "The forecast is currently " + forecast + ".\n"
              "The temperature is currently " + str(celsius_current) + "\u00b0.\n" 
              "The high temperature is " + str(celsius_high) + "\u00b0.\n"
              "The low temperature is " + str(celsius_low) + "\u00b0.\nThe wind speed is " + str(wind_speed) + " m/s.\n"
              "The sunrise will be at " + sunrise_final + ".\nThe sunset will be at " + sunset_final)

    except KeyError:  # This error arises when a city name is spelled incorrectly.
        print("DEFEND THIS")


def multiplication():
    print("INSTRUCTIONS")
    max_num: int = input("Max Num: ")
    if float(max_num).is_integer() and int(max_num) >= 1:  # This checks if the user input is a whole number
        correct = 0
        answered = 0
        for current in range(0, int(max_num) + 1):
            print("What is " + str(current) + " x " + str(max_num))
            ans = input("Your Answer Here: ")
            answered += 1
            solution = int(current) * int(max_num)
            if ans.lower() == "end":
                percent_ended = (int(correct) / int(answered - 1)) * 100
                print("Out of " + str(answered - 1) + " answered questions, you got " + str(correct)
                      + " right answers. You scored " + str(percent_ended) + "%")

                break
            elif int(ans) == solution:
                correct += 1
            elif ans.isdigit():
                print("Incorrect. The correct answer is: " + str(solution))
            current += 1
            if int(current) > int(max_num):
                print("Out of " + str(answered) + " questions, you got " + str(correct) + " right answers.")
                # CALCULATE PERCENTAGE
                break


def translate():
    print("Speak the text you want to translate below.")
    lang_select = input("1) English to Spanish\n"
                        "2) English to Portuguese\n"
                        "3) English to French\n"
                        "Your Input: ")
    if lang_select == "1":
        lang = "es"
    elif lang_select == "2":
        lang = "pt"
    elif lang_select == "3":
        lang = "fr"
    else:
        restart("wrong_input")
    translator = Translator(to_lang= lang)
    returned_output = input("Returning of This Output Can be Done in 2 Ways.\n"
                            "1) In speech\n"
                            "2) As text")
    if returned_output == "1":
        say(translator.translate(speech()))
    elif returned_output == "2":
        print(translator.translate(speech()))
    else:
        restart("wrong_input")
    restart("ending")


def message_recorder():
    print("This is the message recording section. Please enter your file name below, wait for the prompt and enter your"
          "desired information.")
    filename = input("File Title: ")  # I am placing no defensive programming on this file name, as it is the user's
    # choice. I have no reason to limit their possible inputs, as this is their file title.
    user_file = open(str(filename), "w")  # Using the open function to create a new file, for writing. This is due to
    # the fact that the write command will make a new file, if there are no TXT files with the same name.
    user_file.write(speech())  # The write function allows for the file to be written to. This is done through
    # calling the speech() function.
    restart("ending")  # Calling the restart function, due to the fact that this MR function has ended.
    '''
    This allows users to title a file, and then add onto it using the speech() function.
    '''


def search():
    wb.open_new_tab('https://www.google.com/search?q=%s' % speech())  # The % appends the string onto the search
    '''
    This search works due to the way that a google search URL is formatted. The start of every google search is the
    same, and appending allows me to let the user search their desired query through google. Also, the speech function
    is accessed here in order to have the user verbally input their search. 
    '''


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
    print("Welcome to the spelling bee.\nYou will be tested on 10 words.\nThese will be spoken to you.\n"
          "Enter the answers into the  (Your Answers)  section.\nType(end)into the input to exit the bee.")
    time.sleep(4)
    print("Here is your first word.")
    time.sleep(0.5)
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
        elif answer.lower() == "end":
            break
        else:
            print("Incorrect\nCorrect Answer: " + solution[index].strip("\n"))
    print("Your score was " + str(score))
    restart("ending")


def restart(reason):
    if reason == "ending":
        print("You have finished using this section.")
    elif reason == "wrong_input":
        print("You entered in the wrong input.")
    restart_q = input("(Y/N) Do you want to start again? ").lower()
    if restart_q.upper() == "Y" or "YES":
        menu()
    else:
        print("Thanks for using Leo's Speech Recognition Application.")
        exit()


def menu():
    print("Hello.\nWelcome to Leo's Speech Recognition Application.")
    print("Options:\n"
          "1) Message Recorder\n"
          "2) Spelling Bee\n"
          "3) Google Search\n"
          "4) Time of Day and Weather\n"
          "5) Multiplication Practice\n"
          "Please Make Your Choice: ")
    time.sleep(0.5)
    selection = (speech())
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
        print("Launching Time of Day and Weather")
        date()
    elif selection == "5":
        time.sleep(0.5)
        print("Launching Multiplication Practice")
        multiplication()


spelling()
