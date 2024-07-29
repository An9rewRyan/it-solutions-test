from fastapi import FastAPI
from routers.auth import auth_router
from routers.crud import crud_router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="ADS_API",
              description="Crud interface for https://www.farpost.ru",
              version="1.0",
              docs_url='/api/docs',
              redoc_url='/api/redoc',
              openapi_url='/api/openapi.json')


app.include_router(
    auth_router,
)
app.include_router(
    crud_router
)

# Настройка CORS
app.add_middleware(
    middleware_class=CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
