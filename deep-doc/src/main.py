import psycopg2
from utils import Config, DBLayerAccess, Piece, Doc, DocParser, PieceMapper, DocMapper

if __name__ == '__main__':
    
    c = Config()
    db_layer = DBLayerAccess(c)
    db_layer.connect()
    piece_mapper = PieceMapper(db_layer)
    doc_mapper = DocMapper(db_layer)
    
    doc = Doc({"content": "First deep doc with this amazing piece: \@1@"})
    inserted_doc = doc_mapper.insert(doc)

    piece = Piece({"content": "I am an amazing piece"})
    inserted_piece = piece_mapper.insert(piece)

    print(DocParser.read(doc))

    db_layer.close()