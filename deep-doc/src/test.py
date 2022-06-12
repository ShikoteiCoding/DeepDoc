from db import  DBLayerAccess
from config import Config
from utils import (
    DocumentParser, 
    PieceMapper, DocumentMapper
)
# This is sample testing, no real and serious unit tests to be implemented
# Used to assert that code evolutions should not make the existing one crash
# Can also be use to DB changes by adding the changes in the Mappers

from domain_types import Piece, Document

import unittest

class PieceTest(unittest.TestCase):

    def test_correct_piece_instance(self):
        piece = Piece(**{"title": "Title", "content": "Content"})
        self.assertIsInstance(piece, Piece)
        self.assertIsNone(piece.id)
        self.assertTrue(piece.title, "Title")
        self.assertTrue(piece.content, "Content")
        self.assertIsNone(piece.create_date)
        self.assertIsNone(piece.modify_date)

    def test_wrong_piece_instance(self):
        self.assertRaises(TypeError, Piece, **{"titl": "Title", "conten": "Content"})

class DocTest(unittest.TestCase):

    def test_correct_doc_instance(self):
        doc = Document(**{"title": "Title", "content": "Content"})
        self.assertIsInstance(doc, Document)
        self.assertIsNone(doc.id)
        self.assertTrue(doc.title, "Title")
        self.assertTrue(doc.content, "Content")
        self.assertIsNone(doc.create_date)
        self.assertIsNone(doc.modify_date)

    def test_wrong_doc_instance(self):
        self.assertRaises(TypeError, Document, **{"titl": "Title", "conten": "Content"})

class DBMappingTest(unittest.TestCase):

    def test_insert_piece_db(self):
        """ Testing a Piece inserted for the first time (no prior existence in DB). """
        
        c = Config()
        db_layer = DBLayerAccess(c)
        db_layer.connect()
        piece_mapper = PieceMapper(db_layer)
        piece = Piece(**{"title": "Title", "content": "Content"})
        inserted_piece = piece_mapper.insert(piece)

        self.assertIsNotNone(inserted_piece)
        self.assertIsInstance(inserted_piece, Piece)

        self.assertIsNotNone(inserted_piece.id)
        self.assertTrue(inserted_piece.title, "Title")
        self.assertTrue(inserted_piece.content, "Content")
        self.assertIsNotNone(inserted_piece.create_date)
        self.assertIsNotNone(inserted_piece.modify_date)
        self.assertEqual(inserted_piece.create_date, inserted_piece.modify_date)
        
        self.assertEqual(piece.title, inserted_piece.title)
        self.assertEqual(piece.content, inserted_piece.content)

        db_layer.close()

    def test_insert_doc_db(self):
        """ Testing a Doc inserted for the first time (no prior existence in DB). """

        c = Config()
        db_layer = DBLayerAccess(c)
        db_layer.connect()
        doc_mapper = DocumentMapper(db_layer)
        doc = Document(**{"title": "Title", "content": "Content"})
        inserted_doc = doc_mapper.insert(doc)

        self.assertIsNotNone(inserted_doc)
        self.assertIsInstance(inserted_doc, Document)

        self.assertIsNotNone(inserted_doc.id)
        self.assertTrue(inserted_doc.title, "Title")
        self.assertTrue(inserted_doc.content, "Content")
        self.assertIsNotNone(inserted_doc.create_date)
        self.assertIsNotNone(inserted_doc.modify_date)
        self.assertEqual(inserted_doc.create_date, inserted_doc.modify_date)
        
        self.assertEqual(doc.title, inserted_doc.title)
        self.assertEqual(doc.content, inserted_doc.content)

        db_layer.close()

    def test_fetch_piece_db(self):
        
        c = Config()
        db_layer = DBLayerAccess(c)
        db_layer.connect()
        piece_mapper = PieceMapper(db_layer)
        piece = Piece(**{"title": "Title", "content": "Content"})
        inserted_piece = piece_mapper.insert(piece)

        found_piece = piece_mapper.find(inserted_piece.id)

        self.assertIsInstance(found_piece, Piece)
        self.assertEqual(inserted_piece, found_piece)

        db_layer.close()

    def test_fetch_doc_db(self):
        
        c = Config()
        db_layer = DBLayerAccess(c)
        db_layer.connect()
        doc_mapper = DocumentMapper(db_layer)
        doc = Document(**{"title": "Title", "content": "Content"})
        inserted_doc = doc_mapper.insert(doc)

        found_doc = doc_mapper.find(inserted_doc.id)

        self.assertIsInstance(found_doc, Document)
        self.assertEqual(inserted_doc, found_doc)

        db_layer.close()

    def test_update_piece_db(self):
        
        c = Config()
        db_layer = DBLayerAccess(c)
        db_layer.connect()
        piece_mapper = PieceMapper(db_layer)
        piece = Piece(**{"title": "Title", "content": "Content"})
        inserted_piece = piece_mapper.insert(piece)

        updated_piece = Piece(**{
            "id": inserted_piece.id,
            "title": "new title",
            "content": "update this piece",
            "create_date": inserted_piece.create_date,
            "modify_date": inserted_piece.modify_date
        })

        self.assertEqual(inserted_piece.id, updated_piece.id)
        self.assertNotEqual(inserted_piece.title, updated_piece.title)
        self.assertNotEqual(inserted_piece.content, updated_piece.content)
        self.assertEqual(inserted_piece.create_date, updated_piece.create_date)
        self.assertEqual(inserted_piece.modify_date, updated_piece.modify_date)

        saved_piece = piece_mapper.update(updated_piece)

        self.assertEqual(saved_piece.id, updated_piece.id)
        self.assertEqual(saved_piece.title, updated_piece.title)
        self.assertEqual(saved_piece.content, updated_piece.content)
        self.assertEqual(saved_piece.create_date, updated_piece.create_date)
        self.assertNotEqual(saved_piece.modify_date, updated_piece.modify_date)

        self.assertNotEqual(saved_piece, updated_piece)

        db_layer.close()

    def test_update_doc_db(self):
        
        c = Config()
        db_layer = DBLayerAccess(c)
        db_layer.connect()
        doc_mapper = DocumentMapper(db_layer)
        doc = Document(**{"title": "Title", "content": "Content"})
        inserted_doc = doc_mapper.insert(doc)

        updated_doc = Document(**{
            "id": inserted_doc.id,
            "title": "new title",
            "content": "update this piece",
            "create_date": inserted_doc.create_date,
            "modify_date": inserted_doc.modify_date
        })

        self.assertEqual(inserted_doc.id, updated_doc.id)
        self.assertNotEqual(inserted_doc.title, updated_doc.title)
        self.assertNotEqual(inserted_doc.content, updated_doc.content)
        self.assertEqual(inserted_doc.create_date, updated_doc.create_date)
        self.assertEqual(inserted_doc.modify_date, updated_doc.modify_date)

        saved_doc = doc_mapper.update(updated_doc)

        self.assertEqual(saved_doc.id, updated_doc.id)
        self.assertEqual(saved_doc.title, updated_doc.title)
        self.assertEqual(saved_doc.content, updated_doc.content)
        self.assertEqual(saved_doc.create_date, updated_doc.create_date)
        self.assertNotEqual(saved_doc.modify_date, updated_doc.modify_date)

        self.assertNotEqual(saved_doc, updated_doc)

        db_layer.close()


if __name__ == '__main__':
    #print("6 - Creating a nested doc")
    #print("6.1 - Creating a piece which will be used in the doc")
    #referenced_piece = Piece({"title": "Creation Date", "content": "2022"})
    #saved_referenced_piece = piece_mapper.insert(referenced_piece)
    #
    #print("6.2 - Creating the doc and referencing the previously saved piece")
    #nested_doc = Doc({"content": f"DeepDoc was created in \@{saved_referenced_piece.id}@ and is for now open source (lol)"})
    #
    #print("6.3 - Reading the document with inline references")
    #print(DocParser.read(nested_doc, piece_mapper))
#
    #print("7 - Getting all records")
    #print(piece_mapper.findall())
    #print(doc_mapper.findall())
    #
    #db_layer.close()

    unittest.main()