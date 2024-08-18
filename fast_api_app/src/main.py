import os

from fastapi import FastAPI, HTTPException
import redis.asyncio as redis

from utils import Utils
import schemas

app = FastAPI()

client = redis.Redis(
            host='redis', 
            port=6379, username='', 
            password=os.getenv('REDIS_PASSWORD'), 
            encoding="utf8", 
            decode_responses=True
            )

@app.get("/check_data")
async def get_check_data(phone: str):
    if not Utils.check_phone_format(phone):
        raise HTTPException(status_code=400, detail="The wrong phone format")
    
    address = await client.get(phone)

    if not address:
        raise HTTPException(status_code=404, detail="Address not found")
    return {'detail': 'Success', 'address': address}


@app.post("/write_data")
async def post_write_data(write_data: schemas.WriteData):
    phone = write_data.phone

    if not Utils.check_phone_format(phone):
        raise HTTPException(status_code=400, detail="The wrong phone format")
    
    address = await client.get(phone)
    
    if address:
        raise HTTPException(status_code=404, detail="The phone already exists")

    await client.set(phone, write_data.address)
    return  {'detail': 'Success'}


@app.patch("/write_data")
async def update_write_data(write_data: schemas.WriteData):
    phone = write_data.phone

    if not Utils.check_phone_format(phone):
        raise HTTPException(status_code=400, detail="The wrong phone format")

    address = await client.get(phone)
    
    if not address:
        raise HTTPException(status_code=404, detail="Item not found")
    
    await client.set(phone, write_data.address)

    return {'detail': 'Success'}