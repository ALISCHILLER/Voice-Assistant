import sounddevice as sd
import sys



# پشتیبانی از چاپ فارسی در ویندوز
try:
    sys.stdout.reconfigure(encoding='utf-8')
except:
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
# نرخ‌های رایج که می‌خوایم تست کنیم
common_rates = [8000, 16000, 22050, 32000, 44100, 48000]

print("🔍 بررسی دقیق دستگاه‌های ورودی و نرخ‌های پشتیبانی‌شده:\n")

# بررسی همه دستگاه‌ها
for idx, device in enumerate(sd.query_devices()):
    if device['max_input_channels'] > 0:
        print(f"🎤 دستگاه {idx}: {device['name']}")
        print(f"    📌 تعداد کانال ورودی: {device['max_input_channels']}")
        print(f"    🔗 نوع API میزبان: {sd.query_hostapis()[device['hostapi']]['name']}")
        for rate in common_rates:
            try:
                sd.check_input_settings(device=idx, samplerate=rate)
                print(f"      ✅ پشتیبانی می‌کند: {rate} Hz")
            except Exception as e:
                print(f"      ❌ {rate} Hz پشتیبانی نمی‌شود: {str(e).split(':')[0]}")
        print("-" * 60)
