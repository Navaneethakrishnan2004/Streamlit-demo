import streamlit as st
import speech_recognition as sr
import asyncio
import nest_asyncio
import pyttsx3
from pydub import AudioSegment
from pydub.playback import play
from truecallerpy import search_phonenumber
import pywhatkit
import webbrowser
import random
import pyjokes

nest_asyncio.apply()

# Initialize speech recognizer and text-to-speech engine
recognizer = sr.Recognizer()
engine = pyttsx3.init()

# Function to take user's command
def take_command():
    with sr.Microphone() as source:
        st.write("Listening...")
        recognizer.adjust_for_ambient_noise(source, duration=1)
        audio = recognizer.listen(source)

        try:
            st.write("Recognizing...")
            command = recognizer.recognize_google(audio)
            st.write(f"You said: {command}")
            return command
        except sr.UnknownValueError:
            st.write("Sorry, I didn't understand your command.")
            return ""

# Function to generate speech
def talk(txt):
    st.write(txt)
    engine.say(txt)
    engine.runAndWait()

# Function to get phone number info asynchronously
async def get_phone_number_info(phone_number, country_code, installation_id):
    try:
        response = await search_phonenumber(phone_number, country_code, installation_id)
        if response['status_code'] == 200:
            data = response['data']['data'][0]

            # Extract information
            name = data['name']
            state = data['addresses'][0]['city']
            country = data['addresses'][0]['countryCode']
            email = data['internetAddresses'][0]['id'] if data['internetAddresses'] else 'Not available'
            carrier = data['phones'][0]['carrier'] if data['phones'] else 'Not available'

            # Create and return the information as a dictionary
            sentence = f"Gathering information from the database. I think I got some information. {name} is located in {state}. Email is {email}. Carrier is {carrier}."
   
            return sentence
        else:
            return f"HTTP Status Code: {response['status_code']}"
    except Exception as e:
        return str(e)

# Streamlit App
def main():
    st.title("Voice Assistant App")
    st.write("Hello Nanba, How can I help You?")

    while True:
        command = take_command().lower()

        if 'good morning' in command:
            wishes = ["Wishing you a very Good Morning! A new blessing, a new hope, a new light and a new day is waiting for you to conquer it.",
                      "A very Good Morning! I hope this morning brings a bright smile on your face. May you have a beautiful and rewarding day! Always keep smiling.",
                      "Life is a mystery and things always look impossible until it is made. Do not stop, move ahead and kill it. Good Morning, have a nice day!",
                      "Good Morning! It is a bright day. Wake up every morning with an assurance that you can do it. Think positive, stay happy and keep going"]
            talk(random.choice(wishes))

        elif 'good afternoon' in command:
            wishes = ["I wish you a lovely afternoon and a beautiful day.",
                      "Wishing for your afternoon to be wonderful, cozy, and happy. Have a great one, dear.",
                      "May this afternoon bring a lot of pleasant surprises for you and fill your heart with infinite joy. Wishing you a very warm and love-filled afternoon!",
                      "May your Good afternoon be light, blessed, enlightened, productive, and happy."]
            talk(random.choice(wishes))

        elif 'good evening' in command:
            wishes = ["Good evening! I hope you had a good and productive day. Cheer up!",
                      "No matter how bad your day has been, the beauty of the setting sun will make everything serene. Good evening.",
                      "I am wishing you an amazing evening full of gossips and coffee. Just know that you are always in my mind. Enjoy this evening to the fullest!"]
            talk(random.choice(wishes))

        elif 'good night' in command:
            wishes = ["You have so many reasons to thank God, but first thank him for such a peaceful night like this. What a blissful night for a good sleep. Good night!",
                      "May you have sound sleep and wake up tomorrow with new hopes and a lot of positive energy. Good night to you!",
                      "Wishing you good night and rest well, dear friend. Stop worrying about life. I will always have your back no matter what.",
                      "May tomorrow be sunny and full of joy. Good night!"]
            talk(random.choice(wishes))

        elif 'search' in command:
            st.write("What do you want to search?")
            query = take_command().replace('search', '').strip()
            st.write(f"Searching {query} on Google...")
            pywhatkit.search(query)

        elif 'joke' in command:
            talk(pyjokes.get_joke())

        elif 'hello' in command:
            talk("Hi Nanba! How was the day?")

        elif 'sad' in command or 'bad' in command or 'nothing much' in command:
            wishes = ["i wish to have a arms to hug you and say, iam there for you","Please don’t be sad","A certain darkness is needed to see the stars.","Don’t let little stupid things break your happiness","Breathe. It’s only a bad day, not a bad life"]
            talk(random.choice(wishes))
            talk("can i play a song for you Nanba?")
            des = take_command()
            if "yes" in des:
                options = ["https://www.youtube.com/results?search_query=pachai+kiligal+tholodu","https://www.youtube.com/watch?v=Pj-qgL2nKvs","https://www.youtube.com/watch?v=sJIC5Yyc5dI","https://www.youtube.com/watch?v=uQqk9XsVxjI","https://www.youtube.com/watch?v=zLcrEO-eIOQ"]
                webbrowser.open_new(random.choice(options))
            else:
                talk("ok Nanba")

        elif 'happy' in command or 'good' in command:
            wishes = ["im so glad to hear from you Nanba, your smile make me happy too","im so glad to hear from you Nanba,Be happy for this moment. This moment is your life","im so glad to hear from you Nanba,The best way to pay for a lovely moment is to enjoy it","im so glad to hear from you Nanba,Sometimes your joy is the source of your smile, but sometimes your smile can be the source of your joy"]
            talk(random.choice(wishes))
            talk("can i play a song for you Nanba?")
            des = take_command()
            if "yes" in des:
                options = ["https://www.youtube.com/results?search_query=pachai+kiligal+tholodu","https://www.youtube.com/watch?v=Pj-qgL2nKvs","https://www.youtube.com/watch?v=sJIC5Yyc5dI","https://www.youtube.com/watch?v=uQqk9XsVxjI","https://www.youtube.com/watch?v=zLcrEO-eIOQ"]
                webbrowser.open_new(random.choice(options))
            else:
                talk("ok Nanba")
        elif 'angry' in command:
            wishes = ["calm down Nanba, no matter how angry you get , you end up forgiving the people you love","calm down Nanba,The smarter you get, the more you realize anger is not worth it","Never waste a minute thinking about people you don’t like. Dwight D. Eisenhower"]
            talk(random.choice(wishes))

        elif 'sing' in command:
            talk('I see treeeees of greeeen. red roses tooooo, I watch them bloooom for me and you . And I think to '
                'myself. what a wonderful wooorld')

        elif "you doing" in command:
            response = ["I’m doing great (thanks). How about you?", "Doing good. You?", 'Doing pretty good. You?']
            talk(random.choice(response))

        elif 'how are you' in command or 'how r u' in command:
            response = ["I’m good, thanks. You?","I’m pretty good. What’s new with you?","Never been better. What about you?"]
            talk("i'm Bloody Sweet, What About You?")

        elif 'i am fine' in command:
            talk("happy to hear that Nanba , how can i help you?")

        elif "wait a minute" in command or "minute" in command:
            talk("im always here to help you")

        elif 'trace' in command or 'track' in command:
            st.write("Say the phone number Nanba, I'll trace it for you")
            my_string = take_command()
            
            phone_number = "+91" + my_string.strip()
            country_code = "IN"
            installation_id = "a1i0_--mgx3BLFBkt1HTBo23L7sP9-FrqJGLPdBRJG4oPSXIWvVGZEfY77FxLhTb"

            info_result = asyncio.run(get_phone_number_info(phone_number, country_code, installation_id))
            
            output = str("  "+info_result+"")
            talk(output)

        elif 'want to know about' in command:
            st.write("Can I help you Nanba, whom you want to know about?")
            my_string = take_command()
            pearson(my_string)

        elif "hi" in command or "hay" in command:
            talk("hello nanba, how can i help you? ")

        elif "are you there" in command:
            talk("Yes Nanba, how can i help you")

        elif "wish me" in command:
            wishes = ["wish you happy life","wishing you all the best","im so proud of you","i wish you luck","You've worked hard for this, i believe in you "]
            talk(random.choice(wishes))
        elif "dice" in command:
            options = [1,2,3,4,5,6]
            talk(random.choice(options))

        elif "coin" in command:
            options = ["head","tail"]
            talk(random.choice(options))

        elif "worst" in command:
            talk("sorry Nanba, im doing my best")

        elif"your bad"in command:
            talk("Sorry Nanba , i will try to change")

        elif 'sleep' in command:
            talk("bye Nanba, have a good day")
            break

        elif 'Thank you' in command:
            talk("I am glad to help you all the time")
            break
            
        else:
            talk('Sorry nanba, I didnt get you.')
            st.write('Sorry nanba, I didnt get you.')


