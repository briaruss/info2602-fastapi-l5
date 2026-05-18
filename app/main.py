import uvicorn
from fastapi import FastAPI
from fastapi.templating import Jinja2Templates
from starlette.middleware.sessions import SessionMiddleware
from starlette_flash import flash, get_messages_for_template

app = FastAPI()
app.add_middleware(SessionMiddleware, secret_key="secret")
templates = Jinja2Templates(directory="templates")
templates.env.globals["get_flashed_messages"] = get_messages_for_template

from app.routers import main_router
app.include_router(main_router)

if __name__ == "__main__":
    uvicorn.run("app.main:app", reload=True)