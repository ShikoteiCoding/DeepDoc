from dataclasses import InitVar, dataclass, field
import os
from typing import Optional

class MissingEnvironmentVar(Exception):
    pass

#
def get_required(var: str) -> str:
    try:
        return str(os.getenv(var))
    except KeyError as error:
        raise MissingEnvironmentVar(f"{var} is missing from environment variables. {error}")

##
## Project config
##
@dataclass(kw_only=True, slots=True)
class Config:
    """ Dataclass to hold the DB configurations. Not mutable. """

    db_host: Optional[str] = field(init=True, default=None)
    db_port: Optional[str] = field(init=True, default=None)
    db_name: Optional[str] = field(init=True, default=None)
    db_user: Optional[str] = field(init=True, default=None)
    db_pwd:  Optional[str] = field(init=True, default=None)

def load_config() -> Config:
    db_host = get_required("DB_HOST")
    db_port = get_required("DB_PORT")
    db_name = get_required("DB_NAME")
    db_user = get_required("DB_USER")
    db_pwd  = get_required("DB_PWD")

    return Config(
            db_host=db_host, 
            db_port=db_port, 
            db_name=db_name, 
            db_user=db_user,
            db_pwd=db_pwd
        )