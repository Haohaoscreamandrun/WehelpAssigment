from fastapi import FastAPI, Form, Response
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse
from pydantic import BaseModel
app = FastAPI()
app.mount("/", StaticFiles(directory="static", html= True), name="static")
class Userdata(BaseModel):
    password: str = Form(...)
@app.post("/signin", response_class= JSONResponse)
async def validation(password: Userdata):
    try:
      print("Password received:", password)
      return {"message": "Password received"}
    except:
       print("Not success")