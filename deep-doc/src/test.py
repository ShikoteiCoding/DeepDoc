from utils import DBLayerAccess, Piece, Doc, Config
# This is sample testing, no real and serious unit tests to be implemented
# Used to assert that code evolutions should not make the existing one crash

if __name__ == '__main__':
    print("Beginning Tests")
    c = Config()
    db_layer = DBLayerAccess(c)
    db_layer.connect()

    print("1 - Creating a Piece and a Doc")
    piece   = Piece({"content": "Created piece"})
    doc     = Doc({"content": "Created doc"})

    print("2 - Saving a Piece and a Doc")
    db_layer.save_piece(piece)
    db_layer.save_doc(doc)
    
    print("3 - Fetching a Piece and a Doc")
    fetchPiece  = db_layer.get_piece(1)
    fetchDoc    = db_layer.get_doc(1)

    print("4 - Updating a Piece and a Doc")
    fetchPiece.update({"content": "I modified this piece"})
    fetchDoc.update({"content": "I modified this doc"})

    print("5 - Saving the Piece and Doc")
    db_layer.save_piece(fetchPiece)
    db_layer.save_doc(fetchDoc)

    db_layer.close()