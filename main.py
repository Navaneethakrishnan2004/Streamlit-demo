import streamlit as st
from audio_recorder_streamlit import st_audio_recorder
import asyncio
import nest_asyncio
from truecallerpy import search_phonenumber
import random
import pyjokes
import pywhatkit
import webbrowser
import speech_recognition as sr
import pyttsx3
from pyht import Client
from dotenv import load_dotenv
from pyht.client import TTSOptions
from pydub import AudioSegment
from pydub.playback import play
import io

load_dotenv()

User_id = "XhhM74QLk3Wd6gArrUKCD5vfmYC2"
Api_Key = "54a64e257595419fb21f4ddff90cf810"

client = Client(
    user_id=User_id,
    api_key=Api_Key,
)

engine = pyttsx3.init()
recognizer = sr.Recognizer()

nest_asyncio.apply()

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
            sentence = f"gathering information from the database, ah I think,I got some information. {name} is located in {state}. Email is {email}. Carrier is {carrier}."
   
            return sentence
        else:
            return {'Error': f"HTTP Status Code: {response['status_code']}"}
    except Exception as e:
        return {'Error': str(e)}

def talk(txt):
    options = TTSOptions(voice="s3://voice-cloning-zero-shot/084070b5-e3d8-431c-a0b6-edb09d7356d0/vijay-actor/manifest.json")

    # Request text-to-speech conversion
    audio_generator = client.tts(txt, options)

    # Convert the generator to a list of bytes
    audio_bytes = b''.join(audio_generator)

    # Create an AudioSegment directly from the bytes
    audio = AudioSegment.from_file(io.BytesIO(audio_bytes), format='wav')

    # Play the audio
    play(audio)

def take_command():
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source, duration=1)
        audio = recognizer.listen(source)

        try:
            print("Recognizing...")
            command = recognizer.recognize_google(audio)
            print(f"You said: {command}")
        except sr.UnknownValueError:
            print("Sorry, I didn't understand your command.")
            command = ""
    return command

def main():
    st.title("Voice Assistant App")
    st.write("Hello Nanba, How can I help You?")
    
    with st.echo():
        # Display audio recorder
        audio_bytes = st_audio_recorder(initial_secs=10, recording_secs=20, sample_rate=44100)
        
        # Process the recorded audio
        if audio_bytes is not None:
            # Convert audio bytes to AudioSegment
            audio = AudioSegment.from_file(io.BytesIO(audio_bytes), format="wav")
            
            # Save the recorded audio to a file if needed
            with open("recorded_audio.wav", "wb") as f:
                f.write(audio_bytes)

            # Convert the recorded audio to text
            command = recognize_audio(audio)
            st.write(f"Recognized Command: {command}")

            # Process the recognized command
            process_command(command)

def recognize_audio(audio):
    recognizer = sr.Recognizer()
    with sr.AudioFile(io.BytesIO(audio.raw_data)) as source:
        audio_data = recognizer.record(source)
    try:
        recognized_text = recognizer.recognize_google(audio_data)
        return recognized_text
    except sr.UnknownValueError:
        return ""
    except sr.RequestError as e:
        return ""


def process_command(command):
    if 'good morning' in command:
        wishes = ["Wishing you a very Good Morning!  A new blessing, a new hope, a new light and a new day is waiting for you to conquer it.","A very Good Morning! I hope this morning brings a bright smile on your face. May you have a beautiful and rewarding day! Always keep smiling.","Life is a mystery and things always look impossible until it is made. Do not stop, move ahead and kill it. Good Morning, have a nice day!","Good Morning! It is a bright day. Wake up every morning with an assurance that you can do it. Think positive, stay happy and keep going"]
        talk(random.choice(wishes))
    elif 'good afternoon' in command:
        wishes = ["I wish you a lovely afternoon and a beautiful day.","Wishing for your afternoon to be wonderful, cozy, and happy. Have a great one, dear.","May this afternoon bring a lot of pleasant surprises for you and fills your heart with infinite joy. Wishing you a very warm and love-filled afternoon!","May your Good afternoon be light,blessed,enlightened,productive and happy."]
        talk(random.choice(wishes))
    elif 'good evening' in command:
        wishes = ["Good evening! I hope you had a good and productive day. Cheer up!","No matter how bad your day has been, the beauty of the setting sun will make everything serene. Good evening.","No matter how bad your day has been, the beauty of the setting sun will make everything serene. Good evening.","I am wishing you an amazing evening full of gossips and coffee. Just know that you are always in my mind. Enjoy this evening to the fullest!"]
        talk(random.choice(wishes))
    elif 'good night' in command:
        wishes = ["You have so many reasons to thank God, but first thank him for such a peaceful night like this. What a blissful night for a good sleep. Good night!","May you have sound sleep and wake up tomorrow with new hopes and a lot of positive energy. Good night to you!","Wishing you good night and rest well, dear friend. Stop worrying about life. I will always have your back no matter what.","May tomorrow be sunny and full of joy. Good night!"]
        talk(random.choice(wishes))
    elif 'search' in command:
        talk("What do you want to search for?")
        my_string = take_command()
     
        talk("Okay, I'll search that for you on Google.")
        pywhatkit.search(my_string.replace('search', ''))
    elif 'joke' in command:
        talk(pyjokes.get_joke())
    elif 'hello' in command:
        talk("Hi! How was the day?")
    elif 'sad' in command or 'bad' in command or 'nothing much' in command:
        wishes = ["I wish I could hug you and say, 'I'm here for you.'","Please don’t be sad.","A certain darkness is needed to see the stars.","Don’t let little stupid things break your happiness.","Breathe. It’s only a bad day, not a bad life."]
        talk(random.choice(wishes))
        talk("Can I play a song for you?")
        des = take_command()
        if "yes" in des:
            options = ["https://www.youtube.com/results?search_query=pachai+kiligal+tholodu","https://www.youtube.com/watch?v=Pj-qgL2nKvs","https://www.youtube.com/watch?v=sJIC5Yyc5dI","https://www.youtube.com/watch?v=uQqk9XsVxjI","https://www.youtube.com/watch?v=zLcrEO-eIOQ"]
            webbrowser.open_new(random.choice(options))
        else:
            talk("Okay!")
    elif 'happy' in command or 'good' in command:
        wishes = ["I'm so glad to hear from you! Your smile makes me happy too.","Be happy for this moment. This moment is your life.","The best way to pay for a lovely moment is to enjoy it.","Sometimes your joy is the source of your smile, but sometimes your smile can be the source of your joy."]
        talk(random.choice(wishes))
        talk("Can I play a song for you?")
        des = take_command()
        if "yes" in des:
            options = ["https://www.youtube.com/results?search_query=pachai+kiligal+tholodu","https://www.youtube.com/watch?v=Pj-qgL2nKvs","https://www.youtube.com/watch?v=sJIC5Yyc5dI","https://www.youtube.com/watch?v=uQqk9XsVxjI","https://www.youtube.com/watch?v=zLcrEO-eIOQ"]
            webbrowser.open_new(random.choice(options))
        else:
            talk("Okay!")
    elif 'angry' in command:
        wishes = ["Calm down! No matter how angry you get, you end up forgiving the people you love.","The smarter you get, the more you realize anger is not worth it.","Never waste a minute thinking about people you don’t like. - Dwight D. Eisenhower"]
        talk(random.choice(wishes))
    elif 'sing' in command:
        talk('I see trees of green. Red roses too. I watch them bloom for me and you. And I think to myself, "What a wonderful world!"')
    elif "you doing" in command:
        response = ["I’m doing great (thanks). How about you?", "Doing good. You?", 'Doing pretty good. You?']
        talk(random.choice(response))
    elif 'how are you' in command or 'how r u' in command:
        response = ["I’m good, thanks. You?","I’m pretty good. What’s new with you?","Never been better. What about you?"]
        talk("I'm bloody sweet. What about you?")
    elif 'i am fine' in command:
        talk("Happy to hear that! How can I help you?")
    elif "wait a minute" in command or "minute" in command:
        talk("I'm always here to help you.")
    elif 'trace' in command or 'track' in command:
        talk("Say the phone number and I'll trace it for you.")
        my_string = take_command()
        
        phone_number = "+91" + my_string.strip()
        country_code = "IN"
        installation_id = "a1i0_--mgx3BLFBkt1HTBo23L7sP9-FrqJGLPdBRJG4oPSXIWvVGZEfY77FxLhTb"

        info_result = asyncio.run(get_phone_number_info(phone_number, country_code, installation_id))
        
        output = f"I found some information. {info_result}"
        talk(output)
    elif 'want to know about' in command:
        talk("Can I help you with something? Whom do you want to know about?")
        my_string = take_command()
        pearson(my_string)
    elif "hi" in command or "hay" in command:
        talk("Hello! How can I help you?")
    elif "are you there" in command:
        talk("Yes, I'm here. How can I help you?")
    elif "wish me" in command:
        wishes = ["Wish you a happy life!","Wishing you all the best!","I'm so proud of you!","I wish you luck!","You've worked hard for this. I believe in you!"]
        talk(random.choice(wishes))
    elif "dice" in command:
        options = [1,2,3,4,5,6]
        talk(random.choice(options))
    elif "coin" in command:
        options = ["head","tail"]
        talk(random.choice(options))
    elif "worst" in command:
        talk("Sorry, I'm doing my best.")
    elif "your bad" in command:
        talk("Sorry, I will try to change.")
    elif 'sleep' in command:
        talk("Goodbye! Have a good day.")
    elif 'Thank you' in command:
        talk("I'm glad to help you all the time.")

