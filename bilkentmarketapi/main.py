from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import database
from routers import user, auth, item

app = FastAPI()
database.Base.metadata.create_all(bind=database.engine)

origins = [
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return {"message": "Hello App"}


app.include_router(user.router)
app.include_router(item.router)
app.include_router(auth.router)