from fastapi import APIRouter, HTTPException, Request, Form
from fastapi.responses import RedirectResponse, HTMLResponse
from sqlmodel import select
from app.database import SessionDep
from app.models import *
from app.auth import AuthDep
from fastapi import status
from typing import Annotated
from app.main import templates
from starlette_flash import flash

todo_router = APIRouter(tags=["Todo Management"])

@todo_router.post("/todos")
def create_todo_action(request: Request, text: Annotated[str, Form()], db: SessionDep, user: AuthDep):
    user.todos.append(Todo(text=text))
    db.add(user)
    db.commit()
    flash(request).success("Item created successfully")
    return RedirectResponse(url="/app", status_code=status.HTTP_303_SEE_OTHER)

@todo_router.post('/toggle/{id}')
async def toggle_todo_action(request: Request, id: int, db: SessionDep, user: AuthDep):
    todo = db.exec(select(Todo).where(Todo.id == id, Todo.user_id == user.id)).one_or_none()
    if not todo:
        flash(request).error('Invalid id or unauthorized')
    else:
        todo.done = not todo.done
        db.add(todo)
        db.commit()
        flash(request).success(f'Todo { "done" if todo.done else "not done" }!')
    return RedirectResponse(url=request.url_for('app_dashbaord'), status_code=status.HTTP_303_SEE_OTHER)

@todo_router.get('/editTodo/{id}', response_class=HTMLResponse)
def edit_todo_page(request: Request, id: int, db: SessionDep, user: AuthDep):
    todo = db.exec(select(Todo).where(Todo.id == id, Todo.user_id == user.id)).one_or_none()
    if not todo:
        return RedirectResponse(url="/app", status_code=status.HTTP_303_SEE_OTHER)
    return templates.TemplateResponse(
        request=request,
        name="edit.html",
        context={"todo": todo, "current_user": user}
    )

@todo_router.post('/editTodo/{id}')
def edit_todo_action(request: Request, id: int, text: Annotated[str, Form()], db: SessionDep, user: AuthDep):
    todo = db.exec(select(Todo).where(Todo.id == id, Todo.user_id == user.id)).one_or_none()
    if not todo:
        flash(request).error('Invalid id or unauthorized')
    else:
        todo.text = text
        db.add(todo)
        db.commit()
        flash(request).success('Todo updated!')
    return RedirectResponse(url=request.url_for('app_dashbaord'), status_code=status.HTTP_303_SEE_OTHER)

@todo_router.get('/deleteTodo/{id}')
def delete_todo_action(request: Request, id: int, db: SessionDep, user: AuthDep):
    todo = db.exec(select(Todo).where(Todo.id == id, Todo.user_id == user.id)).one_or_none()
    if not todo:
        flash(request).error('Invalid id or unauthorized')
    else:
        db.delete(todo)
        db.commit()
        flash(request).success('Deleted successfully')
    return RedirectResponse(url=request.url_for('app_dashbaord'), status_code=status.HTTP_303_SEE_OTHER)