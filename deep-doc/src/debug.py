from domain_types import Piece, Document

from config import Config
from db import DBLayerAccess

from utils import PieceMapper

if __name__ == "__main__":

    piece = Piece()
    document = Document()

    c = Config()
    db_layer = DBLayerAccess(c)
    db_layer.connect()
    piece_mapper = PieceMapper(db_layer)
    piece = Piece(**{"title": "Title", "content": "Content"})
    inserted_piece = piece_mapper.insert(piece)

    print(piece)
    print(inserted_piece)