from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from redis_om import get_redis_connection, HashModel
from pydantic import BaseModel
import redis


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



class Product(HashModel):
    name: str 
    price: int
    quantity: int

    class Meta():
        database = redis



@app.get('/products')
def all():
    return [format(pk) for pk in Product.all_pks()]


def format(pk: str):
    product = Product.get(pk)

    return {
        'id': product.pk,
        'name': product.name,
        'price': product.price,
        'quantity': product.quantity
    }



@app.post('/products')
async def create(prod_dict: dict):

        prod = Product(
            name=prod_dict['name'],
            price=prod_dict['price'],
            quantity=prod_dict['quantity']
        )
        return prod.save()
        

@app.get('/products/{pk}')
async def get(pk: str):
        return Product.get(pk)


@app.delete('/products/{pk}')
def delete(pk: str):
    return Product.delete(pk)