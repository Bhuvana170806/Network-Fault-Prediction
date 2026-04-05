import numpy as np
import pandas as pd
import time
import subprocess
import re
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense
from sklearn.preprocessing import MinMaxScaler

# Load dataset
df = pd.read_csv("data.csv")

# Label fault
df['fault'] = df.apply(lambda row: 1 if row['latency'] > 50 or row['packet_loss'] > 10 else 0, axis=1)

data = df[['cpu', 'latency', 'packet_loss']].values

# Normalize
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

# Build model
model = Sequential()
model.add(LSTM(50, input_shape=(seq_length, 3)))
model.add(Dense(1, activation='sigmoid'))

model.compile(optimizer='adam', loss='binary_crossentropy')

model.fit(X, y, epochs=10, verbose=0)

# Ping function
def ping_test(ip):
    result = subprocess.run(["ping", "-n", "5", ip], capture_output=True, text=True)
    output = result.stdout

    loss = re.search(r"(\d+)% loss", output)
    packet_loss = int(loss.group(1)) if loss else 0

    latency = re.search(r"Average = (\d+)ms", output)
    avg_latency = int(latency.group(1)) if latency else 0

    return avg_latency, packet_loss

print("🚀 Real-time Monitoring Started...\n")

# Continuous loop
while True:
    latency, loss = ping_test("1.1.1.1")
    cpu = np.random.randint(40, 90)  # simulated CPU

    sample = np.array([[cpu, latency, loss]])
    sample = scaler.transform(sample)

    sample = sample.reshape(1, 1, 3)
    sample = np.repeat(sample, 3, axis=1)

    prediction = model.predict(sample, verbose=0)

    print(f"Latency: {latency}, Loss: {loss}")

    if prediction[0][0] > 0.7:
        print("🚨 High Risk: Fault likely soon!\n")
    elif prediction[0][0] > 0.4:
        print("⚠️ Warning: Network degrading\n")
    else:
        print("✅ Network Normal\n")

    time.sleep(5)