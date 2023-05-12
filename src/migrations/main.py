""" The function `main` applies the migrations for the
     specified database automatically when application
     starting.

"""


import os
import typing
from pathlib import Path

from alembic import command
from alembic.config import Config

if typing.TYPE_CHECKING:
    from sqlalchemy.engine.url import URL

PROJECT_PATH = Path(__file__).parent.parent.parent.resolve()


def main(db_url: typing.Optional[typing.Union[str, "URL"]] = None):
    if db_url:
        alembic_ini = os.path.join(PROJECT_PATH, "alembic.ini")

        alembic_cfg = Config(file_=alembic_ini, ini_section="alembic")
        alembic_cfg.set_main_option("sqlalchemy.url", str(db_url))
        alembic_location = alembic_cfg.get_main_option("script_location")
        if not os.path.isabs(alembic_location):
            alembic_cfg.set_main_option(
                "script_location",
                os.path.join(PROJECT_PATH, alembic_location),
            )

        command.upgrade(alembic_cfg, "head")
