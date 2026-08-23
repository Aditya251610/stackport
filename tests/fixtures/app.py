import time

print("Test application started", flush=True)

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("Test application stopped", flush=True)