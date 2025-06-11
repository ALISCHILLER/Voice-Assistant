import os
import queue
import sounddevice as sd
import vosk
import json
import sys
import pyttsx3

# --- پشتیبانی از چاپ فارسی در ویندوز ---
try:
    sys.stdout.reconfigure(encoding='utf-8')
except:
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# === مسیر مدل vosk ===
model_path = "model"
if not os.path.exists(model_path):
    print("❌ پوشه مدل vosk-model-fa-0.42 پیدا نشد.")
    exit(1)

model = vosk.Model(model_path)
q = queue.Queue()

# === پاسخ‌های ساده ===
responses = {
    "سلام": "سلام! من زر هستم. چطور می‌تونم کمک کنم؟",
    "اسمت چیه": "اسم من زر هست. دستیار صوتی فارسی شما.",
    "خداحافظ": "خداحافظ! هر وقت خواستی صدام کن.",
    "حالت چطوره": "من خوبم. مرسی که پرسیدی!"
}

# === موتور تبدیل متن به گفتار ===
engine = pyttsx3.init()
engine.setProperty('rate', 150)

voices = engine.getProperty('voices')
found_persian = False
for voice in voices:
    if "iran" in voice.name.lower() or "persian" in voice.name.lower():
        engine.setProperty('voice', voice.id)
        found_persian = True
        break

if not found_persian:
    print("⚠️ صدای فارسی روی سیستم پیدا نشد. از صدای پیش‌فرض استفاده می‌شود.")

# === تابع تبدیل گفتار به متن ===
def callback(indata, frames, time, status):
    if status:
        print("⛔ خطا در صدا:", status)
    print(".", end="", flush=True)  # نمایش دریافت صدا
    q.put(bytes(indata))

# === پاسخ‌دهی به کاربر ===
def respond(text):
    print(f"🟢 متن دریافتی برای پاسخ‌دهی: '{text}'")
    answer = "متوجه نشدم. لطفاً واضح‌تر بگو."
    for key in responses:
        if key in text:
            answer = responses[key]
            break
    print(f"🤖 زر: {answer}")
    engine.say(answer)
    engine.runAndWait()

# === انتخاب دستگاه ورودی ===
def get_input_device():
    print("📋 لیست دستگاه‌های ورودی صدا:")
    valid_devices = []
    for i, dev in enumerate(sd.query_devices()):
        if dev['max_input_channels'] > 0:
            print(f"🔢 {i}: {dev['name']} (ورودی کانال: {dev['max_input_channels']})")
            valid_devices.append(i)

    while True:
        try:
            selected = int(input("👉 شماره دستگاه میکروفون را وارد کن: "))
            if selected in valid_devices:
                return selected
            else:
                print("❌ دستگاه ورودی صدا ندارد یا نامعتبر است.")
        except Exception:
            print("❌ ورودی اشتباه است. فقط عدد وارد کن.")

# === شروع تشخیص و پاسخ ===
def recognize_and_respond():
    device_id = get_input_device()
    try:
        device_info = sd.query_devices(device_id)
        samplerate = int(device_info['default_samplerate'])

        print(f"\n🎧 زر گوش می‌دهد... ({device_info['name']}, {samplerate} Hz)\n")
        with sd.InputStream(device=device_id, samplerate=samplerate, channels=1,
                            dtype='int16', blocksize=8000, callback=callback):
            rec = vosk.KaldiRecognizer(model, samplerate)
            while True:
                data = q.get()
                if rec.AcceptWaveform(data):
                    result = json.loads(rec.Result())
                    print("📤 نتیجه کامل:", result)  # نمایش برای دیباگ
                    text = result.get("text", "")
                    if text:
                        print(f"📥 گفتی: {text}")
                        respond(text)
    except Exception as e:
        print("❌ خطا در باز کردن ورودی صدا:", e)
        print("📌 لطفاً مطمئن شو دستگاه انتخابی فعال و به درستی وصل است.")

# === اجرای برنامه ===
if __name__ == "__main__":
    try:
        recognize_and_respond()
    except KeyboardInterrupt:
        print("\n🛑 برنامه با فشار دادن Ctrl+C بسته شد.")
    except Exception as e:
        print("❌ خطا در اجرای برنامه:", e)

    engine.stop()
