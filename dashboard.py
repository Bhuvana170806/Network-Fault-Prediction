import streamlit as st
import pandas as pd
import numpy as np
import subprocess
import re
from sklearn.ensemble import RandomForestClassifier

# Title
st.title("🚀 Network Fault Prediction Dashboard")

# Load dataset
df = pd.read_csv("data.csv")

# Create fault label
df['fault'] = df.apply(lambda row: 1 if row['latency'] > 50 or row['packet_loss'] > 10 else 0, axis=1)

# Train model
X = df[['cpu', 'latency', 'packet_loss']]
y = df['fault']

model = RandomForestClassifier()
model.fit(X, y)

# Ping function
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
cpu = np.random.randint(40, 90)

# Predict
prediction = model.predict([[cpu, latency, loss]])

# Display metrics
st.metric("Latency (ms)", latency)
st.metric("Packet Loss (%)", loss)
st.metric("CPU Usage (%)", cpu)

# Prediction result
if prediction[0] == 1:
    st.error("🚨 Fault Detected!")
else:
    st.success("✅ Network Normal")

# Graph
st.line_chart(df[['latency', 'packet_loss']])