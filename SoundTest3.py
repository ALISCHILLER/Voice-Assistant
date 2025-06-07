import sounddevice as sd
import numpy as np
import sys

# پشتیبانی از چاپ فارسی در ویندوز
try:
    sys.stdout.reconfigure(encoding='utf-8')
except:
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
def test_mic(device_index, duration=5):
    device_info = sd.query_devices(device_index, 'input')
    fs = int(device_info['default_samplerate'])
    channels = device_info['max_input_channels']

    print(f"🎧 تست ورودی شماره {device_index} برای {duration} ثانیه با نرخ {fs} هرتز و {channels} کانال...")
    print("حرف بزن 👇")

    try:
        recording = sd.rec(int(duration * fs), samplerate=fs, channels=channels, device=device_index)
        sd.wait()
        volume = np.linalg.norm(recording) / recording.size
        print(f"🔊 حجم صدا: {volume:.4f}")
        if volume < 1e-4:
            print("⚠️ هشدار: صدای ضبط شده بسیار کم یا وجود ندارد.")
    except Exception as e:
        print(f"[خطا] در ورودی {device_index}: {e}")

print(sd.query_devices())  # لیست دستگاه‌ها

test_mic(21)
