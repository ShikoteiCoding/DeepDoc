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

    piece_refs = DocParser.extract_piece_references(inserted_doc)

    doc_associated_pieces = [PieceMapper(db_layer).find(piece_id) for piece_id in piece_refs]

    pieces = {str(piece.id): str(piece.content) for piece in doc_associated_pieces}

    print(pieces)

    doc_view = DocParser.replace_piece_references(doc, piece_refs, pieces)
    
    print(doc_view)

    db_layer.close()