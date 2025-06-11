import speech_recognition as sr
import pyttsx3
from datetime import datetime

# تنظیمات TTS (متن به گفتار)
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)  # صدای زن (اگر وجود داشته باشد)
engine.setProperty('rate', 150)  # سرعت گفتار

def speak(text):
    print("زر: " + text)
    engine.say(text)
    engine.runAndWait()

# تشخیص گفتار به متن
def listen():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("زر منتظر فرامین شماست...")
        audio = r.listen(source)
        try:
            command = r.recognize_google(audio, language='fa-IR')  # تشخیص فارسی
            print("شما گفتید: " + command)
            return command.lower()
        except sr.UnknownValueError:
            speak("نمی‌فهمم، لطفاً دوباره بگویید.")
            return ""
        except sr.RequestError:
            speak("خطا در اتصال به سرور")
            return ""

# منطق دستیار
def handle_command(command):
    if 'سلام' in command:
        speak("سلام، من زر هستم!")

    elif 'چند دقیقه' in command or 'ساعت' in command:
        now = datetime.now().strftime("%H:%M")
        speak(f"ساعت حالا {now} است.")

    elif 'خوبی' in command:
        speak("مرسی از حسن سوال شما، من خوبم.")

    elif 'تشکر' in command:
        speak("خواهش می‌کنم!")

    elif 'خداحافظ' in command or 'بای' in command:
        speak("خداحافظ!")
        exit()

    else:
        speak("متاسفم، فرمان شما را نمی‌فهمم.")

# حلقه اصلی
if __name__ == "__main__":
    speak("من زر هستم، چطور می‌توانم کمکتان کنم؟")
    while True:
        command = listen()
        if command:
            handle_command(command)