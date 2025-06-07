import sounddevice as sd
import numpy as np
import time
import sys

# پشتیبانی از چاپ فارسی در ویندوز
try:
    sys.stdout.reconfigure(encoding='utf-8')
except:
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# === تنظیمات ضبط ===
duration = 10  # زمان ضبط به ثانیه
samplerate = 44100
channels = 1
frames = []

# === پیدا کردن دستگاه ورودی مناسب ===
def find_input_device(samplerate=44100, dtype='float32'):
    print("🔍 در حال بررسی دستگاه‌های ورودی...")
    for idx, dev in enumerate(sd.query_devices()):
        if dev['max_input_channels'] > 0:
            try:
                with sd.InputStream(device=idx, samplerate=samplerate, channels=1, dtype=dtype):
                    print(f"✅ دستگاه شماره {idx} ({dev['name']}) مناسب است.")
                    return idx
            except Exception as e:
                print(f"❌ دستگاه {idx} ({dev['name']}) پشتیبانی نمی‌شود: {e}")
    print("🚫 هیچ دستگاه ورودی معتبری پیدا نشد.")
    return None

device_id = find_input_device()
if device_id is None:
    sys.exit("❌ هیچ دستگاه ورودی قابل استفاده پیدا نشد.")

print(f"\n🎙️ شروع ضبط از دستگاه شماره {device_id} برای {duration} ثانیه...")

# === تابع دریافت صدا از میکروفون ===
def callback(indata, frames_count, time_info, status):
    if status:
        print(f"⚠️ وضعیت ضبط: {status}")
    if indata.size > 0:
        frames.append(indata.copy())
    else:
        print("❗ هیچ داده‌ای دریافت نشد در این فریم.")

# === شروع ضبط ===
try:
    start_time = time.time()

    with sd.InputStream(samplerate=samplerate,
                        channels=channels,
                        callback=callback,
                        device=device_id,
                        dtype='float32'):
        while time.time() - start_time < duration:
            time.sleep(0.1)

    elapsed_time = time.time() - start_time
    print(f"\n⏱️ زمان واقعی ضبط: {elapsed_time:.2f} ثانیه")

    if len(frames) == 0:
        print("❌ هیچ داده‌ای دریافت نشد!")
        sys.exit(1)

    recording = np.concatenate(frames, axis=0)

    rms = np.sqrt(np.mean(recording**2))
    print(f"✅ ضبط کامل شد. RMS = {rms:.6f}")

    if rms > 0.01:
        print("🔊 صدا با موفقیت دریافت شد.")
    else:
        print("🔇 صدا بسیار کم یا خاموش است. لطفاً میکروفون را بررسی کن.")

except Exception as e:
    print("❌ خطا در هنگام ضبط:", e)

print("📌 اگر مشکلی وجود داشت، لطفاً بررسی کن که میکروفون فعال و به درستی انتخاب شده باشد.")
