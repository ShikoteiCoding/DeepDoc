from dataclasses import dataclass

##
## Project config
##
@dataclass(frozen=True, slots=True)
class Config:
    """ Dataclass to hold the DB configurations. Not mutable. """

    db_host: str = "localhost"
    db_port: str = "5432"
    db_name: str = "postgres"
    db_user: str = "admin"
    db_pwd:  str = "admin"