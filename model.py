import pandas as pd

# Load data
df = pd.read_csv("data.csv")

# Fault condition
def detect_fault(row):
    if row['latency'] > 50 or row['packet_loss'] > 10:
        return 1
    return 0

df['fault'] = df.apply(detect_fault, axis=1)

print(df)
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier

# Load data
df = pd.read_csv("data.csv")

# Create fault label
def detect_fault(row):
    if row['latency'] > 50 or row['packet_loss'] > 10:
        return 1
    return 0

df['fault'] = df.apply(detect_fault, axis=1)

# Features & labels
X = df[['cpu', 'latency', 'packet_loss']]
y = df['fault']

# Split data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

# Train model
model = RandomForestClassifier()
model.fit(X_train, y_train)

# Accuracy
print("Accuracy:", model.score(X_test, y_test))

# Test prediction
sample = [[85, 60, 15]]
prediction = model.predict(sample)

print("Prediction for sample:", prediction)
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
import subprocess
import re

# Load dataset
df = pd.read_csv("data.csv")

# Create fault label
def detect_fault(row):
    if row['latency'] > 50 or row['packet_loss'] > 10:
        return 1
    return 0

df['fault'] = df.apply(detect_fault, axis=1)

# Train model
X = df[['cpu', 'latency', 'packet_loss']]
y = df['fault']

model = RandomForestClassifier()
model.fit(X, y)

# 🔥 Real-time ping function
def ping_test(ip):
    result = subprocess.run(["ping", "-n", "5", ip], capture_output=True, text=True)
    output = result.stdout

    loss = re.search(r"(\d+)% loss", output)
    packet_loss = int(loss.group(1)) if loss else 0

    latency = re.search(r"Average = (\d+)ms", output)
    avg_latency = int(latency.group(1)) if latency else 0

    return avg_latency, packet_loss

# Get real data
latency, loss = ping_test("8.8.8.8")

# Fake CPU (for now)
cpu = 60

# Predict
import pandas as pd
model.predict(pd.DataFrame([[cpu, latency, loss]], columns=['cpu','latency','packet_loss']))

print("Latency:", latency)
print("Packet Loss:", loss)

if prediction[0] == 1:
    print("⚠️ Fault Detected!")
else:
    print("✅ Network Normal")
