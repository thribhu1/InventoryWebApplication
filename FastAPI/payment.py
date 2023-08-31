from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from redis_om import get_redis_connection, HashModel
from pydantic import BaseModel
from starlette.requests import Request
import requests, time

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=['http://localhost:3000'],
    allow_methods=['*'],
    allow_headers=['*']
)

redis = get_redis_connection(
    host="redis-16058.c258.us-east-1-4.ec2.cloud.redislabs.com",
    port=16058,
    password="mOx2y1u8MY53J7lwdbmaFnpI3VU7TMGj",
    decode_responses=True
)

class Order(HashModel):
  product_id: str
  price: int
  fee: float
  total: float
  quantity: int
  status: str #pending, completed, refunded

  class Meta:
    database: redis


  async def create(request: Request):
    body = await request.json()

    req = requests.get('http://localhost:8000/products/%s' % body['id'])
    return req.json()
