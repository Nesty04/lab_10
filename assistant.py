import requests
import pyttsx3
import pyaudio
import vosk
import json

def greet():
    speak('Вас приветствует голосовой ассистент! Вот мои команды')
    print("1. Занятие\n2. Тип\n3. Участники\n4. Новое\n5. Сохрани\n")


def show_random_activity():
    activity = requests.get("https://www.boredapi.com/api/activity").json()
    speak(f"Ваше занятие: {activity['activity']}")
    print(f"Ваше занятие: {activity['activity']}")


def say_type():
    activity = requests.get("https://www.boredapi.com/api/activity").json()
    speak(f"Тип занятия: {activity['type']}")
    print(f"Тип занятия: {activity['type']}")


def say_participants():
    activity = requests.get("https://www.boredapi.com/api/activity").json()
    speak(f"Количество участников: {activity['participants']}")
    print(f"Количество участников: {activity['participants']}")


def generate_new_activity():
    speak("Генерирую новое занятие...")
    return show_random_activity()


def create_file():
    with open("result.txt", "w") as file:
        activity = requests.get("https://www.boredapi.com/api/activity").json()
        file.write(f"Your activity: {activity['activity']}\n" +
                f"Type: {activity['type']}\n"+
                f"Participants: {activity['participants']}"
                )
    speak("Запись сохранена")
    print("Ваша запись сохранена в файл 'result.txt'")



def main():
    while True:
        command = recognize_speech().lower()
        print(command)
        if "привет" in command:
            greet()
        elif "занятие" in command:
            show_random_activity()
        elif "тип" in command:
            say_type()
        elif "участники" in command:
            say_participants()
        elif "новое" in command:
            generate_new_activity()
        elif "сохрани" in command:
            create_file()
        else:
            speak("Команда не распознана, повторите.")


# Функция для преобразования текста в речь
def speak(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()


# Функция для распознавания речи
def recognize_speech():
    model = vosk.Model("model")
    recognizer = vosk.KaldiRecognizer(model, 16000)

    p = pyaudio.PyAudio()
    stream = p.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=8000)

    stream.start_stream()
    while True:
        data = stream.read(4000)
        if len(data) == 0:
            break
        if recognizer.AcceptWaveform(data):
            result = json.loads(recognizer.Result())
            return result['text']

    stream.stop_stream()
    stream.close()
    p.terminate()


if __name__ == "__main__":
    main()
