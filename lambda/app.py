from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from datetime import datetime
import boto3
import os
from mangum import Mangum

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table(os.getenv("TABLE_NAME", "EnvironmentData"))

class EnvironmentData(BaseModel):
    temperature: float
    humidity: float
    water_temperature: float
    timestamp: str

@app.post("/environment")
async def receive_environment(data: EnvironmentData):
    try:
        table.put_item(
            Item={
                "id": "latest",
                "temperature": data.temperature,
                "humidity": data.humidity,
                "water_temperature": data.water_temperature,
                "timestamp": data.timestamp,
                "created_at": datetime.now().isoformat()
            }
        )
        print(f"저장된 데이터: {data}")
        return {"status": "ok", "message": "Environment data saved to DynamoDB"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to save data: {str(e)}")

@app.get("/environment")
async def get_environment():
    try:
        response = table.get_item(Key={"id": "latest"})
        item = response.get("Item")
        if not item:
            raise HTTPException(status_code=404, detail="No environment data found")
        return {
            "temperature": item["temperature"],
            "humidity": item["humidity"],
            "water_temperature": item["water_temperature"],
            "timestamp": item["timestamp"]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch data: {str(e)}")

handler = Mangum(app)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
