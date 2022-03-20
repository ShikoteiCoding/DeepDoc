from utils import DBLayerAccess, Piece, Doc, Config, PieceMapper, DocMapper, DocParser
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

    print("6 - Creating a nested doc")
    print("6.1 - Creating a piece which will be used in the doc")
    referenced_piece = Piece({"content": "2022"})
    saved_referenced_piece = piece_mapper.insert(referenced_piece)
    
    print("6.2 - Creating the doc and referencing the previously saved piece")
    nested_doc = Doc({"content": f"DeepDoc was created in \@{saved_referenced_piece.id}@ and is for now open source (lol)"})

    print("6.3 - Reading the document with inline references")
    print(DocParser.read(nested_doc, piece_mapper))

    db_layer.close()