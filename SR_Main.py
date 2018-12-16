import speech_recognition as sr  # This import allows for the function to be used multiple times, condesing the amount of lines.
import webbrowser as wb


def speech():
    r = sr.Recognizer()

    with sr.Microphone() as source:  # This enables the microphone to be used.
        print("Say Something: ")
        audio = r.listen(source)  # Listening to the audio source and saving it under the variable source.
        try:  # Used to verify that the audio is clear
            text = r.recognize_google(audio)
            print("You said: " + str(text))
        except:
            print("Could not recognize that input")


def search():
    inquiry = input("What do you want to search on Google: ")
    wb.open_new_tab('http://google.com/?q=%s' % inquiry)  # the % appends the string onto the search
    g = ("http://groodle.greenwoodcollege.com/")


speech()


# COULD BE USED
# phrase_time_limit = input(int("How long will you be speaking for: "))
# Learn how to change languages
# File IO
