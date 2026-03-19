from fastapi import FastAPI, Request, Form, UploadFile, File
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import os
from typing import Optional
# 128비트 길이로 범용 고유 식별자 생성
#파일 업로드 시 이름 충돌 방지, 로그인 세션이나 인증 토큰을 유일하게 만들 때
from uuid import uuid4 
import shutil

BASE_DIR =os.path.dirname(os.path.abspath(__file__))
app = FastAPI()
templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "templates"))

@app.get('/')
def read_root(): return {'message':'hello'}

#GET: /item/정수?q=문자열
@app.get('/item/{item_id}')  
#q로 문자열을 받아온다고 주석에 적었음.해당 파라미터로 넘어오는 값이 없으면 기본값 None으로 처리하라
def read_param(item_id:int, q:str | None = None): # None='없음'으로도 가능
    return{'item_id':item_id, 'q':q} #json형태로 값을 리턴

@app.get('/item', response_class=HTMLResponse)
def form_page(request:Request):
    return templates.TemplateResponse('item_form.html',{'request':request})

@app.post("/item")
def create_item(name:str=Form(...), price:int=Form(0), is_offer:str | None=Form(None)):
    #is_offer 문자열 처리 ("true"->True, ""/None->False)
    is_offer_bool = (is_offer == 'true')
    return{'name':name, 'price':price, 'isDiscount':is_offer_bool}

@app.get('/member', response_class=HTMLResponse)
def member_form_page(request:Request):
    return templates.TemplateResponse('member.html', {'request':request})

@app.post('/member')
def create_member(id:str=Form(...), pw:str=Form(...),gender:str=Form(...),
                  comment:str=Form(...),hobby:list[str]=Form(None)):
            #체크박스 0개 체크 시 422에러 발생 방지 Form(default=[]) 이것도 가능

            #: 이후에 작성. 이렇게도 가능, 값이 없을 수도 있다는 뜻
            #hobby:Optional[list[str]]=Form(default=[])
            #q:str | None=None 해당 표현과 유사한 맥락

            #textarea에서 엔터를 인식하려면 \r\n
            #html에서 줄바꿈을 그대로 표현하고 싶다면 <br>로 변경
    comment = comment.replace('\r\n','<br>')
    return {'id':id,'pw':pw,'gender':gender,'comment':comment,'hobby':hobby}

@app.get('/file.up')
def fileGet(request:Request):
    return templates.TemplateResponse('file_input.html',{'request':request})

@app.post('/file.up')
async def fileUp(title:str = Form(),photo:UploadFile = File(...)):
    #파일 정보
    filename = photo.filename
    content_type = photo.content_type
    #업로드 경로
    folder = os.path.join(BASE_DIR,'upload')
    os.makedirs(folder, exist_ok=True)
    #업로드 될 파일 명(중복 방지)
    ext = filename[-4:]#   .png
    filename = filename.replace(ext,'')+str(uuid4()) + ext
    #파일 내용
    content = await photo.read() # 큰 파일을 로드할 때 시간이 소요될 수 있기때문에 여기에 await
    f = open(folder+'/'+filename, 'wb') # 쓰기 + 바이너리 파일 출력
    f.write(content)
    f.close()
    return {'type':content_type, 'name': filename}

@app.get('/file2.up')
def fileGet(request:Request):
    return templates.TemplateResponse('file_input2.html',{'request':request})

@app.post('/file2.up')
async def fileUp2(title:str = Form(),
           photo:list[UploadFile] = File(...)):
    #업로드 경로
    folder = os.path.join(BASE_DIR,'upload')
    os.makedirs(folder, exist_ok=True)
 
    saved_file_names =[]
    for file in photo:
        filename = file.filename
        ext = filename[-4:]#   .png
        filename = filename.replace(ext,'')+str(uuid4()) + ext
 
        with open(folder+'/'+filename, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
 
        saved_file_names.append(filename)
 
    return {"message":'업로드 성공', 'files':saved_file_names}  
    