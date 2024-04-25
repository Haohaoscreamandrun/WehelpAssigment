# Step 1: import FastAPI
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi import FastAPI, Request, Form
from typing_extensions import Annotated


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
# This will set default parameter
# http://127.0.0.1:8000/items/?skip=0&limit=10 is the same as http://127.0.0.1:8000/items/

@app.get("/items/")
async def read_item(skip: int = 0, limit: int = 10):
    return fake_items_db[skip: skip + limit]

# when reboot the server in bash with "uvicorn main:app --reload", make sure to cd to where main.py locates
# main: the file main.py (the Python "module").
# app: the object created inside of main.py with the line app = FastAPI().
# --reload: make the server restart after code changes. Only use for development.


app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name='static')
# The first "/static" refers to the sub-path this "sub-application" will be "mounted" on. So, any path that starts with "/static" will be handled by it.
# The directory="static" refers to the name of the directory that contains your static files.
# The name="static" gives it a name that can be used internally by FastAPI.

templates = Jinja2Templates(directory='templates')
# Create a templates object that you can re-use later.


@app.get("/items/{id}", response_class=HTMLResponse)
async def read_item(request: Request, id: str):
  return templates.TemplateResponse(
      request=request, name='item.html', context={"id": id}
  )
# Declare a Request parameter in the path operation that will return a template.
# Use the templates you created to render and return a TemplateResponse, pass the name of the template, the request object, and a "context" dictionary with key-value pairs to be used inside of the Jinja2 template.
# By declaring response_class=HTMLResponse the docs UI will be able to know that the response will be HTML.

# Form data
@app.post("/login/")
async def login(username: Annotated[str, Form()], password: Annotated[str, Form()]):
   return {"username": username}
# The spec requires the fields to be exactly named username and password, and to be sent as form fields, not JSON.
