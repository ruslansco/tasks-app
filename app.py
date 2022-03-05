from shelve import DbfilenameShelf
from fastapi import FastAPI, Depends, Request, Form, status
#import requirements from Starlette
from starlette.responses import RedirectResponse
from starlette.templating import Jinja2Templates
#import session class
from sqlalchemy.orm import Session
#import model, sessionlocal and engine
import models
from database import SessionLocal, engine


#Create all database tables
models.Base.metadata.create_all(bind=engine)

#Speficy template directory
templates = Jinja2Templates(directory="templates")

#Create app instance
app = FastAPI()

#Create helper function to access DB session.
#Dependency that will be passed to def home - as second argument.
#If DB access is not available, then def home will throw error.
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

#Create a function and decorate with @app.get
@app.get("/status")
def status():
    #We can also define the function as async def home():
    #Returns dict that will be auto-converted to JSON
    return {"Hellow":"World"}


#Use template response with /list route.
#We pass request:Request argument and db which is a session object.
@app.get("/")
def home(request: Request, db: Session = Depends(get_db)):
    #Query the DB for all todos.
    todos = db.query(models.Todo).all()

    #return a template response that needs an html file, the request and todo list.
    return templates.TemplateResponse("base.html",
                                        {"request": request,
                                        "todo_list": todos})


#ADD Function
#New argument - title which is a string that comes from Form and passed as parameter to def add.
@app.post("/add")
def add(request: Request, title: str = Form(...), db: Session = Depends(get_db)):
    #New todo
    new_todo = models.Todo(title=title)
    #Add to the DB
    db.add(new_todo)
    #Commit change
    db.commit()
    #Get URL of the /list page
    url = app.url_path_for("home")

    #returns a redirect response to /list and specify status code
    return RedirectResponse(url=url, status_code=303)

#Update Function with {todo_id} parameter as dynamic argument with the type: int.
@app.get("/update/{todo_id}")
def update(request: Request, todo_id: int, db: Session = Depends(get_db)):
    #Query the DB for todo change
    todo = db.query(models.Todo).filter(models.Todo.id == todo_id).first()
    todo.complete = not todo.complete
    db.commit()

    url = app.url_path_for("home")
    return RedirectResponse(url=url, status_code=302)

#Delete Function with {todo_id} parameter as dynamic argument with the type: int.
@app.get("/delete/{todo_id}")
def delete(request: Request, todo_id: int, db: Session = Depends(get_db)):

    #Query the DB for todo change
    todo = db.query(models.Todo).filter(models.Todo.id == todo_id).first()
    db.delete(todo)
    db.commit()

    url = app.url_path_for("home")

    return RedirectResponse(url=url, status_code=302)

#Create dynamic route
#Argument is in curly braces in the route, so we use the same name there as function argument together with type int.
@app.get("/items/{item_id")
def read_item(item_id: int):
    return {"item_id": item_id}