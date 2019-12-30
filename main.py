from enum import Enum
from fastapi import FastAPI, Query
from pydantic import BaseModel


class Item(BaseModel):
    name: str
    price: float
    is_offer: bool = None


class ModelName(str, Enum):
    alexnet = "alexnet"
    resnet = "resnet"
    lenet = "lenet"


app = FastAPI()


@app.get("/")
async def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
async def read_item(item_id: int, q: str = Query(None, max_length=20, deprecated=True)):
    return {"item_id": item_id, "q": q}


@app.get("/items/query_required/")
async def read_item_query(
    q: str = Query(
        ...,
        alias="query-alias",
        max_length=10,
        title="Required Query",
        regex=r"^fix\d+$",
        description="An example how to declare a required query using the ... syntax",
    )
):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results


@app.put("/items/{item_id}")
async def put_item(item_id: int, item: Item):
    return {"item_name": item.name, "item_id": item_id}


@app.post("/items/")
async def create_item(item: Item):
    return item


@app.get("/users/me")
async def read_current_user():
    return {"user_id": "the current user"}


@app.get("/users/{user_id}")
async def read_user(user_id: int):
    return {"user_id": user_id}


@app.get("/model/{model_name}")
async def read_model(model_name: ModelName):
    if model_name == ModelName.alexnet:
        return {"model_name": model_name, "message": "Deep learning ftw"}
    if model_name == ModelName.resnet:
        return {"model_name": model_name, "message": "Resnet wohoo"}
    return {"model_name": model_name, "message": "some residuals please"}
