from fastapi import FastAPI
import models.tasks
from routers.tasks import router as tasks_router
from session import engine


tags_info = [
    {"name": "Auth", "description": "Routes related with authentication."},
    {"name": "Tasks", "description": "Routes related with tasks."},
    {"name": "Admin", "description": "Routes available only for admins"},
]


app = FastAPI(openapi_tags=tags_info)

app.include_router(tasks_router)


models.tasks.Base.metadata.create_all(bind=engine)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="localhost", port=8000)
