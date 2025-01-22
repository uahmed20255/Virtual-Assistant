import speech_recognition as aa
import pyttsx3
import pywhatkit
import datetime
import wikipedia
import requests

# Initialize recognizer and text-to-speech engine
listener = aa.Recognizer()
machine = pyttsx3.init()

def talk(text):
    """Converts text to speech."""
    machine.say(text)
    machine.runAndWait()

def input_instructions():
    """Listens to user speech and converts it into a string."""
    global instruction
    instruction = None
    try:
        with aa.Microphone() as origin:
            print('I am listening...')
            speech = listener.listen(origin)
            instruction = listener.recognize_google(speech)
            instruction = instruction.lower()
            if "jarvis" in instruction:
                instruction = instruction.replace('jarvis', '').strip()
                print(f"Command received: {instruction}")
    except Exception as e:
        print(f"Error: {e}")
    return instruction

def get_weather(city):
    """Fetches weather data using wttr.in."""
    try:
        response = requests.get(f"http://wttr.in/{city}?format=3")  # Simple format
        if response.status_code == 200:
            return response.text  # Returns weather as a simple string
        else:
            return "Sorry, I couldn't fetch the weather information."
    except Exception as e:
        return f"Error fetching weather data: {e}"

def play_Jarvis():
    """Runs Jarvis in an infinite loop."""
    while True:
        instruction = input_instructions()
        if not instruction:
            continue

        # Exit command
        if 'stop' in instruction or 'exit' in instruction:
            talk('Goodbye! Have a great day!')
            print('Exiting program...')
            break  # Breaks the while loop to stop the program

        if 'play' in instruction:
            song = instruction.replace('play', '').strip()
            talk(f"Playing {song}")
            pywhatkit.playonyt(song)

        elif 'what is the time' in instruction:
            time = datetime.datetime.now().strftime('%I:%M %p')
            talk(f"Current time is {time}")

        elif 'what is the date today' in instruction:
            date = datetime.datetime.now().strftime('%d/%m/%Y')
            talk(f"Current date is {date}")

        elif 'how are you' in instruction:
            talk('I am fine, thank you. How can I assist you?')

        elif 'what is your name' in instruction:
            talk('I am Jarvis, your virtual assistant. What can I do for you?')

        elif 'who is' in instruction:
            person = instruction.replace('who is', '').strip()
            try:
                info = wikipedia.summary(person, sentences=1)
                print(info)
                talk(info)
            except wikipedia.exceptions.DisambiguationError:
                talk("There are multiple results for that name. Please be more specific.")
            except wikipedia.exceptions.PageError:
                talk("Sorry, I couldn't find information on that topic.")
            except Exception as e:
                print(f"Error: {e}")
                talk("Sorry, I encountered an error while searching.")

        elif 'weather in' in instruction:
            city = instruction.replace('what is the weather in', '').strip()
            weather_info = get_weather(city)
            print(weather_info)
            talk(weather_info)

        else:
            talk('I did not understand that. Could you please repeat?')

# Start the virtual assistant
play_Jarvis()

