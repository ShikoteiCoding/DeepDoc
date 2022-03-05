CREATE TABLE IF NOT EXISTS piece (
    id INT NOT NULL,
    content TEXT NOT NULL,
    create_date TIMESTAMP WITH TIME ZONE NOT NULL,
    modify_date TIMESTAMP WITH TIME ZONE NOT NULL,
    PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS doc (
    id INT NOT NULL,
    content text NOT NULL,
    create_date TIMESTAMP WITH TIME ZONE NOT NULL,
    modify_date TIMESTAMP WITH TIME ZONE NOT NULL,
    PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS doc_piece_rel (
    piece_id INT NOT NULL,
    doc_id INT NOT NULL,
    CONSTRAINT fk_piece
        FOREIGN KEY (piece_id) 
            REFERENCES piece(id),
    CONSTRAINT fk_doc
        FOREIGN KEY (doc_id) 
            REFERENCES doc(id)
);