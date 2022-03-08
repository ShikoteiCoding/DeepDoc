CREATE SEQUENCE piece_id_pk_seq
    START 1
    INCREMENT 1
    NO MAXVALUE
    CACHE 1;

CREATE TABLE IF NOT EXISTS pieces (
    id INT NOT NULL DEFAULT nextval('piece_id_pk_seq'),
    content TEXT NOT NULL,
    create_date TIMESTAMP WITH TIME ZONE NOT NULL,
    modify_date TIMESTAMP WITH TIME ZONE NOT NULL,
    PRIMARY KEY (id)
);

CREATE SEQUENCE doc_id_pk_seq
    START 1
    INCREMENT 1
    NO MAXVALUE
    CACHE 1;

CREATE TABLE IF NOT EXISTS docs (
    id INT NOT NULL DEFAULT nextval('doc_id_pk_seq'),
    content text NOT NULL,
    create_date TIMESTAMP WITH TIME ZONE NOT NULL,
    modify_date TIMESTAMP WITH TIME ZONE NOT NULL,
    PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS docs_pieces_rel (
    pieces_id INT NOT NULL,
    docs_id INT NOT NULL,
    CONSTRAINT fk_pieces
        FOREIGN KEY (pieces_id) 
            REFERENCES pieces(id),
    CONSTRAINT fk_docs
        FOREIGN KEY (docs_id) 
            REFERENCES docs(id)
);

