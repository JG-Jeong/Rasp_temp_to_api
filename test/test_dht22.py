#!/usr/bin/env python3
import adafruit_dht
import board
import time

dht_device = adafruit_dht.DHT22(board.D18, use_pulseio=False) # GPIO18

for _ in range(5):
    try:
        temperature = dht_device.temperature
        humidity = dht_device.humidity
        print(f"기온: {temperature}°C, 습도: {humidity}%")
        break
    except RuntimeError as e:
        print(f"오류: {e}")
        time.sleep(2)
