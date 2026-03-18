from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import os
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
 
app = FastAPI()
 
templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "templates"))
 
@app.get("/html")
def html_test():
    html = "<html><head><meta charset=\"utf-8\"></head><body>"
    html += "<marquee>fast api 공부중!! </marquee>"
    html += "</body></html>"
    return HTMLResponse(html)
 
@app.get('/items', response_class=HTMLResponse)
def form_page(request: Request):
    return templates.TemplateResponse('form.html',{"request": request})

# ... : 필수값. 반드시 들어와야하는 값, ... 대신 기본값 작성 가능
@app.post('/submit')  #form에서 넘어온 객체임을 표현, form데이터 전달된 것 중 name을 저장할 것
def submit(name:str = Form(...), age:int = Form(0),age2:int = Form(0)): 
    return {'name':name, 'age':age, 'age2':age2}