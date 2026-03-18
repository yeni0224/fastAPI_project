from fastapi import FastAPI

app = FastAPI()

@app.get("/") #get방식으로 요청 route 대신 저렇게 작성한다.
def index():
    return{'message':'hello, FAST API!'}

#라우팅
@app.get("/item")
def get_items():
    return ['apple','banana']

#동적url
@app.get("/item/{item_id}")
def get_item(item_id:int):
    return {'item_id':item_id}