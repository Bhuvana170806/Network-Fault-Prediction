import numpy as np
import pandas as pd
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense
from sklearn.preprocessing import MinMaxScaler

# Load data
df = pd.read_csv("data.csv")

# Create fault label
df['fault'] = df.apply(lambda row: 1 if row['latency'] > 50 or row['packet_loss'] > 10 else 0, axis=1)

# Select features
data = df[['cpu', 'latency', 'packet_loss']].values

# Normalize data
scaler = MinMaxScaler()
data = scaler.fit_transform(data)

# Create sequences
X = []
y = []

seq_length = 3

for i in range(len(data) - seq_length):
    X.append(data[i:i+seq_length])
    y.append(df['fault'].values[i+seq_length])

X = np.array(X)
y = np.array(y)

# Build LSTM model
model = Sequential()
model.add(LSTM(50, input_shape=(seq_length, 3)))
model.add(Dense(1, activation='sigmoid'))

model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

# Train
model.fit(X, y, epochs=20, verbose=1)

# Test prediction
sample = X[-1].reshape(1, seq_length, 3)
prediction = model.predict(sample)

print("Prediction:", prediction)
if prediction[0][0] > 0.7:
    print("🚨 High Risk: Fault likely soon!")
elif prediction[0][0] > 0.4:
    print("⚠️ Warning: Network degrading")
else:
    print("✅ Network Normal")