from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name= 'static')

templates = Jinja2Templates(directory= 'templates')

@app.get("/", response_class= HTMLResponse)
async def read_item(request: Request):
  return templates.TemplateResponse(
    request = request, name = 'item.html'
  )
# Declare a Request parameter in the path operation that will return a template.
# Use the templates you created to render and return a TemplateResponse, pass the name of the template, the request object, and a "context" dictionary with key-value pairs to be used inside of the Jinja2 template.
# By declaring response_class=HTMLResponse the docs UI will be able to know that the response will be HTML.
