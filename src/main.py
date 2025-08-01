import uvicorn
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from api.v1 import endpoints as routes
from utils.errors import DomainError, domain_error_exception_handler

app = FastAPI(
    title="DirectotyOfAreaManagmet",
    openapi_url="/directory_of_area/openapi.json",
    docs_url="/directory_of_area/docs",
    exception_handlers={DomainError: domain_error_exception_handler},
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(routes.room_type.router)
app.include_router(routes.auth.router)
app.include_router(routes.user.router)
app.include_router(routes.room.router)

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        reload=True,
        proxy_headers=True,
    )
