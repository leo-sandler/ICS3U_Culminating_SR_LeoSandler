import speech_recognition as sr  # This import allows for the function to be used multiple times, condesing the amount of lines.
import webbrowser as wb
import time
from weather import *


def speech():
    r = sr.Recognizer()

    with sr.Microphone() as source:  # This enables the microphone to be used.
        r.adjust_for_ambient_noise(source)
        timelimit = input(int("How long will you be speaking for: "))
        print("Speak Now: ")
        audio = r.listen(source, phrase_time_limit=timelimit)  # Listening to the audio source and saving it under the variable source.
        try:  # Used to verify that the audio is clear
            dictation = r.recognize_google(audio)
            return dictation
        except sr.UnknownValueError:
            print("Could not recognize that input")


def message_recorder():
    filename = input(str("File Title: "))
    user_file = open(filename, "w")
    user_file.write(speech())
# Can append to the files, via opening old ones. This should also have a menu within it.


def search():
    wb.open_new_tab('https://www.google.com/search?q=%s' % speech())  # the % appends the string onto the search


def date():
    print("Enter Your Location: ")
    user_location = (speech().title())
    localtime = time.asctime(time.localtime(time.time()))
    print("Today's Date and Your Local Time: " + localtime)
    weather = Weather(unit=Unit.CELSIUS)
    location = weather.lookup_by_location(user_location)
    forecasts = location.forecast
    print("Note: All temperatures are in Celsius")
    for forecast in forecasts:
        print("On " + forecast.date + ", in " + user_location + " the forecast calls for " + forecast.text +
              ". The high will be " + forecast.high + ". The low will be " + forecast.low + ".")


def spelling():
    print("Spelling")


def restart():
    restart_q = input("(Y/N) Do you want to start again? ").lower()
    if restart_q == "y":
        menu()
    else:
        print("Thanks for using Leo's speech recognition application.")
        exit()



def menu():
    selection = input("Options:\n"
                      "A) Message Recorder\n"
                      "B) Spelling Bee\n"
                      "C) Bing Search\n"
                      "D) Time of Day and Weather\n"
                      "Your Choice: ").upper()
    if selection == "A":
        message_recorder()
    elif selection == "B":
        spelling()
    elif selection == "C":
        search()
    elif selection == "D":
        date()
    else:
        print("You selected an invalid input.")
        restart()


menu()

# COULD BE USED

# x = k.wait('esc')
# k.wait(hotkey=None, suppress=False, trigger_on_release=False)
# Learn how to change languages
# Spelling Bee
