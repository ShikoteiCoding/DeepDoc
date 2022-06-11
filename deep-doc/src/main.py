import psycopg2
from utils import Config, DBLayerAccess, DocParser, PieceMapper, DocMapper

from domain_types.piece import Piece
from domain_types.document import Document

if __name__ == '__main__':
    
    c = Config()
    db_layer = DBLayerAccess(c)
    db_layer.connect()
    piece_mapper = PieceMapper(db_layer)
    doc_mapper = DocMapper(db_layer)
    

    db_layer.close()