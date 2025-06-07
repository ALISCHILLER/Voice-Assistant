import sounddevice as sd
import time
import sys
# پشتیبانی از چاپ فارسی
sys.stdout.reconfigure(encoding='utf-8')
def callback(indata, frames, time_info, status):
    volume_norm = int(abs(indata).max() * 50)
    print("🔊 " + "|" * volume_norm)

def test_microphones():
    devices = sd.query_devices()
    input_devices = [(i, dev['name']) for i, dev in enumerate(devices) if dev['max_input_channels'] > 0]

    print("🎤 لیست ورودی‌های میکروفون:")
    for index, name in input_devices:
        print(f"🔢 {index}: {name}")

    print("\n🔍 حالا هر ورودی رو یکی‌یکی تست می‌کنیم. حرف بزن تا ببینی صدا داره یا نه.\n")

    for index, name in input_devices:
        print(f"🎧 تست {name} (شماره {index}) برای ۵ ثانیه... حرف بزن 👇")
        try:
            with sd.InputStream(device=index, channels=1, callback=callback):
                sd.sleep(5000)  # ضبط به مدت ۵ ثانیه
        except Exception as e:
            print(f"⛔ خطا در ورودی {index}: {e}")
        print("—" * 30)
        time.sleep(1)

    print("✅ تست همه‌ی میکروفون‌ها تمام شد.")

if __name__ == "__main__":
    test_microphones()
