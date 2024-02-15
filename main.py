from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles

from app.dbfactory import db_startup

from app.routes.admin import admin_router
from app.routes.main import  main_router
from app.routes.board import board_router
from app.routes.member import member_router

# 서버 시작 시 DB 생성
@asynccontextmanager
async def lifespan(app: FastAPI):
    yield
    db_startup()

app = FastAPI(lifespan=lifespan)

app.include_router(member_router)
app.include_router(admin_router, prefix='/admin')
app.include_router(board_router)
app.include_router(main_router)




# jinja2 설정
templates = Jinja2Templates(directory='views/templates')
app.mount('/static', StaticFiles(directory='views/static'), name='static')



@app.get("/", response_class=HTMLResponse)
async def index(req: Request):
    return templates.TemplateResponse('index.html', {'request': req})


# 파이썬 코드로
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", reload=True)