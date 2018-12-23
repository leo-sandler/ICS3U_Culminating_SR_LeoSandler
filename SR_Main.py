import speech_recognition as sr  # This import allows for the function to be used multiple times, condesing the amount of lines.
import webbrowser as wb
import time
from weather import *


def speech():
    r = sr.Recognizer()

    with sr.Microphone() as source:  # This enables the microphone to be used.
        r.adjust_for_ambient_noise(source)
        print("Speak Now: ")
        audio = r.listen(source)  # Listening to the audio source and saving it under the variable source.
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
              ". The high will be " + forecast.high + "\u00b0. The low will be " + forecast.low + "\u00b0.")


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
    print("Options:\n"
          "1) Message Recorder\n"
          "2) Spelling Bee\n"
          "3) Google Search\n"
          "4) Time of Day and Weather\n"
          "Please Dictate Your Choice: ")
    time.sleep(2)
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


menu()

# COULD BE USED
# NEED TO DIFFERENTIATE BETWEEN TYPED AND DICTATED INPUTS
# Learn how to change languages
# x = k.wait('esc')
# k.wait(hotkey=None, suppress=False, trigger_on_release=False)
