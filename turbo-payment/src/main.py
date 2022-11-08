import time
from typing import Union

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from redis_om import get_redis_connection,HashModel
from starlette.requests import Request
from fastapi.background import BackgroundTasks
import requests

from utils_functions import get_config_file_data
config,config_file = get_config_file_data()
config.read(config_file)

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins = ["http://localhost:3000"],
    allow_methods = ["*"],
    allow_headers = ["*"]
)

redis = get_redis_connection(
    host = config._defaults['redis_host'],
    port = config._defaults['redis_port'],
    password = config._defaults['redis_password'],
    decode_responses= True
)

class Order(HashModel):
    product_id: str
    price: float
    fee: float
    total: float
    quantity: int
    status: str #pending, completed, refunded

    class Meta:
        database = redis

@app.get("/orders")
def all():
    return [format(pk) for pk in Order.all_pks()]

def format(pk:str):
    order = Order.get(pk)
    return {
        'id': order.pk,
        'product_id': order.product_id,
        'price': order.price,
        'fee':order.fee,
        'total': order.total,
        'quantity': order.quantity,
        'status':order.status
     }

@app.get('/orders/{pk}')
def get(pk: str):
    order = Order.get(pk)
    redis.xadd('refund_order', order.dict(), '*')
    return order

@app.post('/orders')
async def create(request: Request, background_task: BackgroundTasks):
    body = await request.json()

    req = requests.get('http://localhost:8000/products/%s' % body['id'])
    product = req.json()

    order = Order(
        product_id = body['id'],
        price = product['price'],
        fee = 0.2 * product['price'],
        total = 1.2 * product['price'],
        quantity = body['quantity'],
        status = 'pending' 
    )

    order.save()

    background_task.add_task(order_completed, order)

    order_completed(order)

    return order

def order_completed(order: Order):
    time.sleep(5)
    order.status = 'completed'
    order.save()
    redis.xadd('order_completed', order.dict(), '*')
