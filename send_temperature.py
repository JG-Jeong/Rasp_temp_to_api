#!/usr/bin/env python3
import requests
from datetime import datetime
import sys
import os
import schedule
import time

# 프로젝트 루트를 import 경로에 추가
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, ROOT)
from sensor.read_temp import read_temperature_and_humidity, read_water_temperature

def send_temperature_to_api():
    """기온, 습도, 수온 데이터를 API Gateway로 전송."""
    api_url = "https://<your-api-id>.execute-api.<your-region>.amazonaws.com/Prod/temperature"
    temp, humidity = read_temperature_and_humidity()
    water_temp = read_water_temperature()
    timestamp = datetime.now().isoformat()
    
    if temp is None or humidity is None or water_temp is None:
        print(f"[{timestamp}] 데이터 읽기 실패 (기온: {temp}, 습도: {humidity}, 수온: {water_temp})")
        return
    
    # API 전송 전 데이터 출력
    print(f"[{timestamp}] 측정 데이터 - 기온: {temp:.2f}°C, 습도: {humidity:.2f}%, 수온: {water_temp:.2f}°C")
    
    data = {"temperature": temp, "humidity": humidity, "water_temperature": water_temp, "timestamp": timestamp}
    
    try:
        response = requests.post(api_url, json=data)
        if response.status_code == 200:
            print(f"[{timestamp}] 데이터 전송 성공: 기온 {temp:.2f}°C, 습도 {humidity:.2f}%, 수온 {water_temp:.2f}°C")
        else:
            print(f"[{timestamp}] 데이터 전송 실패: {response.status_code}, {response.text}")
    except Exception as e:
        print(f"[{timestamp}] 전송 오류: {str(e)}")

if __name__ == "__main__":
    # 즉시 데이터 확인
    print("초기 데이터 테스트...")
    send_temperature_to_api()
    
    # 1시간마다 데이터 전송 스케줄링
    schedule.every(1).hours.do(send_temperature_to_api)
    
    print("1시간마다 기온, 습도, 수온 데이터를 전송합니다...")
    while True:
        schedule.run_pending()
        time.sleep(60)
