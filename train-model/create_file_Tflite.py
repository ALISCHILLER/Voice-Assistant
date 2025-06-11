import os
import sys
import numpy as np
import tensorflow as tf

# تنظیم خروجی ترمینال برای پشتیبانی از UTF-8
sys.stdout.reconfigure(encoding='utf-8')

# اطمینان از وجود پوشه ذخیره مدل
os.makedirs("train-model", exist_ok=True)

# ------------------------
# بارگذاری مدل آموزش‌دیده
# ------------------------
model_path = "train-model/intent_model.h5"
if not os.path.exists(model_path):
    print("❌ فایل مدل وجود ندارد:", model_path)
    sys.exit(1)

model = tf.keras.models.load_model(model_path)
print("✅ مدل با موفقیت بارگذاری شد.")

# ------------------------
# تابع تولید داده نماینده برای Full Integer Quantization
# ------------------------
def representative_data_gen():
    for _ in range(100):
        data = np.random.randint(1, 1000, size=(1, 10)).astype(np.float32)
        yield [data]

# ------------------------
# 1. تبدیل مدل ساده (بدون کوانتیزیشن)
# ------------------------
converter = tf.lite.TFLiteConverter.from_keras_model(model)
tflite_model = converter.convert()
with open("train-model/intent_model.tflite", "wb") as f:
    f.write(tflite_model)
print("✅ مدل TFLite ساده ذخیره شد.")

# ------------------------
# 2. Dynamic Range Quantization
# ------------------------
converter = tf.lite.TFLiteConverter.from_keras_model(model)
converter.optimizations = [tf.lite.Optimize.DEFAULT]
tflite_dynamic_quant_model = converter.convert()
with open("train-model/intent_model_dynamic_quant.tflite", "wb") as f:
    f.write(tflite_dynamic_quant_model)
print("✅ مدل با Dynamic Range Quantization ذخیره شد.")

# ------------------------
# 3. Float16 Quantization
# ------------------------
converter = tf.lite.TFLiteConverter.from_keras_model(model)
converter.optimizations = [tf.lite.Optimize.DEFAULT]
converter.target_spec.supported_types = [tf.float16]
tflite_fp16_model = converter.convert()
with open("train-model/intent_model_float16.tflite", "wb") as f:
    f.write(tflite_fp16_model)
print("✅ مدل با Float16 Quantization ذخیره شد.")



# ------------------------
# 4. Full Integer Quantization
# ------------------------
converter = tf.lite.TFLiteConverter.from_keras_model(model)
converter.optimizations = [tf.lite.Optimize.DEFAULT]
converter.representative_dataset = representative_data_gen
converter.target_spec.supported_ops = [tf.lite.OpsSet.TFLITE_BUILTINS_INT8]
converter.inference_input_type = tf.uint8
converter.inference_output_type = tf.uint8
tflite_int8_model = converter.convert()
with open("train-model/intent_model_full_integer.tflite", "wb") as f:
    f.write(tflite_int8_model)
print("✅ مدل با Full Integer Quantization ذخیره شد.")

print("✅ تمام مدل‌ها با موفقیت ساخته شدند.")