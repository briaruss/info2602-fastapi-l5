from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from app.auth import AuthDep
from app.main import templates

home_router = APIRouter(tags=["Home"])

@home_router.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return RedirectResponse(url="/login")

@home_router.get("/app", response_class=HTMLResponse)
async def app_dashbaord(request: Request, user: AuthDep):
    return templates.TemplateResponse(
        request=request,
        name="todo.html",
        context={
            "current_user": user
        }
    )