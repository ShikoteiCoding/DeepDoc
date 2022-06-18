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


db_layer = DBLayerAccess(Config())
db_layer.connect()
document_mapper = DocumentMapper(db_layer)
piece_mapper = PieceMapper(db_layer)


@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/pieces/{piece_id}")
async def get_piece(piece_id: int):
    """ Get a piece by specifiying ID. """
    piece = piece_mapper.find(piece_id)
    return {"piece_id": piece.__dict__}

@app.get("/documents/{document_id}")
async def get_document(document_id: int):
    document = document_mapper.find(document_id)
    return {"document_id": document.__dict__}