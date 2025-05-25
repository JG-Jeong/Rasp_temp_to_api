#!/usr/bin/env python3
from w1thermsensor import W1ThermSensor

sensor = W1ThermSensor()
temperature = sensor.get_temperature()
print(f"수온: {temperature:.2f}°C")
