from utils import DBLayerAccess, Piece, Doc, Config, PieceMapper, DocMapper
# This is sample testing, no real and serious unit tests to be implemented
# Used to assert that code evolutions should not make the existing one crash

if __name__ == '__main__':
    print("Beginning Tests")
    c = Config()
    db_layer = DBLayerAccess(c)
    db_layer.connect()
    piece_mapper = PieceMapper(db_layer)
    doc_mapper = DocMapper(db_layer)

    print("1 - Creating a Piece and a Doc")
    piece   = Piece({"content": "Created piece"})
    doc = Piece({"content": "new documentation with new pattern"})

    print("2 - Saving a Piece and a Doc")
    inserted_piece = piece_mapper.insert(piece)
    inserted_doc = doc_mapper.insert(doc)
    
    print("3 - Fetching a Piece and a Doc")
    fetch_piece = piece_mapper.find(1)
    fetch_doc = doc_mapper.find(1)

    print("4 - Updating a Piece and a Doc Objects")
    piece_updated = Piece({
        "id": fetch_piece.id, 
        "content": "update this piece",
        "create_date": fetch_piece.create_date,
        "modify_date": fetch_piece.modify_date
    })
    doc_updated = Doc({
        "id": fetch_doc.id,
        "content": "update this document",
        "create_date": fetch_doc.create_date,
        "modify_date": fetch_doc.modify_date
    })
    
    print("5 - Updating a Piece and Doc records")
    piece_updated_saved = piece_mapper.update(piece_updated)
    doc_updated_saved = piece_mapper.update(doc_updated)

    db_layer.close()