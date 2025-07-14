
import logging
from fastapi import Depends, FastAPI

from app.config import conf
from app.database import init_db
from app.models import Base
from app.api import router


logging.basicConfig(
    level=logging.DEBUG,  # NOTE: not for production
    format='%(asctime)s %(name)s %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
)

logger = logging.getLogger(__name__)


# NOTE: fix lifecycle
init_db(Base)


app = FastAPI(
    docs_url=conf.openapi_docs, 
    redoc_url=conf.openapi_redoc,
    # NOTE: dependencies=[Depends(...)]
)

app.include_router(router, prefix="/api")

@app.get("/")
def root():
    return {
        "message": "dev demo root",
        "docs_url": conf.openapi_docs, 
        "redoc_url": conf.openapi_redoc, 
        }

logger.info("start app")
