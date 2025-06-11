import os
import sys
import pandas as pd
from sklearn.preprocessing import LabelEncoder
import tensorflow as tf
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
import pickle

# تنظیم خروجی ترمینال برای UTF-8
sys.stdout.reconfigure(encoding='utf-8')

# مطمئن شو پوشه مدل وجود داره
os.makedirs("train-model", exist_ok=True)

# مسیر فایل CSV که تو مرحله قبل ساختی
csv_path = "train-model/train.csv"

# خواندن داده‌ها از فایل CSV
df = pd.read_csv(csv_path)

# آماده‌سازی داده‌ها
texts = df['text'].astype(str).tolist()
labels = df['command_type'].astype(str).tolist()

# تنظیمات توکنایزر
vocab_size = 1000
max_length = 10
oov_token = "<OOV>"

tokenizer = Tokenizer(num_words=vocab_size, oov_token=oov_token)
tokenizer.fit_on_texts(texts)

sequences = tokenizer.texts_to_sequences(texts)
padded_sequences = pad_sequences(sequences, maxlen=max_length, padding='post', truncating='post')

# کدگذاری برچسب‌ها
label_encoder = LabelEncoder()
encoded_labels = label_encoder.fit_transform(labels)

# ساخت مدل ساده
model = tf.keras.Sequential([
    tf.keras.layers.Embedding(input_dim=vocab_size, output_dim=16, input_length=max_length),
    tf.keras.layers.GlobalAveragePooling1D(),
    tf.keras.layers.Dense(16, activation='relu'),
    tf.keras.layers.Dense(len(label_encoder.classes_), activation='softmax')
])

model.compile(loss='sparse_categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

# آموزش مدل
epochs = 50
model.fit(padded_sequences, encoded_labels, epochs=epochs, verbose=2)

print("✅ مدل آموزش داده شد.")

# ذخیره مدل
model_save_path = "train-model/intent_model.h5"
model.save(model_save_path)
print(f"✅ مدل Keras در مسیر {model_save_path} ذخیره شد.")

# ذخیره توکنایزر و label encoder
with open('train-model/tokenizer.pkl', 'wb') as f:
    pickle.dump(tokenizer, f)

with open('train-model/label_encoder.pkl', 'wb') as f:
    pickle.dump(label_encoder, f)

print("✅ توکنایزر و کدگذار برچسب‌ها ذخیره شدند.")
