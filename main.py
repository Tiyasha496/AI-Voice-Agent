from speech import listen, speak
from agent import ask_ai


def main():

    speak("Hello. I am your AI assistant. I am ready.")

    while True:

        command = listen()

        if not command:
            continue

        if "stop assistant" in command or "exit assistant" in command:
            speak("Goodbye.")
            break

        print("Sending to Gemini...")

        answer = ask_ai(command)

        speak(answer)


if __name__ == "__main__":
    main()