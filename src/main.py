from typing import Union

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from redis_om import get_redis_connection,HashModel

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

class Product(HashModel):
    name: str
    price: float
    quantity_available: int

    class Meta:
        database = redis

@app.get("/products")
def all():
    return [format(pk) for pk in Product.all_pks()]

def format(pk:str):
    product = Product.get(pk)
    return {
        'id': product.pk,
        'name': product.name,
        'price': product.price,
        'quantity_available':product.quantity_available
     }

@app.post("/products")
def create(product: Product):
    return product.save()

@app.get("/products/{pk}")
def get(pk:str):
    return Product.get(pk)

@app.delete("/products/{pk}")
def delete(pk:str):
    return Product.delete(pk)
