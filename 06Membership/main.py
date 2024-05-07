import mysql.connector
from dotenv import load_dotenv
import os
from fastapi import FastAPI, Request, Form
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from starlette.middleware.sessions import SessionMiddleware
import uvicorn

app = FastAPI()

app.add_middleware(SessionMiddleware,
                   secret_key="APP_AUTHORIZED", max_age=3600)  # 10 mins valid

app.mount("/static", StaticFiles(directory="static"), name='static')

templates = Jinja2Templates(directory='templates')

@app.get("/", response_class=HTMLResponse)
async def read_item(request: Request):
    if len(request.session.keys()) == 0:  # switch the flag to False if there's no flag
        request.session.update({"SIGNED-IN": False})
    return templates.TemplateResponse(
        # Declare a Request parameter in the path operation that will return a template.
        request=request,
        name='home.html',
        status_code=200
    )

if __name__ == "__main__":
   uvicorn.run("main:app",host = "127.0.0.1", port= 8000, log_level="info")

# load in environment variables in .env
load_dotenv()
password = os.getenv('password')

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password=password
)

mycursor = mydb.cursor()
# mycursor.execute("CREATE DATABASE MEMBERSHIP")
mycursor.execute("SHOW DATABASES")

for x in mycursor:
  print(x)

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password=password,
    database="membership"
)
mycursor = mydb.cursor()
