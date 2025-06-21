import os
import sys
import numpy as np
import tensorflow as tf

# تنظیم خروجی UTF-8 برای ترمینال
try:
    sys.stdout.reconfigure(encoding='utf-8')
except:
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# مسیرها
MODEL_DIR = "train-model"
MODEL_PATH = os.path.join(MODEL_DIR, "intent_model.h5")

# بررسی وجود مدل
if not os.path.exists(MODEL_PATH):
    print(f"❌ فایل مدل وجود ندارد: {MODEL_PATH}")
    sys.exit(1)

# بارگذاری مدل
model = tf.keras.models.load_model(MODEL_PATH)
print("✅ مدل با موفقیت بارگذاری شد.")

# ------------------------------
# داده نماینده برای کوانتیزیشن - اصلاح شده به float32
# ------------------------------
def representative_data_gen():
    for _ in range(100):
        data = np.random.randint(1, 1000, size=(1, 10)).astype(np.float32)
        yield [data]

# ------------------------------
# تابع ذخیره مدل TFLite
# ------------------------------
def save_tflite_model(converter: tf.lite.TFLiteConverter, filename: str):
    tflite_model = converter.convert()
    with open(os.path.join(MODEL_DIR, filename), "wb") as f:
        f.write(tflite_model)
    print(f"✅ ذخیره شد → {filename}")

# ------------------------------
# 1. مدل TFLite معمولی
# ------------------------------
converter = tf.lite.TFLiteConverter.from_keras_model(model)
save_tflite_model(converter, "intent_model.tflite")

# ------------------------------
# 2. Dynamic Range Quantization
# ------------------------------
converter = tf.lite.TFLiteConverter.from_keras_model(model)
converter.optimizations = [tf.lite.Optimize.DEFAULT]
save_tflite_model(converter, "intent_model_dynamic_quant.tflite")

# ------------------------------
# 3. Float16 Quantization
# ------------------------------
converter = tf.lite.TFLiteConverter.from_keras_model(model)
converter.optimizations = [tf.lite.Optimize.DEFAULT]
converter.target_spec.supported_types = [tf.float16]
save_tflite_model(converter, "intent_model_float16.tflite")

# ------------------------------
# 4. Full Integer Quantization (با داده float32 چون مدل از float32 استفاده می‌کنه)
# ------------------------------
converter = tf.lite.TFLiteConverter.from_keras_model(model)
converter.optimizations = [tf.lite.Optimize.DEFAULT]
converter.representative_dataset = representative_data_gen
converter.target_spec.supported_ops = [tf.lite.OpsSet.TFLITE_BUILTINS_INT8]
# بدون تعیین نوع ورودی/خروجی چون مدل float32 می‌خواد
save_tflite_model(converter, "intent_model_full_integer.tflite")

print("🎉 تمام مدل‌های TFLite با موفقیت ساخته شدند.")
