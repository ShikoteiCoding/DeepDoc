from models import (PieceMapper, Document)

import json

SCHEMA_PATH = "../schema/"

def read_schema(path: str) -> dict:

    with open(path) as f:
        return json.load(f)

##
#   Parser Functions
##

import re
class DocumentParser:
    """ Static class to hold parsing functions. """

    @staticmethod
    def read(doc: Document, piece_mapper: PieceMapper) -> str:
        if not isinstance(doc, Document) or not isinstance(piece_mapper, PieceMapper): 
            raise TypeError("Expect a doc object and a piece mapper object.")

        piece_refs = DocumentParser.extract_piece_ids(doc)

        # Regex match ids. Extract is type-safe. Cast the id to integer.
        doc_associated_pieces = [piece_mapper.find(int(piece_id)) for piece_id in piece_refs]
        pieces_dict = {str(piece.id): str(piece.content) for piece in doc_associated_pieces}
        return DocumentParser.replace_piece_ids(doc, pieces_dict)

    @staticmethod
    def extract_piece_ids(doc: Document) -> list[str]:
        # Might not need to be called "on read" but "on save"
        # Because we can use a different relation table to track saved pieces associated to doc
        # Upsert to avoid adding already existing relations ?
        content = doc.content
        pattern = re.compile('@(.*?)@')
        matches = pattern.findall(content)
        return matches

    @staticmethod
    def replace_piece_ids(doc: Document, pieces_dict: dict[str, str]) -> str:
        content = doc.content
        for key, value in pieces_dict.items():
            content = content.replace(f"@{str(key)}@", value)
        return content