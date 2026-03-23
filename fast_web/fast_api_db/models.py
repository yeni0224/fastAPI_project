from sqlalchemy import Column, Integer, String, Text
from fast_api_db.database import Base

#테이블과 연결할 객체, obj 객체로 만들면 note의 instance는 한 줄을 저장하는 공간이 될 것
#schema 공간을 생각하며 작성
#해당 이름의 테이블이 없으면 테이블을 만들어주는 작업을 할 수 있다. Base.metadata.create_all(bind=engine)
class Note(Base): #모델이기 때문에 항상 base를 상속받아야함. 
    __tablename__ = "notes"

    #primary_key=True라서 autoincrement가 자동 적용
    id = Column(Integer, primary_key=True, index = True) 
    title = Column(String(255), nullable=False) # varchar
    content = Column(Text, nullable=False)

    #파일 경로 또는 파일명을 저장할 컬럼 추가
    file_path = Column(String(255), nullable=True)