from dataclasses import InitVar, dataclass, field
import os
from typing import Optional

class MissingEnvironmentVar(Exception):
    pass

#
def get_required(var: str, default: str) -> str:
    env_var = os.getenv(var, default)
    if env_var is None:
        raise MissingEnvironmentVar(f"{var} is missing from environment variables.")
    return str(env_var)
        

##
## Project config
##
@dataclass(kw_only=True)
class Config:
    """ Dataclass to hold the DB configurations. Not mutable. """

    db_host: Optional[str] = field(init=True, default=None)
    db_port: Optional[str] = field(init=True, default=None)
    db_name: Optional[str] = field(init=True, default=None)
    db_user: Optional[str] = field(init=True, default=None)
    db_pwd:  Optional[str] = field(init=True, default=None)

def load_config() -> Config:
    db_host = get_required("DB_HOST", "db")
    db_port = get_required("DB_PORT", "5432")
    db_name = get_required("DB_NAME", "postgres")
    db_user = get_required("DB_USER", "admin")
    db_pwd  = get_required("DB_PWD", "admin")

    return Config(
            db_host=db_host, 
            db_port=db_port, 
            db_name=db_name, 
            db_user=db_user,
            db_pwd=db_pwd
        )