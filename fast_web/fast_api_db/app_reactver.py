from fastapi import FastAPI, Depends, HTTPException, Request, Form, File, UploadFile
from fastapi.responses import RedirectResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from fast_api_db.database import SessionLocal, engine, Base
import fast_api_db.models as models
from fast_api_db.schema import NoteCreate, NoteUpdate, NoteOut
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import os
from uuid import uuid4

#테이블 생성
Base.metadata.create_all(bind=engine)

app = FastAPI()
#CORS 추가 : 포트번호가 달라도 접근을 허용하겠다
app.add_middleware(
    CORSMiddleware,
    #리엑트 서버 추가
    allow_origins=["http://localhost:5173","http://127.0.0.1:5173"],
    allow_credentials=True,   # 쿠키/인증정보 포함 허용
    allow_methods=["*"],      # 모든 HTTP 메서드(GET, POST, PUT, DELETE 등) 허용
    allow_headers=["*"],      # 모든 요청 헤더 허용
)

# 1. 업로드할 폴더 경로 설정
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_DIR = os.path.join(BASE_DIR, "uploads")

# 2. 폴더가 없으면 자동으로 생성하는 코드
if not os.path.exists(UPLOAD_DIR):
    os.makedirs(UPLOAD_DIR)
 
# /uploads URL로 요청이 오면, 서버의 "uploads" 폴더 안의 파일들을 보여줍니다.
app.mount("/uploads", StaticFiles(directory=UPLOAD_DIR), name="uploads")

# DB 세션 의존성 : 요청할 때마다 DB연결 열고->사용->연결종료
def get_db():
    db = SessionLocal() # 세션 생성
    try:
        yield db # db 사용이 끝날때까지 대기, 요청 끝나고 돌아오면
    finally:
        db.close() # 세션 종료

# 전체 조회
#response_model : 리턴 데이터의 타입을 검증 + 변환 + 필터링(타입 틀리면, 누락된 필드 있으면 에러)
#NoteOut 구조와 맞는지 확인
#ORM 객체를 JSON으로 자동 변환
#필터링 (NoteOut에 없는 데이터는 반환X)- a컬럼이 있어서 가져왔어도 NoteOut에 없으면 필터로 걸러냄
@app.get("/notes", response_model=list[NoteOut])
def get_notes(db:Session=Depends(get_db)):
    return db.query(models.Note).all()

# 상세 조회
@app.get("/notes/{note_id}", response_model=NoteOut)
def get_note(note_id:int, db:Session=Depends(get_db)):
    note = db.query(models.Note).get(note_id)
    if not note:
        raise HTTPException(404, "Not Found")
    return note

# 생성
# @app.post("/notes", response_model=NoteOut)
# def create_note(note: NoteCreate, db: Session = Depends(get_db)):
#     #JSON 에서 note: NoteCreate(Pydantic모델)을 Python dict로 변경
#     #**:언패킹 딕셔너리 키-값을 키워드 인자로 풀어서 전달
#     db_note = models.Note(**note.model_dump()) 
#     db.add(db_note)
#     db.commit()
#     db.refresh(db_note) #DB에 반영된 최신 상태를 다시 객체에 가져오는 함수
#                         #refresh하여 INSERT 후 자동 생성 값 가져올 때 사용
#     return db_note

@app.post("/notes", response_model=NoteOut)
async def create_note(    # 1. 텍스트 데이터는 Form(...)
    title: str = Form(...),
    content: str = Form(...),
    # 2. 파일(기본값 None) 텍스트와 별개로 받아온다
    file: UploadFile | None = File(None),
    db: Session = Depends(get_db)
):
    # 3. 받은 폼 데이터 NoteCreate에 넣어 검증    
    note_data = NoteCreate(title=title, content=content)
 
    # 4. 파일 처리 로직 (파일이 들어왔을 때만 실행)
    file_path = None
    if file is not None:
        # 실제 환경에서는 uuid 등을 써서 파일명 중복을 방지하는 것이 좋음
        folder = os.path.join(BASE_DIR,'uploads')
        #업로드 될 파일 명(중복 방지)
        name, ext = os.path.splitext(file.filename)#   .png
        filename = name +str(uuid4()) + ext
        #파일 내용
        content = await file.read()
        f = open(folder+'/'+filename, 'wb')  # 바이너리 파일 출력
        f.write(content)
        f.close()
 
        file_path = f"uploads/{filename}"
 
    # 5. DB에 저장할 SQLAlchemy 모델 객체 생성
    db_note = models.Note(
        title=note_data.title,
        content=note_data.content,
        file_path=file_path # 파일이 없으면 None이 들어감
    )
   
    # 6. DB 커밋
    db.add(db_note)
    db.commit()
    db.refresh(db_note)
 
    return db_note

# 수정
@app.post("/notes/{note_id}",response_model=NoteOut)
def update_note(note_id: int, data:NoteUpdate, db: Session = Depends(get_db)):
    note = db.query(models.Note).get(note_id) #ORM 객체 → JSON 직렬화
    if not note:
        raise HTTPException(404)

    note.title = data.title
    note.content = data.content
    db.commit()
    return note

# 삭제
@app.post("/notes/{note_id}")
def delete_note(note_id: int, db: Session = Depends(get_db)):
    note = db.query(models.Note).get(note_id)
    if not note:
        raise HTTPException(404)

    db.delete(note)
    db.commit()
    return {"message" : "deleted"}