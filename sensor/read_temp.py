#!/usr/bin/env python3
import adafruit_dht
import board
import time
from w1thermsensor import W1ThermSensor

def read_temperature_and_humidity():
    """DHT22 센서에서 기온과 습도를 읽어 반환 (GPIO18 사용)."""
    dht_device = adafruit_dht.DHT22(board.D18, use_pulseio=False)
    
    max_attempts = 5
    for attempt in range(max_attempts):
        try:
            temperature = dht_device.temperature
            humidity = dht_device.humidity
            if temperature is not None and humidity is not None:
                return temperature, humidity
            else:
                print(f"Attempt {attempt + 1}: Null reading (temp: {temperature}, humidity: {humidity})")
        except RuntimeError as e:
            print(f"Attempt {attempt + 1}: Failed to read DHT22 - {str(e)}")
            time.sleep(2)
        except Exception as e:
            print(f"Attempt {attempt + 1}: Unexpected error - {str(e)}")
            dht_device.exit()
            break
        time.sleep(2)
    
    print("Failed to read temperature and humidity after multiple attempts")
    return None, None

def read_water_temperature():
    """DS18B20 센서에서 수온을 읽어 반환."""
    try:
        sensor = W1ThermSensor()
        return sensor.get_temperature()
    except Exception as e:
        print(f"DS18B20 읽기 오류: {str(e)}")
        return None
