import speech_recognition as sr  # Lets the program take in verbal input, and convert it to text.
import webbrowser as wb  # Allows for me to open a new tab on the user's computer.
import time  # Used for gathering current time, and allowing the user time to read with .sleep()
import random  # Used for the random question selection within the spelling bee.
import pyttsx3  # Allows for text-to-speech to be used within my code.
from translate import Translator  # Used in the translate function.
import requests  # Used in gathering JSON data from the OpenWeatherMap API.
import datetime  # Used in converting unix time.
import os.path  # Lets me search for existing txt files.


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
            try:  # Used to verify that the audio is clear and that the API is working.
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
            except:  # This prevents the code from exiting out on an error.
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
    engine = pyttsx3.init()  # Initializing the pyttsx3 package.
    rate = engine.getProperty('rate')  # This is accessing the property of speaking rate.
    engine.setProperty('rate', rate - 90)  # This drops the default speaking rate by 90 WPM, as the default was 200.
    engine.say(statement)  # This uses the parameter within the function to say what is requested.
    engine.runAndWait()  # This engages the engine, allowing it to speak.
    '''
    This function allows for me to only need one line to initialize and run TTS witin my code. As well, a parameter is 
    used in order for the engine to interpret what is entered. The speech rate is lowered from the default in order for
    more clarity, as the default is very fast.
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


def message_recorder():
    print("Welcome to the Message Recording section.\nINSTRUCTIONS- Please enter your file name below,"
          " wait for the prompt and enter your desired information. Enter in an existing file name to add onto it.")
    filename = input("File Title: ")  # I am placing no defensive programming on this file name, as it is the user's
    # choice. I have no reason to limit their possible inputs, as this is their file title.
    if os.path.isfile(filename):  # Using the OS function to sense if there is a duplicate file.
        print("You have a file with this name.\nYou will be adding onto it from the end.")
        continuing = input("(Y/N) Continue Adding to This File: ")
        if continuing.upper() == "Y" or continuing.upper() == "YES":  # Sensing if the user wants to add on to the file
            appended_file = open(str(filename), "a")  # If there is a duplicate file, it will be appended to using
            # file I/O. This opening for appending moves the cursor to the end of the file.
            appended_file.write(speech())  # Using the speech function to append to the file.
            restart("ending")
        else:
            restart("wrong_input")  # Calling the restart, as the user has made an error by entering the same name, and
            # not wanting to continue adding to the file.
    else:
        user_file = open(str(filename), "w")  # Using the open function to create a new file, for writing. This is due
        # to the fact that the write command will make a new file, if there are no TXT files with the same name.
        user_file.write(speech())  # The write function allows for the file to be written to. This is done through
        # calling the speech() function.
        restart("ending")  # Calling the restart function, due to the fact that this MR function has ended.
    '''
    This allows users to title a file, and then add onto it using the speech() function. As well, past files can be
    accessed via appending through file I/O.
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
    print("Welcome to the Spelling Bee.\nINSTRUCTIONS- You will be tested on 10 words. These will be spoken to you."
          " Enter the answers into the 'Your Answers' section. Type 'end' into the input to exit the bee.")
    # Notifying the user of the instructions.
    starting = input("(Y/N)Are you ready to start: ")  # Allowing the user to start.
    if starting.upper() == "Y" or starting.upper() == "YES":
        words = open("Words.txt", "r")  # Opening up my words list file for reading, as it is not being edited.
        indexes = question_picker(range(0, 14), 10)  # Picking a random order of the 10 words, out of a possible 15
        # total words on the list.
        words.seek(0)  # Going to the top of the document, to make sure that the lines specified below have not
        # been passed over already.
        questions = words.readlines()  # Reading the TXT file, in order to ask questions and verify solutions
        score = 0  # Keeping track of user score.
        answered = 0
        for index in indexes:  # This for loop goes through the list of index values created via using the question_
            # picker function.
            say(questions[index].strip())  # Using the TTS function, the word is spoken to the user. The .strip()
            # removes whitespace characters which would complicate asking questions and checking answers. The index
            # value from the list is given by the for loop.
            answer = input(str("Your answer: ")).lower()  # The user's input is given here. The .lower() prevents
            # capitalization discrepancies. This is not in speech, as the user could just say the word that they heard
            # (defeating the purpose of a spelling quiz)
            answered += 1
            if questions[index].strip() == answer:  # This checks the answers with the same format as they were asked,
                # by taking away whitespace characters.
                print("Correct")
                score += 1  # Adding onto the score, which needs to be continually updated as the for loop reiterates.
            elif answer.lower() == "end":  # If the user states end, it ends the loop. The .lower() accounts for
                # capitalization discrepancies.
                percent_ended = (int(score) / int(answered - 1)) * 100
                print("Your score was " + str(percent_ended) + "%")
                break  # This ends the loop, and the score is displayed followed by a trigger of the restart function.
            else:  # This makes sure any answer that is not the correct one is marked as incorrect. This also defends
                # the program, as it takes in all possible inputs.
                print("Incorrect\nCorrect Answer: " + questions[index].strip())  # Notifying the user, and then
                # printing the correct answer.
        percent_final = (int(score) / int(10)) * 100
        print("Your score was " + str(percent_final) + "%")  # After the user is done, their % is printed.
        restart("ending")  # Calling the restart function, as the user has reached the end of the spelling bee.
    else:
        restart("wrong_input")
    '''
    The spelling bee section uses the TTS function to ask the user 10 words to spell. The user inputs these, and they 
    are verified through reading a TXT file.
    '''


def search():
    print("Welcome to the Google Search section.\nInput your query in verbal or text format.")
    wb.open_new_tab('https://www.google.com/search?q=%s' % speech())  # The % appends the string onto the search
    restart("ending")
    '''
    This search works due to the way that a google search URL is formatted. The start of every google search is the
    same, and appending allows me to let the user search their desired query through google. Also, the speech function
    is accessed here in order to have the user verbally input their search. 
    '''


def date():
    print("Welcome to the Date and Weather section.")
    try:  # Placed within a try to defend against incorrect city inputs.
        print("Enter City Name: ")
        city_name = speech()  # Calling upon the speech function for this input.
        url = "https://api.openweathermap.org/data/2.5/weather?appid=9eae8652756b8c816d040731d8a607d7&q=" + city_name
        json_data = requests.get(url).json()
        forecast = json_data['weather'][0]['description']  # Accessing the first dictionary within the list(In the API)
        low_temp = json_data['main']['temp_min']  # Accessing the main section of the JSON dictionary.
        celsius_low = low_temp - 273.15  # This is the conversion from kelvin to celsius.
        high_temp = json_data['main']['temp_max']
        celsius_high = high_temp - 273.15
        current_temp = json_data['main']['temp']
        celsius_current = current_temp - 273.15
        wind_speed = json_data['wind']['speed']
        sunrise_time = json_data['sys']['sunrise']
        sunset_time = json_data['sys']['sunset']
        sunrise_final = time_converter(sunrise_time)  # Calling the function which converts UNIX time.
        sunset_final = time_converter(sunset_time)
        time_collected = json_data['dt']
        final_time_collected = time_converter(time_collected)
        localtime = time.asctime(time.localtime(time.time()))  # Using the time function to collect local time,
        print("Today's Date and Your Local Time:\n" + localtime)
        print("Today's Weather Data: " + city_name.title() + "\n"
              "The data was collected at " + final_time_collected + "\n"
              "The forecast is currently " + forecast + ".\n"
              "The temperature is currently " + str(celsius_current) + "\u00b0.\n" 
              "The high temperature is " + str(celsius_high) + "\u00b0.\n"
              "The low temperature is " + str(celsius_low) + "\u00b0.\nThe wind speed is " + str(wind_speed) + " m/s.\n"
              "The sunrise will be at " + sunrise_final + ".\nThe sunset will be at " + sunset_final)
        # Compiling all of the data into a print statement.
        restart("ending")  # Calling the restart function.
    except KeyError:  # This error arises when a city name is spelled incorrectly, as the API will give this error.
        restart("wrong_input")


def multiplication():
    print("Welcome to Multiplication Table Practice.\nINSTRUCTIONS- Select your maximum number that you want"
          "to practice up to. You will be quizzed until this specified number. Answer 'end' to stop the quiz."
          "\nAnswer all questions by typing in numbers(9), rather than writing them in full(nine).")
    max_num: int = input("Max Num: ")  # Asking the user to specify the largest number.
    try:  # This defends the user not entering in a whole number, greater than 1.
        if float(max_num).is_integer() and int(max_num) >= 1:  # This checks if the user input is a whole number
            correct = 0  # Tallying correct answers.
            answered = 0  # Tracking answered questions.
            for current in range(0, int(max_num) + 1):  # Using a for loop to reiterate until the max number is reached.
                print("What is " + str(current) + " x " + str(max_num))  # Asking the user the question.
                ans = input("Your Answer Here: ")  # Taking in the user answer.
                answered += 1  # Automatically, 1 is added to the answered questions within the for loop.
                solution = int(current) * int(max_num)  # The answer is verified through the multiplication operation.
                if ans.lower() == "end":  # This defends capitalization errors when the user enters "end".
                    percent_ended = (int(correct) / int(answered - 1)) * 100  # The same percentage calculation is
                    # made as below, but 1 is subtracted from the answered as the "end" question adds to the total.
                    print("Out of " + str(answered - 1) + " answered questions, you got " + str(correct)
                          + " right answers. You scored " + str(percent_ended) + "%")
                    break  # Ending the loop, as the user has typed end.
                if ans.isdigit():
                    if int(ans) == solution:  # If the user is correct, 1 is added to their score.
                        correct += 1
                elif ans != solution:
                    print("Incorrect. The correct answer is: " + str(solution))
                current += 1  # Allowing for the for loop to continue moving, as the current question number is updated.
                if int(current) > int(max_num):  # This prevents the program from asking a question that goes higher
                    # than their input
                    percent_completion = (int(correct) / int(answered)) * 100
                    print("Out of " + str(answered) + " questions, you got " + str(correct) + " right answers. You "
                          "scored " + str(percent_completion) + " % ")
                    break
        else:  # For some reason, this else errors out when trying to enter in a string for the max number.
            restart("wrong_input")
    except ValueError:  # This is the error received when entering in letters for the maximum number. This is used
        # because it cannot be prevented by the else statement.
        restart("wrong_input")
    restart("ending")
    '''
    This multiplication table function uses try, except, if, elif, and else statements to verify correct inputs within
    this function. The function reiterates due to the presence of a for loop, which can be broken by the user if they 
    decide to end their time within this section.
    '''


def translate():
    print("Input the text you want to translate to French below.")
    translator = Translator(to_lang="fr")  # Specifying the language to be translated as French.
    returned_output = input("Returning of This Output Can be Done in 2 Ways.\n"
                            "1) In speech\n"
                            "2) As text\n"
                            "Your Choice: ")
    if returned_output == "1":
        say(translator.translate(speech()))  # Triggering the say function to output what is input by the speech
        # function. This is done through calling the Translator function.
        restart("ending")
    elif returned_output == "2":
        print(translator.translate(speech()))  # This does the same thing, but returns the input as text.
        restart("ending")
    else:
        restart("wrong_input")  # If the does not enter 1 or 2, the code will not error out.
    '''
    The translation function is mostly ran through the translator module. Using this module allows me to return data
    which is collected by calling upon the speech() function.
    '''


def restart(reason):
    if reason == "ending":  # This is the parameter, which is filled out at the spot where the function is called.
        # I feel like the user should be notified why the code restarts: whether they have completed a section, or
        # made an invalid input.
        print("You have finished using this section.")
    elif reason == "wrong_input":
        print("You entered an incorrect input.")
    restart_q = input("(Y/N) Do you want to start again: ").upper()  # The .lower() prevents capitalization errors
    if restart_q == "Y" or restart_q == "YES":
        menu()  # This triggers the menu, essentialy restarting the entire app.
    else:  # This catches all other possible answers, and ends the code.
        print("Thanks for using Leo's Speech Recognition Application.")
        time.sleep(0.5)
        exit()
    '''
    The restart function is something that is extremely valuable to my code. Since it is used over 15 times, it 
    condenses the total lines used within the application. As well, it allows for my code to have defensive programming.
    Therefore, the application should only end/error out on decisions made by the user.
    '''


def menu():
    print("Welcome to Leo's Speech Recognition Application.\nOptions:\nPick one of these numbers.\n"
          "1) Message Recorder\n"
          "2) Spelling Bee\n"
          "3) Google Search\n"
          "4) Time of Day and Weather\n"
          "5) Multiplication Practice\n"
          "6) English to French Translation\n"
          "Please Make Your Choice: ")
    time.sleep(0.5)
    selection = (speech())  # Calling upon the speech() function for the user's input.
    if selection == "1":  # Each selection launches the corresponding application section.
        time.sleep(0.5)  # Time.sleep() allows for me to allow the user time to read and adjust to what they are doing.
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
    else:  # This prevents the code from having errors, due to an incorrect choice.
        restart("wrong_input")
    '''
    The menu function uses if, elif, and else statements in filtering through user selection responses. This is vital
    to the start of the code, as the menu alerts the user of all options. As well, its use within the restart function
    allows for the user to restart the code, essentially from the start.
    '''


menu()  # Starting the code, by calling the menu function
