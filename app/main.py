from dotenv import load_dotenv
from fastapi import FastAPI

from .database import db_connection, models
from .route import router

load_dotenv()

models.Base.metadata.create_all(bind=db_connection.engine)

app = FastAPI(
    debug=True,
)

app.include_router(router)
