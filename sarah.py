import signal
import time

def signal_handler(signal, frame):
    
    return

signal.signal(signal.SIGINT, signal_handler)

for i in range(10):
    print(i)
    time.sleep(3)