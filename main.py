from fastapi import FastAPI, status, HTTPException
from pydantic import BaseModel
from typing import Optional, List
from database import SessionLocal
import models

app=FastAPI()


class Item(BaseModel): #serializer
    id:int
    name:str
    description:str
    price:int
    on_offer:bool
    
    class Config:
        orm_mode=True


db=SessionLocal()


@app.get('/items', response_model=List[Item], status_code=status.HTTP_200_OK)
def get_all_items():
    return db.query(models.Item).all()


@app.get('/item/{item_id}', response_model=Item, status_code=status.HTTP_200_OK)
def get_an_item(item_id:int):
    return db.query(models.Item).filter(models.Item.id==item_id).first()


@app.post('/items', response_model=Item, status_code=status.HTTP_201_CREATED)
def create_an_item(item:Item):
    db_item=db.query(models.Item).filter(models.Item.name==item.name).first()
    if db_item is not None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Item already exists!")
    
    new_item=models.Item(
        name=item.name,
        price=item.price,
        description=item.description,
        on_offer=item.on_offer
    )
    
    db.add(new_item)
    db.commit()
    return new_item


@app.put('/item/{item_id}', response_model=Item, status_code=status.HTTP_200_OK)
def update_an_item(item_id:int, item:Item):
    item_new=db.query(models.Item).filter(models.Item.id==item_id).first()
    item_new.name = item.name
    item_new.price = item.price
    item_new.description = item.description
    item_new.on_offer = item.on_offer
    
    db.commit()
    return item_new


@app.delete('/item/{item_id}')
def delete_an_item(item_id:int):
    item_delete=db.query(models.Item).filter(models.Item.id==item_id).first()
    
    if item_delete is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Resource Not Found")
    
    db.delete(item_delete)
    db.commit()
    return item_delete

