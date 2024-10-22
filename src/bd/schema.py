from pydantic import BaseModel


class Product(BaseModel):
    name: str
    price: int
    category: str

class Filtering(BaseModel):
    initial_price: int
    final_price: int

class Name(BaseModel):
    name: str

class Category(BaseModel):
    category: str
