from pydantic import BaseModel

#Json API면 BaseModel 필수
#Form 기반이면 BaseModel이 필요없음(이번 예제에서 사용x)
#FastAPI가 요청/응답 처리할 때 자동으로 사용

#공통 필드 정의 (재사용) - 검사 대상

class NoteBase(BaseModel):
    title : str
    content : str

class NoteCreate(NoteBase):
    pass

class NoteUpdate(NoteBase):
    pass

class  NoteOut(NoteBase):
    id : int
    class Config:
        orm_mode = True