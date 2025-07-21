
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


# NOTE: dev lifecycle not for production
init_db(Base)


app = FastAPI(
    docs_url=conf.openapi_docs, 
    redoc_url=conf.openapi_redoc,
)

app.include_router(router, prefix="/api")

@app.get("/")
def root():
    """Demo application root page"""
    return {
        "message": "dev demo root",
        "api_url": "/api",
        "docs_url": conf.openapi_docs, 
        "redoc_url": conf.openapi_redoc, 
        }

logger.info("start app")
