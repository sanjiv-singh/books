import databases
from fastapi import FastAPI, Request
import sqlalchemy

DATABASE_URL = "sqlite:///udemy.sqlite"

database = databases.Database(DATABASE_URL)
metadata = sqlalchemy.MetaData()

books = sqlalchemy.Table(
    "books",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("title", sqlalchemy.String),
    sqlalchemy.Column("author", sqlalchemy.String),
)

engine = sqlalchemy.create_engine(DATABASE_URL)

app = FastAPI()

@app.on_event("startup")
async def startup():
    await database.connect()
    metadata.create_all(engine)


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()

@app.get("/books/")
async def get_all_books():
    query = books.select()
    return await database.fetch_all(query)

@app.post("/books/")
async def create_book(request: Request):
    data = await request.json()
    query = books.insert().values(*data)
    last_record_id = await database.execute(query)
    return {"id": last_record_id}