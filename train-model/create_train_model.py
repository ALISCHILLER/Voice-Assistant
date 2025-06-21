import os
import sys
import pandas as pd
import pickle
import tensorflow as tf
from sklearn.preprocessing import LabelEncoder
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
# ذخیره tokenizer به صورت JSON برای استفاده در اندروید
from tensorflow.keras.preprocessing.text import tokenizer_from_json
import json
# تنظیم خروجی ترمینال برای UTF-8
try:
    sys.stdout.reconfigure(encoding='utf-8')
except:
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# مسیرها
MODEL_DIR = "train-model"
CSV_PATH = os.path.join(MODEL_DIR, "train.csv")
MODEL_PATH = os.path.join(MODEL_DIR, "intent_model.h5")
TOKENIZER_PATH = os.path.join(MODEL_DIR, "tokenizer.pkl")
LABEL_ENCODER_PATH = os.path.join(MODEL_DIR, "label_encoder.pkl")
tokenizer_json_path = os.path.join(MODEL_DIR, "tokenizer.json")

# اطمینان از وجود پوشه مدل
os.makedirs(MODEL_DIR, exist_ok=True)

# بررسی وجود فایل CSV
if not os.path.exists(CSV_PATH):
    print(f"❌ فایل {CSV_PATH} پیدا نشد.")
    sys.exit(1)

# خواندن داده‌ها
df = pd.read_csv(CSV_PATH)

# آماده‌سازی داده‌ها
texts = df['text'].astype(str).tolist()
labels = df['command_type'].astype(str).tolist()

# توکنایزر
vocab_size = 1000
max_length = 10
oov_token = "<OOV>"

tokenizer = Tokenizer(num_words=vocab_size, oov_token=oov_token)
tokenizer.fit_on_texts(texts)
sequences = tokenizer.texts_to_sequences(texts)
padded_sequences = pad_sequences(sequences, maxlen=max_length, padding='post', truncating='post')

tokenizer_json = tokenizer.to_json()
# برچسب‌ها
label_encoder = LabelEncoder()
encoded_labels = label_encoder.fit_transform(labels)
num_classes = len(label_encoder.classes_)

# ساخت مدل
model = tf.keras.Sequential([
    tf.keras.layers.Embedding(input_dim=vocab_size, output_dim=16, input_length=max_length),
    tf.keras.layers.GlobalAveragePooling1D(),
    tf.keras.layers.Dense(32, activation='relu'),
    tf.keras.layers.Dense(num_classes, activation='softmax')
])

model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])

# آموزش
print("🎯 در حال آموزش مدل...")
model.fit(padded_sequences, encoded_labels, epochs=50, verbose=2)
print("✅ آموزش مدل کامل شد.")

# ذخیره مدل
model.save(MODEL_PATH)
print(f"✅ مدل ذخیره شد → {MODEL_PATH}")


with open(tokenizer_json_path, 'w', encoding='utf-8') as f:
    f.write(tokenizer_json)

print(f"✅ tokenizer.json ذخیره شد → {tokenizer_json_path}")

# ذخیره Tokenizer و LabelEncoder
with open(TOKENIZER_PATH, 'wb') as f:
    pickle.dump(tokenizer, f)
with open(LABEL_ENCODER_PATH, 'wb') as f:
    pickle.dump(label_encoder, f)
print("✅ Tokenizer و LabelEncoder ذخیره شدند.")
