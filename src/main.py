import sys
from pathlib import Path


# This path was added to solve some problems with absolute
# imports in order to run this script as an executable file.
sys.path.append(str(Path(__file__).parent.parent))


from fastapi import FastAPI
import uvicorn

from src.core.settings import settings
from src.migrations.main import main as run_migrations
from src.api.routes import router


def get_app() -> 'FastAPI':
    app = FastAPI(
        title=settings.project_name,
        root_path=settings.root_path,
        version=settings.app_version,
        debug=settings.debug,
    )

    app.include_router(router, prefix=settings.api_prefix)
    return app 


app = get_app()


def main():
    run_migrations(settings.sqlalchemy.url)
    uvicorn.run(**settings.uvicorn.dict())


if __name__ == '__main__':
    main()