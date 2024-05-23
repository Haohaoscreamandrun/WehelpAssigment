from fastapi import FastAPI, Form, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse, FileResponse
from pydantic import BaseModel, field_validator
from pydantic_core.core_schema import FieldValidationInfo
import os
import re
app = FastAPI()


@app.get("/")
def root():
   # Get the directory of the current file
    current_dir = os.path.dirname(os.path.realpath(__file__))
    # Construct the file path to index.html
    index_html_path = os.path.join(current_dir, "client.html")
    # Return the index.html file as a response
    return FileResponse(index_html_path)


class Userdata(BaseModel):
    password: str

    @field_validator('password')
    def password_rules(cls, v, info: FieldValidationInfo):
        if len(v) < 4 or len(v) > 8:
            raise ValueError("Length of password should be >= 4 and <= 8")
        elif len(re.findall('[^a-zA-Z0-9@#$%]', v)) > 0:
            raise ValueError(
                "Password should only contain a-z, A-Z, 0-9 and #,$,%,@")
        else:
            return v


@app.post("/signin", response_class=JSONResponse)
async def validation(request: Request, password: Userdata):
    try:
        print("Password received:", password)
        return {"message": "Password received"}
    except (Exception, ValueError) as e:
        print("Not success:", str(e))
