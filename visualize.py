import pandas as pd
import matplotlib.pyplot as plt

# Load data
df = pd.read_csv("data.csv")

# Plot latency
plt.plot(df['time'], df['latency'], label='Latency')

# Plot packet loss
plt.plot(df['time'], df['packet_loss'], label='Packet Loss')

plt.xlabel("Time")
plt.ylabel("Value")
plt.title("Network Behavior Over Time")

plt.legend()
plt.show()