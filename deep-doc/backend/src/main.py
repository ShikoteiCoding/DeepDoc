from db import DBLayerAccess
from models import (Piece, PieceMapper, Document, DocumentMapper)

from config import Config
from fastapi import FastAPI

#if __name__ == '__main__':
    
    #c = Config()
    #db_layer = DBLayerAccess(c)
    #db_layer.connect()
    #db_layer.close()

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/pieces/{piece_id}")
async def get_piece(piece_id: int):
    return {"piece_id": piece_id}

@app.get("/documents/{document_id}")
async def get_document(document_id: int):
    db_layer = DBLayerAccess(Config())
    db_layer.connect()
    document_mapper = DocumentMapper(db_layer)
    document = document_mapper.find(document_id)
    db_layer.close()
    
    return {"document_id": document}