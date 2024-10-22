import logging
import sys

from fastapi import FastAPI
from fastapi import Form
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi_sqlalchemy import DBSessionMiddleware, db

from starlette.responses import JSONResponse

from .config import DB_USER, DB_PASS, DB_HOST, DB_PORT, DB_NAME
from .bd.models import Product as ModelProduct
from .bd.schema import Product as SchemaProduct
from .bd.schema import Filtering as SchemaFiltering
from .bd.schema import Name as SchemaName
from .bd.schema import Category as SchemaCategory

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
stream_handler = logging.StreamHandler(sys.stdout)
log_formatter = logging.Formatter(
    "%(asctime)s [%(processName)s: %(process)d] [%(threadName)s: %(thread)d] [%(levelname)s] %(name)s: %(message)s")
stream_handler.setFormatter(log_formatter)
logger.addHandler(stream_handler)

logger.info('API is starting up')

app = FastAPI()

DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
app.add_middleware(DBSessionMiddleware, db_url=DATABASE_URL)

@app.get("/docs")
def read_docs():
    return get_swagger_ui_html(openapi_url="/openapi.json")

@app.post("/product")
async def add_product(name: str = Form(...), price: int = Form(...), category: str = Form(...)):
    try:
        sh = SchemaProduct(name=name, price=price, category=category)

        db_book = ModelProduct(name=sh.name, price=sh.price, category=sh.category)
        db.session.add(db_book)
        db.session.commit()
        return {"message": "Product saved successfully"}
    except:
        return JSONResponse(status_code=400, content={"message": "Product saved error"})

@app.get("/product")
async def list_product():
    try:
        bd_data = db.session.query(ModelProduct).all()
        data = {}
        for item in bd_data:
            data[item.id] = ["name: " + item.name,"price: " + str(item.price),"category: " +  item.category]

        return JSONResponse(data)
    except:
       return JSONResponse(status_code=400, content={"message": "Incorrect Data"})

@app.get("/product/{name}")
async def show_product(name: str):
    try:
        sh = SchemaName(name=name)
        print(sh.name)
        bd_data = db.session.query(ModelProduct).filter(ModelProduct.name == sh.name).first()

        return {"name: " + bd_data.name,"price: " + str(bd_data.price),"category: " + bd_data.category}
    except AttributeError:
        return JSONResponse(status_code=400, content={"message": "Incorrect Data. This name is not in the database"})
    except:
        return JSONResponse(status_code=400, content={"message": "Incorrect Data. Error name"})

@app.get("/product/category/{category}")
async def category_product(category: str):
    try:
        sh = SchemaCategory(category=category)
        bd_data = db.session.query(ModelProduct).filter(ModelProduct.category == sh.category).all()
        data = {}
        for item in bd_data:
            data[item.id] = ["name: " + item.name,"price: " + str(item.price),"category: " +  item.category]

        return JSONResponse(data)
    except AttributeError:
        return JSONResponse(status_code=400, content={"message": "Incorrect Data. This category is not in the database"})
    except:
        return JSONResponse(status_code=400, content={"message": "Incorrect Data. Error category"})

@app.get("/product/filtering/{initial_price}&{final_price}")
async def filtering_product(initial_price: int, final_price: int):
    try:
        sh = SchemaFiltering(initial_price=initial_price, final_price=final_price)
        bd_data = db.session.query(ModelProduct).filter(ModelProduct.price >= sh.initial_price).filter(
            ModelProduct.price <= sh.final_price).all()
        data = {}
        for item in bd_data:
            data[item.id] = [item.name, item.price, item.category]

        return JSONResponse(data)
    except:
        return JSONResponse(status_code=400, content={"message": "Incorrect Data."})

@app.delete("/product/{name}")
async def delete_product(name: str):
    try:
        sh = SchemaName(name=name)

        db.session.query(ModelProduct).filter(ModelProduct.name == sh.name).delete(synchronize_session=False)
        db.session.commit()
        return {"message": "Product delete successfully"}
    except:
        return JSONResponse(status_code=400, content={"message": "Incorrect Data. Error name"})

@app.put("/product/{name}")
async def update_product(name: str, price: int, category: str):
    try:
        sh = SchemaProduct(name=name, price=price, category=category)
        bd_data = db.session.query(ModelProduct).filter(ModelProduct.name == sh.name).first()

        bd_data.name = sh.name
        bd_data.price = sh.price
        bd_data.category = sh.category
        db.session.add(bd_data)
        db.session.commit()
        return {"message": "Product update successfully"}
    except:
        return JSONResponse(status_code=400, content={"message": "Incorrect Data. Error name"})


