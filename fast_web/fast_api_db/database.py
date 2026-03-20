#특정 db에 접속할 수 있는 드라이버 pymysql도 함께 설치해야함
#모델과 테이블간의 관계를 맺어줌, 관계 기반으로 sql문을 자동으로 작성해주는 기능
from sqlalchemy import create_engine 
from sqlalchemy.orm import sessionmaker, declarative_base 

#MySQL 연결 정보
#다른 PC에서 사용할거라면 localhost자리에 해당 컴퓨터의 ip를 작성할 것
DATABASE_URL = "mysql+pymysql://madang:madang@localhost:3306/madangdb?charset=utf8mb4" 
engine = create_engine(DATABASE_URL, echo=True)

#autocommit이 true일 경우 transaction이 항상 돌고있고, 명령 후 commit을 따로 할 필요가 없음.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base() #테이블과 맵핑할 모델을 만들 때 상속받아야한다.