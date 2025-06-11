import os
import queue
import sounddevice as sd
import vosk
import json
import pyttsx3
import sys
# پشتیبانی از چاپ فارسی
sys.stdout.reconfigure(encoding='utf-8')
# === مسیر مدل vosk انگلیسی ===
model_path = "model-en"
if not os.path.exists(model_path):
    print(" Model folder not found. Please download the model.")
    exit(1)

model = vosk.Model(model_path)
q = queue.Queue()

# === پاسخ‌های ساده ===
responses = {
    "hello": "Hello! I'm your offline voice assistant. How can I help you?",
    "hi": "Hi there! What do you need today?",
    "how are you": "I'm fine, thank you for asking!",
    "what is your name": "My name is OVA, Offline Voice Assistant.",
    "goodbye": "Goodbye! Feel free to ask me anything anytime.",
    "exit": "Goodbye! Feel free to ask me anything anytime."
}

# === موتور TTS ===
engine = pyttsx3.init()
engine.setProperty('rate', 150)

# === انتخاب دستگاه ورودی ===
def get_input_device():
    print(" Available input devices:")
    devices = sd.query_devices()
    input_devices = []

    for i, dev in enumerate(devices):
        if dev['max_input_channels'] > 0:
            print(f"{i}: {dev['name']}")
            input_devices.append(i)

    while True:
        try:
            selected = int(input(" Enter device index: "))
            if selected in input_devices:
                return selected
            else:
                print(" Invalid input device.")
        except Exception:
            print(" Invalid input.")

# === تابع گوش دادن ===
def callback(indata, frames, time, status):
    if status:
        print("[Error]", status)
    q.put(bytes(indata))

# === پاسخ‌دهی ===
def respond(text):
    print(f" You said: '{text}'")
    answer = responses.get(text.lower(), "Sorry, I didn't understand that.")
    print(f" OVA: {answer}")
    engine.say(answer)
    engine.runAndWait()

# === شروع گوش دادن ===
def listen_and_respond():
    device_id = get_input_device()
    device_info = sd.query_devices(device_id)
    samplerate = int(device_info['default_samplerate'])

    print(f" Listening from: {device_info['name']} ({samplerate} Hz)\n")

    try:
        with sd.InputStream(device=device_id, samplerate=samplerate, blocksize=8000,
                            dtype='int16', channels=1, callback=callback):
            rec = vosk.KaldiRecognizer(model, samplerate)

            while True:
                data = q.get()
                if rec.AcceptWaveform(data):
                    result = json.loads(rec.Result())
                    text = result.get("text", "")
                    if text:
                        print(f"📥 You said: {text}")
                        respond(text)
    except Exception as e:
        print(" Error:", e)

# === اجرای برنامه ===
if __name__ == "__main__":
    print(" Offline Voice Assistant (OVA) is ready!")
    print("Type any of these commands:")
    print(", ".join(responses.keys()))
    print("Speak now...")

    try:
        listen_and_respond()
    except KeyboardInterrupt:
        print(" Program exited by user.")