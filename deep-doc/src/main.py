import psycopg2
from utils import Config, DBLayerAccess, Piece, Doc, DocParser, PieceMapper, DocMapper

if __name__ == '__main__':
    
    c = Config()
    db_layer = DBLayerAccess(c)
    db_layer.connect()
    piece_mapper = PieceMapper(db_layer)
    doc_mapper = DocMapper(db_layer)
    
    doc = Doc({"content": "First deep doc with this amazing piece: \@12@. But I can also have other pieces: \@2@."})

    print(DocParser.read(doc, piece_mapper))
    #print(DocParser.extract_piece_references(doc))

    db_layer.close()