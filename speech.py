import os
import wave
import winsound

import speech_recognition as sr
from dotenv import load_dotenv
from google import genai


# Load environment variables
load_dotenv()

# Gemini client
client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)


# Speech recognizer
recognizer = sr.Recognizer()

recognizer.pause_threshold = 2.5
recognizer.energy_threshold = 300
recognizer.dynamic_energy_threshold = True
recognizer.non_speaking_duration = 0.8


# =========================
# GEMINI TEXT TO SPEECH
# =========================

def speak(text):

    print("Assistant:", text)

    try:

        response = client.models.generate_content(
           model="gemini-3.8-flash-lite-tts",

            contents=[
                {
                    "role": "user",
                    "parts": [
                        {
                            "text": text,
                            "speech_metadata": {
                                "style": "warm, friendly, natural and conversational"
                            }
                        }
                    ]
                }
            ],

            config={
                "response_modalities": ["AUDIO"],
                "speech_config": {
                    "voice_config": {
                        "voice": "Kore"
                    }
                }
            }
        )

        # Get generated audio
        audio_data = response.candidates[0].content.parts[0].inline_data.data

        # Save temporary WAV file
        filename = "assistant_voice.wav"

        with open(filename, "wb") as f:
            f.write(audio_data)

        # Play through Windows speakers
        winsound.PlaySound(
            filename,
            winsound.SND_FILENAME
        )

    except Exception as e:

        print("Voice generation error:", e)


# =========================
# SPEECH TO TEXT
# =========================

def listen():

    with sr.Microphone() as source:

        print("Adjusting microphone...")

        recognizer.adjust_for_ambient_noise(
            source,
            duration=1
        )

        print("🎤 Listening... Speak your COMPLETE sentence.")

        try:

            audio = recognizer.listen(
                source,
                timeout=None,
                phrase_time_limit=None
            )

        except Exception as e:

            print("Microphone error:", e)

            return ""

    print("Processing your speech...")

    try:

        text = recognizer.recognize_google(audio)

        print("\nYou:", text)

        return text.lower()

    except sr.UnknownValueError:

        print("Sorry, I couldn't understand the speech.")

        return ""

    except sr.RequestError as e:

        print("Speech recognition service unavailable.")

        print(e)

        return ""