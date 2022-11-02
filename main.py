from typing import Union

from fastapi import FastAPI
from redis_om import get_redis_connection

from src.utils_functions import get_config_file_data
config,config_file = get_config_file_data()
config.read(config_file)

app = FastAPI()

redis = get_redis_connection(
    host = config._defaults['redis_host'],
    port = config._defaults['redis_port'],
    password = config._defaults['redis_password']
)

@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}