import subprocess
import re

def ping_test(ip):
    result = subprocess.run(["ping", "-n", "5", ip], capture_output=True, text=True)
    
    output = result.stdout
    
    # Extract packet loss
    loss = re.search(r"(\d+)% loss", output)
    packet_loss = int(loss.group(1)) if loss else 0

    # Extract average latency
    latency = re.search(r"Average = (\d+)ms", output)
    avg_latency = int(latency.group(1)) if latency else 0

    return avg_latency, packet_loss

latency, loss = ping_test("192.168.2.2")

print("Latency:", latency)
print("Packet Loss:", loss)