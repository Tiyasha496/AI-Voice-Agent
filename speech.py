import speech_recognition as sr
import pyttsx3


# Create speech recognizer
recognizer = sr.Recognizer()

# Create text-to-speech engine
engine = pyttsx3.init()

# Adjust these settings
recognizer.pause_threshold = 100
recognizer.phrase_threshold = 0.3
recognizer.non_speaking_duration = 0.5


def speak(text):
    print("Assistant:", text)
    engine.say(text)
    engine.runAndWait()


def listen():

    with sr.Microphone() as source:

        print("\nAdjusting microphone...")
        recognizer.adjust_for_ambient_noise(source, duration=1)

        print("Listening... Speak now!")

        try:
            audio = recognizer.listen(
                source,
                timeout=5,
                phrase_time_limit=8
            )

        except sr.WaitTimeoutError:
            print("No speech detected.")
            return ""

    try:

        text = recognizer.recognize_google(audio)

        print("You:", text)

        return text.lower()

    except sr.UnknownValueError:

        print("Sorry, I couldn't understand that.")

        return ""

    except sr.RequestError:

        print("Speech recognition service is unavailable.")

        return ""


if __name__ == "__main__":

    speak("Hello. I am ready. Please say something.")

    command = listen()

    if command:
        speak("You said " + command)
    else:
        speak("I didn't hear you.")