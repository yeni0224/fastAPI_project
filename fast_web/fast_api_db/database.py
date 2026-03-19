from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

#MySQL 연결 정보
DATABASE_URL = "mysql+pymysql://madang:madang@localhost:3306/madangdb?charset=utf8mb4"
engine = create_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()