import psycopg2
from utils import Config, DBLayerAccess, Piece, Doc, DocParser, PieceMapper, DocMapper

if __name__ == '__main__':
    
    c = Config()
    db_layer = DBLayerAccess(c)
    db_layer.connect()
    piece_mapper = PieceMapper(db_layer)
    doc_mapper = DocMapper(db_layer)
    
    #piece_mapper.insert(Piece({"title": "Deep Doc Creation Date", "content": "2022"}))
    doc_mapper.insert(Doc({"title": "Presentation Doc", "content": "Deep doc was created in \@1@"}))

    db_layer.close()