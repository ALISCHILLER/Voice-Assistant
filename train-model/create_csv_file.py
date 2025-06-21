import os
import sys
import pandas as pd
from io import StringIO

# تنظیم خروجی ترمینال برای پشتیبانی از UTF-8
try:
    sys.stdout.reconfigure(encoding='utf-8')
except:
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# ساخت پوشه اگر وجود ندارد
os.makedirs("train-model", exist_ok=True)

# داده‌ها به صورت رشته CSV
csv_content = """text,command_type
چراغ را روشن کن,light_on
روشن کن چراغ را,light_on
چراغ روشن بشه,light_on
چراغ روشنه کن,light_on
لامپ رو روشن کن,light_on
نور اتاق رو زیاد کن,light_on
نور چراغ رو بالا ببر,light_on
چراغ رو خاموش کن,light_off
خاموش کن چراغ را,light_off
چراغ خاموش بشه,light_off
لامپ رو خاموش کن,light_off
نور رو کم کن,light_off
نور چراغ رو قطع کن,light_off
دما را افزایش بده,increase_temperature
دما رو زیاد کن,increase_temperature
هوا رو گرم‌تر کن,increase_temperature
دما باید بره بالا,increase_temperature
یه کم گرم‌ترش کن,increase_temperature
گرما رو زیاد کن,increase_temperature
دما رو کاهش بده,decrease_temperature
دما رو کم کن,decrease_temperature
هوا سردتر بشه,decrease_temperature
یه کم خنکش کن,decrease_temperature
سردش کن,decrease_temperature
دما باید بیاد پایین,decrease_temperature
تلویزیون را روشن کن,tv_on
تلویزیون روشن بشه,tv_on
تی‌وی رو روشن کن,tv_on
دستگاه پخش رو روشن کن,tv_on
نمایشگر رو روشن کن,tv_on
تلویزیون رو خاموش کن,tv_off
خاموش کن تلویزیون رو,tv_off
تی‌وی رو خاموش کن,tv_off
دستگاه رو خاموش کن,tv_off
موزیک پخش کن,play_music
موسیقی بذار,play_music
یه آهنگ پلی کن,play_music
یه آهنگ پخش کن,play_music
صدا بزار,play_music
یه موزیک روشن کن,play_music
موزیک رو متوقف کن,stop_music
موسیقی رو قطع کن,stop_music
پخش آهنگ رو ببند,stop_music
موزیک رو خاموش کن,stop_music
آهنگ رو قطع کن,stop_music
روشن کن کولر را,ac_on
کولر رو روشن کن,ac_on
هوا رو خنک کن,ac_on
باد سرد بزن,ac_on
کولر رو بزن,ac_on
کولر را خاموش کن,ac_off
کولر خاموش بشه,ac_off
خاموش کن کولر را,ac_off
خنک‌کننده رو قطع کن,ac_off
هوا رو گرم کن,ac_off
برو به اتاق نشیمن,go_to_livingroom
به نشیمن برو,go_to_livingroom
حرکت کن به نشیمن,go_to_livingroom
برو سالن پذیرایی,go_to_livingroom
برو سمت نشیمن,go_to_livingroom
برو به آشپزخانه,go_to_kitchen
برو توی آشپزخانه,go_to_kitchen
برو به آشپزخونه,go_to_kitchen
برو سمت آشپزخانه,go_to_kitchen
حرکت کن به آشپزخانه,go_to_kitchen
در را باز کن,open_door
در رو باز کن,open_door
بازش کن,open_door
در باید باز بشه,open_door
در رو لطفاً باز کن,open_door
در را ببند,close_door
در رو ببند,close_door
ببند در رو,close_door
در بسته بشه,close_door
در رو لطفاً ببند,close_door
چراغ خواب را روشن کن,bed_light_on
چراغ خواب روشن بشه,bed_light_on
لامپ خواب روشن کن,bed_light_on
نور خواب رو زیاد کن,bed_light_on
چراغ خواب را خاموش کن,bed_light_off
چراغ خواب خاموش بشه,bed_light_off
نور خواب رو خاموش کن,bed_light_off
لامپ خواب رو خاموش کن,bed_light_off
"""

# تبدیل رشته CSV به DataFrame
df = pd.read_csv(StringIO(csv_content))

# ذخیره DataFrame به فایل CSV با encoding مناسب فارسی
df.to_csv("train-model/train.csv", index=False, encoding="utf-8-sig")

print("فایل train.csv با موفقیت ساخته شد.")
