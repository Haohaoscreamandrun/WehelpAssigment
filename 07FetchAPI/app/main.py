from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from starlette.middleware.sessions import SessionMiddleware
import uvicorn
from .routers import pages_router, sign_router, message_router, api_router

app = FastAPI()

app.add_middleware(SessionMiddleware,
                   secret_key="APP_AUTHORIZED", max_age=3600)  # 10 mins valid

app.mount("/static", StaticFiles(directory="static"), name='static')
# In FastAPI, the app.mount() function is typically used to mount an ASGI application on a specific path within another ASGI application. However, it seems like you're trying to mount a directory containing static files rather than an ASGI application.

# Mounting routers
app.include_router(pages_router.router)
app.include_router(sign_router.router)
app.include_router(message_router.router)
app.include_router(api_router.router)

templates = Jinja2Templates(directory='templates')

@app.get("/", response_class=HTMLResponse)
async def read_item(request: Request, message: str = None):
    if len(request.session.keys()) == 0:  # switch the flag to False if there's no flag
        request.session.update({"SIGNED-IN": False})
        return templates.TemplateResponse(
            # Declare a Request parameter in the path operation that will return a template.
            request=request,
            name='home.html',
            context={'message': message},
            status_code=200
        )
    elif request.session["SIGNED-IN"] == True:
        return RedirectResponse("/member", status_code=303)
    else:
        return templates.TemplateResponse(
            # Declare a Request parameter in the path operation that will return a template.
            request=request,
            name='home.html',
            context={'message': message},
            status_code=200
        )

if __name__ == "__main__":
   uvicorn.run("main:app",host = "127.0.0.1", port= 8000, log_level="info")


