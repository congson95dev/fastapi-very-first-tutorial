from fastapi import FastAPI, Request, Query, Path, Body, Header, status, Form, File, UploadFile, HTTPException, \
    Depends, BackgroundTasks
from enum import Enum
from typing import Union, List, Set, Dict
from pydantic import BaseModel, Required, Field, HttpUrl
from datetime import datetime
from uuid import UUID
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder


# init FastApi by using # app = FastAPI()
# we could use normal app = FastAPI() without declare metadata to it
# or we could declare some metadata to it
# metadata is something like description of the app

# app = FastAPI()

# description of metadata
description = """
ChimichangApp API helps you do awesome stuff. 🚀

## Items

You can **read items**.

## Users

You will be able to:

* **Create users** (_not implemented_).
* **Read users** (_not implemented_).
"""

# create metadata for tags
# then insert it to app = FastAPI() as a metadata
# the tags can be used in below routes
# ex: @app.get("/users/", tags=["unicorns"])
tags_metadata = [
    {
        "name": "unicorns",
        "description": "Operations with users. The **login** logic is also here.",
    },
    {
        "name": "default",
        "description": "Manage items. So _fancy_ they have their own docs.",
        "externalDocs": {
            "description": "Items external docs",
            "url": "https://fastapi.tiangolo.com/",
        },
    },
]


# declare some metadata to app = FastAPI()

# docs_url is to set url to go to swagger, by default, it's "docs"
# so when you go to http://127.0.0.1:8000/docs, it will show the swagger to you
# but when you set docs_url="/docs2
# it will change the path to http://127.0.0.1:8000/docs2
app = FastAPI(
    title="ChimichangApp",
    description=description,
    version="0.0.1",
    terms_of_service="http://example.com/terms/",
    contact={
        "name": "Deadpoolio the Amazing",
        "url": "http://x-force.example.com/contact/",
        "email": "dp@x-force.example.com",
    },
    license_info={
        "name": "Apache 2.0",
        "url": "https://www.apache.org/licenses/LICENSE-2.0.html",
    },
    openapi_tags=tags_metadata,
    # docs_url="/docs2"
)


# @app.get("/")
# def root():
#     return {"message": "Hello World 1"}


# @app.get("/items/{item_id}")
# def read_item(item_id: int):
#     return {"item_id": item_id}


"""ENUM part"""


# use enum to create a "select option" as a field in body
class ModelName1(str, Enum):
    alexnet = "alexnet"
    resnet = "resnet"
    lenet = "lenet"


# we use enum model by transfer it to the function
@app.get("/models/{model_name}")
async def get_model(model_name1: ModelName1):
    if model_name1 == ModelName1.alexnet:
        return {"model_name": model_name1, "message": "Deep Learning FTW!"}

    if model_name1.value == "lenet":
        return {"model_name": model_name1, "message": "LeCNN all the images"}

    return {"model_name": model_name1, "message": "Have some residuals"}


"""End ENUM part"""


# :path is to make sure file_path is a file path, but it doesn't seem to work
@app.get("/files/{file_path:path}")
async def read_file(file_path: str):
    return {"file_path": file_path}


fake_items_db = [{"item_name": "Foo"}, {"item_name": "Bar"}, {"item_name": "Baz"}]


# default value of params, use it by using "=", such as skip: int = 0, so default of "skip" param is 0
# @app.get("/items/")
# async def read_item(skip: int = 0, limit: int = 10):
#     return fake_items_db[skip : skip + limit]


# Union mean the type of the variable can be any of those type inside Union
# this could be use as validation for variable type
# @app.get("/items/{item_id}")
# async def read_item(item_id: str, q: Union[None, int, str] = None, short: bool = False):
#     item = {"item_id": item_id}
#     if q:
#         item.update({"q": q})
#     if not short:
#         item.update(
#             {"description": "This is an amazing item that has a long description"}
#         )
#     return item


# HttpUrl is a validate of an url
class Image(BaseModel):
    url: HttpUrl
    name: str


# base model

# !important: In the model, we do not use comma ",", it will break the model some how

# we can use Field in Model, it has every feature that Query, Path and Body have, such as validate

# we can also declare other type of variable as an item of model
# such as tags column below, it used List, or tags2 column, it used Set
# So the result will be like:
# {
#   "item": {
#     "name": "string",
#     "description": "some string",
#     "price": 1.0,
#     "tax": 1.0,
#     "tags": [1, 2],
#     "tags2": [1, 2]
#   }
# }

# we can also call another model in this model, it called "Nested Model"
# Ex, we call Image model in this Item model as an "image" field

# images is a list of Image Model

# we can set example for each field by using Field(example="some data")
class Item(BaseModel):
    name: str
    description: Union[str, None] = Field(
        default=None, title="The description of the item", min_length=10, max_length=300
    )
    price: float = Field(example=0.5)
    tax: Union[float, None] = None
    tags: List[str] = []
    tags2: Set[str] = set()
    image: Union[Image, None] = None
    images: Union[List[Image], None] = None

    # set example data for Model, it will show at swagger
    # syntax are:
    # class Config:
    #     schema_extra = {
    #         "example": {
    #             "your_field": "some data"
    #         }
    #     }

    class Config:
        schema_extra = {
            "example": {
                "name": "string",
                "description": "some string",
                "price": 0,
                "tax": 0,
                "tags": [],
                "tags2": [],
                "image": {
                    "url": "http://a.com",
                    "name": "string"
                },
                "images": [
                    {
                        "url": "http://a.com",
                        "name": "string"
                    },
                    {
                        "url": "http://a.com",
                        "name": "string"
                    }
                ]
            }
        }


# create the first data for Item model
# and add additional value "price_with_tax" to the result
@app.post("/create_item/")
async def create_item(item: Item):
    # transfer model to dict
    item_dict = item.dict()
    if item.tax:
        price_with_tax = item.price + item.tax
        # update a dict by using dict.update()
        item_dict.update({"price_with_tax": price_with_tax})
    return item_dict


# update value "q" to the result
# @app.put("/items/{item_id}")
# async def create_item(item_id: int, item: Item, q: Union[str, None] = None):
#     result = {"item_id": item_id, **item.dict()}
#     if q:
#         result.update({"q": q})
#     return result


# use Union to validate param type
# use Query to validate length of param
# use Required to validate required
# @app.get("/items/")
# async def read_items(q: Union[str, None] = Query(default=Required, min_length=3, max_length=50)):
#     results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
#     if q:
#         results.update({"q": q})
#     return results


# multiple q param (using "List[file_type]" in Union)
# we can validate the element type in List by transfer it inside List, such as List[str, int]
# we also can set default value for multiple q param
# @app.get("/items/")
# async def read_items(q: Union[List[str], None] = Query(default=["foo", "bar"])):
#     query_items = {"q": q}
#     return query_items


# set title, description, alias => metadata for the field
# include_in_schema=False to ignore add this route to schema, i guess, not sure how it work
@app.get("/items/")
async def read_items(
    q: Union[str, None] = Query(
        default=None,
        title="Query string",
        description="Query string for the items to search in the database that have a good match",
        alias="item-query",
        min_length=3,
        # include_in_schema=False
    )
):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results


# use Path to validate, there are some validate that Query doesn't have,
# such as "ge" (greater than or equal), "le" (less than or equal to)
# there are ge, le, gt, lt
# also Path have some feature that Query have, such as "title"
# @app.get("/items/{item_id}")
# async def read_items(*, item_id: int = Path(title="The ID of the item to get", ge=10)):
#     results = {"item_id": item_id}
#     return results


# multiple body param
# we already have Item Model above, so now we created User Model
# class User(BaseModel):
#     username: str
#     full_name: Union[str, None] = None


# transfer Item Model and User Model to body
# now, we can transfer data to body like this:
# {
#     "item": {
#         "name": "Foo",
#         "description": "The pretender",
#         "price": 42.0,
#         "tax": 3.2
#     },
#     "user": {
#         "username": "dave",
#         "full_name": "Dave Grohl"
#     },
#     "importance": 5
# }

# to validate in body, we use Body()
# @app.put("/items/{item_id}")
# async def update_item(item_id: int, item: Item, user: User, importance: int = Body(gt=0)):
#     results = {"item_id": item_id, "item": item, "user": user, "importance": importance}
#     return results


# embed=True is to show item in body as a json element
# by default, if we only have 1 item in body, it will only show the item params, but not the "item" at the first
# Ex:
# {
#   "name": "string",
#   "description": "string",
#   "price": 0,
#   "tax": 0
# }
# with this embed=True, it will show like this:
# {
#   "item": {
#     "name": "string",
#     "description": "string",
#     "price": 0,
#     "tax": 0
#   }
# }
# @app.put("/items/{item_id}")
# async def update_item(item_id: int, item: Item = Body(embed=True)):
#     results = {"item_id": item_id, "item": item}
#     return results

# set multiple examples data
# we can do that by using "examples" inside Body()
# @app.put("/items/{item_id}")
# async def update_item(
#     *,
#     item_id: int,
#     item: Item = Body(
#         examples={
#             "normal": {
#                 "summary": "A normal example",
#                 "description": "A **normal** item works correctly.",
#                 "value": {
#                     "name": "Foo",
#                     "description": "A very nice Item",
#                     "price": 35.4,
#                     "tax": 3.2,
#                 },
#             },
#             "converted": {
#                 "summary": "An example with converted data",
#                 "description": "FastAPI can convert price `strings` to actual `numbers` automatically",
#                 "value": {
#                     "name": "Bar",
#                     "price": "35.4",
#                 },
#             },
#             "invalid": {
#                 "summary": "Invalid data is rejected with an error",
#                 "value": {
#                     "name": "Baz",
#                     "price": "thirty five point four",
#                 },
#             },
#         },
#     ),
# ):
#     results = {"item_id": item_id, "item": item}
#     return results

# UUID is to used as "id" field in database
# @app.put("/items/{item_id}")
# async def read_items(
#     item_id: UUID,
#     start_datetime: Union[datetime, None] = Body(default=None)
# ):
#     return {
#         "item_id": item_id,
#         "start_datetime": start_datetime
#     }


# set this Model to response_model, so it can use this Model as response data

# response_model can work with multiple model, and can return as a List as well
# Ex: response_model=Union[PlaneItem, CarItem] or response_model=List[Item]
class ItemResponse(BaseModel):
    name: str
    description: Union[str, None]
    price: float = None
    tax: Union[float, None] = None


# response_model_exclude_unset is to ignore field which have default value in the response model
# which doesn't actual transferred in the body

# response_model_exclude is to ignore a field you want
# response_model_include is to set the response field you want to get, and ignore all others fields

# status_code can be set as a number, or we can use status.some_http_number, such as status.HTTP_201_CREATED
# @app.post("/items/", response_model=ItemResponse,
#           response_model_exclude_unset=True,
#           response_model_exclude={"tax"},
#           response_model_include={"name", "description"},
#           status_code=status.HTTP_201_CREATED)
# async def create_item(item: Item):
#     return item


# use Form instead of Body or Query, when use Body or Query, it will get the data as JSON
# but when we use Form, the data will be transferred as form data
@app.post("/login/")
async def login(username: str = Form(), password: str = Form()):
    return {"username": username}


# upload file


@app.post("/uploadfile/")
async def create_upload_file(file: UploadFile):
    return {"filename": file.filename, "content_type": file.content_type, "file": file.file}


items = {"foo": "The Foo Wrestlers"}


# raise exception
# @app.get("/items/{item_id}")
# async def read_item(item_id: str):
#     if item_id not in items:
#         raise HTTPException(status_code=404, detail="Item not found")
#     return {"item": items[item_id]}


class Tags(Enum):
    unicorns = "unicorns"
    users = "items"


# custom exception, usually, this custom exception is used for some exception which used over and over again
class UnicornException(Exception):
    def __init__(self, name: str):
        self.name = name


# syntax to custom exception
# @app.exception_handler(some exception)
# we can also do this with other exception such as RequestValidationError
@app.exception_handler(UnicornException)
async def unicorn_exception_handler(request: Request, exc: UnicornException):
    return JSONResponse(
        status_code=418,
        content={"message": f"Oops! {exc.name} did something. There goes a rainbow..."},
    )


# raise custom exception

# add tags to route, so in the swagger, it will group by all the routes in that tag together

# set summary, description and response_description => metadata for route, it will show on swagger
@app.get("/unicorns/{name}", tags=[Tags.unicorns], summary="Create an item",
         description="Create an item with all the information, name, description, price, tax and a set of unique tags",
         response_description="The created item",)
async def read_unicorn(name: str):
    if name == "yolo":
        raise UnicornException(name=name)
    return {"unicorn_name": name}


# convert variable to json
# file type of converted variable is dict
@app.put("/items/{id}")
async def update_item(id: str, item: Item):
    json_compatible_item_data = jsonable_encoder(item)
    print(json_compatible_item_data)
    # => a json variable (or dict variable)
    print(type(item))
    # => main.Item
    print(type(json_compatible_item_data))
    # => dict
    return "check command to see the result"


# create a log file and write a log into it
def write_notification(email: str, message=""):
    with open("log.txt", mode="w") as email_file:
        content = f"notification for {email}: {message}"
        email_file.write(content)


# BackgroundTasks, used to set a task running on background
# so we can still running the main task, but also run the background task behind of it
# it's useful when we need to send email, but still need to return the response
# BackgroundTasks is like a queue in other language
@app.post("/send-notification/{email}")
async def send_notification(email: str, background_tasks: BackgroundTasks):
    background_tasks.add_task(write_notification, email, message="some notification")
    return {"message": "Notification sent in the background"}

# sample data for pytest, check on test_main.py to see how pytest work
fake_secret_token = "coneofsilence"

# sample data for pytest
fake_db = {
    "foo": {"id": "foo", "title": "Foo", "description": "There goes my hero"},
    "bar": {"id": "bar", "title": "Bar", "description": "The bartenders"},
}


# sample data for pytest, check on test_main.py to see how pytest work
class Item1(BaseModel):
    id: str
    title: str
    description: Union[str, None] = None


# sample data for pytest, check on test_main.py to see how pytest work
@app.get("/items/{item_id}", response_model=Item1)
async def read_main(item_id: str, x_token: str = Header()):
    if x_token != fake_secret_token:
        raise HTTPException(status_code=400, detail="Invalid X-Token header")
    if item_id not in fake_db:
        raise HTTPException(status_code=404, detail="Item not found")
    return fake_db[item_id]


# sample data for pytest, check on test_main.py to see how pytest work
@app.post("/items/", response_model=Item1)
async def create_item(item: Item1, x_token: str = Header()):
    if x_token != fake_secret_token:
        raise HTTPException(status_code=400, detail="Invalid X-Token header")
    if item.id in fake_db:
        raise HTTPException(status_code=400, detail="Item already exists")
    fake_db[item.id] = item
    return item
