CREATE OR REPLACE FUNCTION trigger_set_timestamp()
RETURNS TRIGGER AS $$
BEGIN
  NEW.modify_date = NOW();
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE SEQUENCE piece_id_pk_seq
    START 1
    INCREMENT 1
    NO MAXVALUE
    CACHE 1;

CREATE TABLE IF NOT EXISTS pieces (
    id INT NOT NULL DEFAULT nextval('piece_id_pk_seq'),
    title TEXT NOT NULL,
    content TEXT NOT NULL,
    create_date TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    modify_date TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    PRIMARY KEY (id)
);

CREATE TRIGGER set_timestamp
BEFORE UPDATE ON pieces
FOR EACH ROW
EXECUTE PROCEDURE trigger_set_timestamp();

CREATE SEQUENCE piece_version_id_pk_seq
    START 1
    INCREMENT 1
    NO MAXVALUE
    CACHE 1;

CREATE TABLE IF NOT EXISTS pieces_version (
    id INT NOT NULL DEFAULT nextval('piece_version_id_pk_seq'),
    piece_id INT NOT NULL,
    title TEXT NOT NULL,
    content TEXT NOT NULL,
    create_date TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    modify_date TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    PRIMARY KEY (id)
);

CREATE SEQUENCE doc_id_pk_seq
    START 1
    INCREMENT 1
    NO MAXVALUE
    CACHE 1;

CREATE TABLE IF NOT EXISTS documents (
    id INT NOT NULL DEFAULT nextval('doc_id_pk_seq'),
    title TEXT NOT NULL,
    content TEXT NOT NULL,
    create_date TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    modify_date TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    PRIMARY KEY (id),
    CONSTRAINT fk_pieces
        FOREIGN KEY (piece_id) 
            REFERENCES pieces(id)
);

CREATE TRIGGER set_timestamp
BEFORE UPDATE ON documents
FOR EACH ROW
EXECUTE PROCEDURE trigger_set_timestamp();

CREATE SEQUENCE doc_version_id_seq
    START 1
    INCREMENT 1
    NO MAXVALUE
    CACHE 1;

CREATE TABLE IF NOT EXISTS documents_version (
    id INT NOT NULL DEFAULT nextval('doc_version_id_seq'),
    document_id INT NOT NULL,
    title TEXT NOT NULL,
    content TEXT NOT NULL,
    create_date TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    modify_date TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    PRIMARY KEY (id),
    CONSTRAINT fk_docs
        FOREIGN KEY (document_id) 
            REFERENCES documents(id)
);

--CREATE TABLE IF NOT EXISTS docs_pieces_rel (
--    pieces_id INT NOT NULL,
--    docs_id INT NOT NULL,
--    CONSTRAINT fk_pieces
--        FOREIGN KEY (pieces_id) 
--            REFERENCES pieces(id),
--    CONSTRAINT fk_docs
--        FOREIGN KEY (docs_id) 
--            REFERENCES documents(id)
--);

