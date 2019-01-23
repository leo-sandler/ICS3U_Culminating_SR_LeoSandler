import speech_recognition as sr  # Lets the program take in verbal input, and convert it to text.
import webbrowser as wb  # Allows for me to open a new tab on the user's computer.
import time  # Used for gathering current time, and allowing the user time to read with .sleep()
import random  # Used for the random question selection within the spelling bee.
import pyttsx3  # Allows for text-to-speech to be used within my code.
from translate import Translator  # Used in the translate function.
import requests  # Used in gathering JSON data from the OpenWeatherMap API.
import datetime  # Used in converting unix time.


def speech():
    speaking_text = input("(Y/N) Do you want to enter this input via speech: ")
    if speaking_text.upper() == "Y" or speaking_text.upper() == "YES":  # An input which allows the user to pick
        # between a dictated and typed input.
        r = sr.Recognizer()  # Initializing the speech recognition function.
        with sr.Microphone() as source:  # This enables the microphone to be used.
            print("3")  # This countdown allows the user to prepare what they want to dictate.
            time.sleep(1)
            print("2")
            time.sleep(1)
            print("1")
            time.sleep(1)
            r.adjust_for_ambient_noise(source)  # This accounts for ambient noise within the dictation.
            print("Speak Now: ")
            audio = r.listen(source)  # Listening to the audio source and saving it under the variable source.
            try:  # Used to verify that the audio is clear
                dictation = r.recognize_google(audio)  # Using the Google speech API to interpret the verbal input.
                did_you_say = input("Did You Say:\n" + str(dictation) + "\n(Y/N): ")
                if did_you_say.upper() == "Y" or did_you_say.upper() == "YES":
                    return dictation  # This ends the function, as the returned input is transferred to where
                    # the function is called.
                elif did_you_say.upper() == "N" or did_you_say.upper() == "NO":
                    return speech()  # This allows for the user to go through the code again, and for their input
                    # to be returned when this function is called.
                else:
                    restart("wrong_input")  # Preventing an incorrect input to error the code.
            except sr.RequestError or sr.UnknownValueError:  # This prevents the code from exiting out on an error.
                print("Could not recognize that input, because of an error with the Google Speech API")
                restart("ending")  # Calling the restart function, as this function is complete.
    elif speaking_text.upper() == "N" or speaking_text.upper() == "NO":  # The .upper() accounts for capitalization.
        typed_input = input("Type Here: ")  # There is no reason for me to defend this, as the user has freedom to type
        # anything.
        return typed_input  # This return acts in the same way as the dictation
    else:  # This defends against the possibility of a typo within the code.
        restart("wrong_input")  # Calling the restart function. The parameter allows the user to be notified of their
        # incorrect input.
    '''
    This speech recognition is the core of my project. It is called within multiple other functions in the place of
    using inputs. However, sometimes it does not fit(like in the spelling bee) and it is not used. The try and except
    prevents an error caused on Google's end. As well, the if/elif/returning allows for the user to make sure that they
    have entered the correct statement.
    '''


def say(statement):
    engine = pyttsx3.init()  # Initializing, or engaging the pyttsx3 package.
    rate = engine.getProperty('rate')  # This is accessing the property of speaking rate.
    engine.setProperty('rate', rate - 90)  # This drops the default speaking rate by 90 WPM, as the default was 200.
    engine.say(statement)  # This uses the parameter within the function to say what is requested.
    engine.runAndWait()  # This engages the engine, allowing it to speak.
    '''
    This function allows for me to only need one line to initialize and run TTS witin my code. As well, a parameter is 
    used in order for the engine to interpret what is entered. The speech rate is lowered from the default
    '''


def time_converter(time_entered):
    converted_time = datetime.datetime.fromtimestamp(
        int(time_entered)
    ).strftime('%I:%M %p')
    return converted_time  # When printed, the time will show, instead of showing right after the conversion.
    '''
    I am not completely sure of how this function works. Although I understand that it takes data(the time entered) and
    converts it from UNIX time into real time. This is used within the date and weather section, as the sunrise and
    sunset times are in UNIX.
    '''


def date():
    localtime = time.asctime(time.localtime(time.time()))  # Using the time function to find the date and local time.
    print("Today's Date and Your Local Time:\n" + localtime)  # Printing the above variable.
    try:  # Placed within a try to defend against incorrect city inputs.
        print("Enter City Name: ")
        city_name = speech()  # Calling upon the speech function for this input.
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
        restart("ending")
    except KeyError:  # This error arises when a city name is spelled incorrectly.
        restart("wrong_input")


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
                percent_completion = (int(correct) / int(answered)) * 100
                print("Out of " + str(answered) + " questions, you got " + str(correct) + " right answers. You scored "
                      + str(percent_completion) + " % ")
                break
    # DEFEND


def translate():
    print("Speak the text you want to translate below.")
    translator = Translator(to_lang= "fr")
    returned_output = input("Returning of This Output Can be Done in 2 Ways.\n"
                            "1) In speech\n"
                            "2) As text\n"
                            "Your Choice: ")
    if returned_output == "1":
        say(translator.translate(speech()))
        restart("ending")
    elif returned_output == "2":
        print(translator.translate(speech()))
        restart("ending")
    else:
        restart("wrong_input")


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
    restart_q = input("(Y/N) Do you want to start again: ").lower()
    if restart_q.upper() == "Y" or restart_q.upper() == "YES":
        menu()
    else:
        print("Thanks for using Leo's Speech Recognition Application.")
        exit()


def menu():
    print("Welcome to Leo's Speech Recognition Application.\nOptions:\n"
          "1) Message Recorder\n"
          "2) Spelling Bee\n"
          "3) Google Search\n"
          "4) Time of Day and Weather\n"
          "5) Multiplication Practice\n"
          "6) English to French Translation\n"
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
    elif selection == "6":
        time.sleep(0.5)
        print("Launching English to French Translation")
        translate()


translate()
