# Step 1: import FastAPI
from fastapi import FastAPI

# Step 2: create a FastAPI "instance"
## variable name should be change accordingly when refer "uvicorn main:name of the variable --reload"
app = FastAPI()

# Step 3: create a path operation
## Define a path operation decorator
## The @app.get("/") tells FastAPI that the function right below is in charge of handling requests that go to: the path "/" and using a "get" operation
## "@blabla" syntax in Python is called a "decorator". You put it on top of a function. Like a pretty decorative hat.
## A "decorator" takes the function below and does something with it. This decorator tells FastAPI that the function below corresponds to the path / with an operation get.
@app.get("/")
# async function is usually used when there is some variable you need to "await" for
async def root():
  return {"message" : "Hello World"}

# The value of the path parameter item_id will be passed to your function as the argument item_id.
#@app.get("/items/{item_name}")
#async def read_item(item_name):
#  return {"item_id": item_name} # string

# with that type declaration, FastAPI gives you automatic request "parsing".
@app.get("/items/{item_id}")
async def read_item(item_id: int):
    return {"item_id": item_id} # int
# error msg will appear if you try to parse string or float into int.
# Also, when the path mixed, The first one will always be used since the path matches first.
# You should always declare fix path in front of the vary one.

fake_items_db = [{"item_name": "Foo"}, {
    "item_name": "Bar"}, {"item_name": "Baz"}]
# Query parameters
# 
@app.get("/items/")
async def read_item(skip: int = 0, limit: int = 10):
    return fake_items_db[skip: skip + limit]

# when reboot the server in bash with "uvicorn main:app --reload", make sure to cd to where main.py locates
## main: the file main.py (the Python "module").
## app: the object created inside of main.py with the line app = FastAPI().
## --reload: make the server restart after code changes. Only use for development.
